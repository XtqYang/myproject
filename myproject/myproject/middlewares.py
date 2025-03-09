import json
import time
import random
import logging
import requests
import threading
import subprocess
from scrapy import signals
from collections import deque
from urllib.parse import urlencode
from scrapy.exceptions import NotConfigured
from myproject.spiders.m_h5_tk import H5TkExtractor  # 保持原有 m_h5_tk.py 不变
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ProxyPoolMiddleware:
    """Scrapy 代理池中间件，实现自动代理管理和失效重试机制"""

    def __init__(self, PROXY_API, pool_size=5, health_check_url='https://httpbin.org/ip'):
        self.PROXY_API = PROXY_API
        self.pool_size = pool_size
        self.health_check_url = health_check_url
        self.proxy_pool = deque()  # 改用双端队列提高效率
        self.failed_proxies = set()
        self.logger = logging.getLogger(__name__)
        self.lock = threading.Lock()  # 线程锁
        # 初始化时预填充代理池
        self._refresh_proxy_pool()
    @classmethod
    def from_crawler(cls, crawler):
        """从Scrapy配置初始化中间件"""
        PROXY_API = crawler.settings.get('PROXY_API')
        if not PROXY_API:
            raise NotConfigured('PROXY_API 未在配置中设置')

        return cls(
            PROXY_API=PROXY_API,
            pool_size=crawler.settings.getint('PROXY_POOL_SIZE', 10),
            health_check_url=crawler.settings.get('PROXY_HEALTH_CHECK_URL', 'https://httpbin.org/ip')
        )

    def _fetch_new_proxy(self):
        """从代理池服务获取新代理（修改为直接返回文本）"""
        try:
            response = requests.get(self.PROXY_API, timeout=5)
            if response.status_code == 200:
                return response.text.strip()  # 假设API直接返回ip:port
            self.logger.warning(f"代理API返回状态码: {response.status_code}")
        except Exception as e:
            self.logger.warning(f"获取代理失败: {str(e)}")
        return None

    def _health_check(self, proxy):
        """验证代理可用性（优化超时时间）"""
        try:
            resp = requests.get(
                self.health_check_url,
                proxies={'http': proxy, 'https': proxy},
                timeout=5  # 缩短超时时间
            )
            if resp.json().get('origin'):
                return True
        except Exception as e:
            self.logger.debug(f"代理检测失败(验证代理可用性): {proxy} - {str(e)}")
        return False

    def _refresh_proxy_pool(self):
        """线程安全的代理池刷新机制"""
        with self.lock:
            while len(self.proxy_pool) < self.pool_size:
                proxy = self._fetch_new_proxy()
                if not proxy:
                    continue

                # 格式标准化
                if "://" not in proxy:
                    proxy = f"http://{proxy}"

                # 跳过失效代理
                if proxy in self.failed_proxies:
                    continue

                # 执行健康检查
                if self._health_check(proxy):
                    self.proxy_pool.append(proxy)
                    self.logger.info(f"成功添加代理: {proxy}")
                else:
                    self.failed_proxies.add(proxy)
                    self.logger.warning(f"代理检测失败(线程安全的代理池刷新机制): {proxy}")

    def process_request(self, request, spider):
        print(1111)
        """处理请求代理设置（添加线程安全）"""
        if 'proxy' in request.meta:
            return

        # 检查并维护代理池容量
        with self.lock:
            if len(self.proxy_pool) < self.pool_size // 2:
                self._refresh_proxy_pool()

        if not self.proxy_pool:
            spider.logger.error("代理池为空，无法设置代理")
            return

        # 获取并设置代理
        with self.lock:
            proxy = self.proxy_pool.popleft()

        request.meta['proxy'] = proxy
        spider.logger.debug(f"当前使用代理: {proxy}")

        # 异步补充代理池
        self._refresh_proxy_pool()

    def process_response(self, request, response, spider):
        """处理响应（优化状态码判断逻辑）"""
        if response.status in [403, 429, 407, 500, 502, 503]:
            bad_proxy = request.meta.get('proxy')
            if bad_proxy:
                with self.lock:
                    self.failed_proxies.add(bad_proxy)
                spider.logger.warning(f"标记失效代理: {bad_proxy} 状态码: {response.status}")
                # 立即刷新代理池
                self._refresh_proxy_pool()
                return request.replace(dont_filter=True)
        return response

    def process_exception(self, request, exception, spider):
        """处理异常（添加线程安全）"""
        if 'proxy' in request.meta:
            bad_proxy = request.meta['proxy']
            with self.lock:
                self.failed_proxies.add(bad_proxy)
                if bad_proxy in self.proxy_pool:
                    self.proxy_pool.remove(bad_proxy)

            spider.logger.error(f"移除失效代理: {bad_proxy} 原因: {exception}")
            # 立即补充新代理
            self._refresh_proxy_pool()
            return request.replace(dont_filter=True)


class RandomUserAgentMiddleware:
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        user_agent_list = settings.get('USER_AGENT_LIST', [])
        middleware = cls(user_agent_list)
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        spider.logger.info("RandomUserAgentMiddleware 已启用")

    def process_request(self, request, spider):
        # 随机选择一个 UA
        ua = random.choice(self.user_agent_list)
        request.headers.setdefault('User-Agent', ua)


class TaobaoMiddleware:
    def __init__(self, node_path):
        self.node_path = node_path
        self.h5_tk_extractor = H5TkExtractor()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(node_path=settings.get('NODE_SCRIPT_PATH', 'sign_em.js'))

    def process_request(self, request, spider):
        # 检查是否已经处理过该请求
        if 'sign_generated' in request.meta:
            return None  # 已处理过的请求直接放行
        auction_num_id = request.meta.get('auction_num_id')
        page_no = request.meta.get('page_no')
        # 获取 H5 Token
        get_h__tk = self.h5_tk_extractor.get_h5_tk(auction_num_id)
        if not get_h__tk or len(get_h__tk) < 2:
            spider.logger.error("获取 H5 Token 失败")
            return None
        token = get_h__tk[0].split('_')[0]
        e_e = str(int(time.time() * 1000))
        # 运行 Node.js 生成签名
        cmd = ['node', self.node_path, token, str(page_no), auction_num_id, e_e, "12574478"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            spider.logger.error(f"Node.js 调用失败: {e}")
            return None
        try:
            sign_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            spider.logger.error("签名生成失败: %s", result.stdout)
            return None
        # 构造爬虫请求参数
        params = {
            'jsv': '2.7.4',
            'appKey': '12574478',
            't': str(e_e),
            'sign': str(sign_data.get('eM', '')),
            'api': 'mtop.taobao.rate.detaillist.get',
            'v': '6.0',
            'isSec': '0',
            'ecode': '1',
            'timeout': '20000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'jsonpIncPrefix': 'pcdetail',
            'callback': 'mtopjsonppcdetail25',
            'data': f'{{"showTrueCount":false,"auctionNumId":"{auction_num_id}","pageNo":{int(page_no)},"pageSize":20,"rateType":"","searchImpr":"-8","orderType":"","expression":"","rateSrc":"pc_rate_list"}}',
        }
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'
        full_url = base_url + '?' + urlencode(params)
        cookies = {
            'cna': 'FxR3H2WkqwUCAbRbsI99XbR5',
            'thw': 'cn',
            '_cc_': 'U%2BGCWk%2F7og%3D%3D',
            'tfstk': 'gHAt0vm5gDmGcDUUgoMhn8lCPK0nEILZdh87iijghHKpxFFMInx0MtspPVSi3A-vpntFIGOcsIFAvhNcI1sgknLVvO0woArYMMtViGji7iavAEtA3VScciKDld0nZbYw7s5XD0coZchGZ6KTfR6jlM_5502qaSGy7s5jxyVjEbLwV96aNd_fR2QcoPwXcOsQOaIC5i66cM6CPaq1GstjJ6_PuPa1CsZIOM7fGitfGAm3Wi41DSpq_4jpi0l7MSddWOIviMFAEBVldgNOx7F-oNBTpFsLGSOpK_K1nGMz-i5GbF790bPN1tpXs6OsAj1WUHdAF_Hm7_OwlLJX8l3Afexww1O-X5bhHGpB19UbGUT1v9pvXceNfdxdUw6Qkb7HqMTw1p34AFtlX1_CKbgJRt9H_TRiA5CWUFfMh3i3IG9RlgoMZQQmxujRoRgKJ-yVCw895Tw9aPcCnwIo-J2439bFJg0KJ-yVCw7dq2233-Wh8',
            't': '67b05d17a37c35cb6ae723fb2bb2e6ea',
            '_tb_token_': 'f3e657fa10eee',
            '_samesite_flag_': 'true',
            'cookie2': '1f8db2010899859f7ae746c37c3e4ab9',
            '3PcFlag': '1740833156528',
            'sgcookie': 'E100%2Bg17ZWEoFlVN3NYjICxI4oT6QCYNQhw%2Fa%2BGrmP02Q4TU8UIjF1tuWjG%2B8fYcP%2FNnJpEN3G9WgKQnLApDFhXi6DrnsSLdtpRAu5saC8qwTno%3D',
            'wk_cookie2': '16d3a798cbf114b38ff160f1765ef328',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'unb': '2219453037520',
            'uc3': 'id2=UUpgT7v9r1VNs0K1OQ%3D%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dD2E8Zf9qKwtLe3ys%3D',
            'csg': '4a08dd84',
            'lgc': 'tb528238846663',
            'cancelledSubSites': 'empty',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'dnk': 'tb528238846663',
            'skt': '47b49b3557d1e99e',
            'existShop': 'MTc0MDgzMzIyMQ%3D%3D',
            'uc4': 'id4=0%40U2gqwARzFIUfVaMSaLM2EjsU9dS%2FyoQm&nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FY2hriW54Q%3D%3D',
            'tracknick': 'tb528238846663',
            '_l_g_': 'Ug%3D%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            'ariaDefaultTheme': 'default',
            'ariaFixed': 'true',
            'ariaReadtype': '1',
            'ariaoldFixedStatus': 'false',
            'ariaScale': '1',
            'ariaMousemode': 'true',
            'ariaStatus': 'false',
            'uc1': 'cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=UIHiLt3xSalX&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoYai9dzGEgTFw%3D%3D&existShop=false',
            'isg': 'BLm5VEhe-m0zDKX3XT3MYs1dyCWTxq146PRyatvuNeBfYtn0Ixa9SCex5OaUQUWw',
            'mtop_partitioned_detect': '1',
            '_m_h5_tk': get_h__tk[0],
            '_m_h5_tk_enc': get_h__tk[1],
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://item.taobao.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
        }
        # 构造新请求并标记已处理
        new_request = request.replace(
            url=full_url,
            # 交给 parse 方法处理
            callback=spider.parse,
            # meta={**request.meta, 'proxy': 'http://127.0.0.1:8080', 'sign_generated': True},
            meta={**request.meta, 'sign_generated': True},
            cookies=cookies,
            headers=headers,
        )
        spider.logger.debug(f"Proxy in meta: {new_request.meta.get('proxy')}")

        return new_request

    def process_process_response(self, request, response, spider):
        print("响应")
        if response.status != 200:
            spider.logger.error(f"请求失败: {response.status}")
            return response
        # 检查是否需要生成签名（避免重复处理）
        if 'sign_generated' in request.meta:
            return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"请求异常: {exception}")
        return None
