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
from scrapy.exceptions import NotConfigured, IgnoreRequest
from myproject.utils.m_h5_tk import H5TkExtractor  # 保持原有 m_h5_tk.py 不变
from twisted.internet.error import TimeoutError, TCPTimedOutError


class RandomUserAgentMiddleware:
    """
    随机User-Agent中间件
    为每个请求随机分配一个User-Agent头
    """

    def __init__(self, user_agent_list):
        """
        初始化随机User-Agent中间件

        Args:
            user_agent_list: User-Agent字符串列表
        """
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        """
        从Scrapy配置初始化中间件

        Args:
            crawler: Scrapy爬虫实例

        Returns:
            RandomUserAgentMiddleware实例
        """
        settings = crawler.settings
        user_agent_list = settings.get('USER_AGENT_LIST', [])
        middleware = cls(user_agent_list)
        # 在Scrapy框架中，这行代码的作用是将中间件的spider_opened方法注册到Scrapy的信号系统中：
        # signals.spider_opened是Scrapy内置信号，当爬虫开始运行时触发
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        """
        爬虫启动时的处理

        Args:
            spider: 爬虫实例
        """
        spider.logger.info("RandomUserAgentMiddleware 已启用")

    def process_request(self, request, spider):
        """
        处理请求，设置随机User-Agent

        Args:
            request: Scrapy请求对象
            spider: 爬虫实例

        Returns:
            None: 请求处理完成，继续后续中间件处理
        """
        if self.user_agent_list:
            # 随机选择一个 UA
            ua = random.choice(self.user_agent_list)
            request.headers.setdefault('User-Agent', ua)


class ProxyPoolMiddleware:
    """
    Scrapy 代理池中间件
    从指定代理池API获取代理地址，并自动设置到请求中
    包含失效代理处理与重试机制
    """

    def __init__(self, proxy_pool_url, max_retry=3, min_delay=1, max_delay=5):
        """
        初始化代理池中间件

        Args:
            proxy_pool_url: 获取代理的API地址
            max_retry: 获取代理的最大重试次数
            min_delay: 重试最小延迟（秒）
            max_delay: 重试最大延迟（秒）
        """
        self.proxy_pool_url = proxy_pool_url
        self.max_retry = max_retry  # 获取代理的最大重试次数
        self.min_delay = min_delay  # 重试延迟下限
        self.max_delay = max_delay  # 重试延迟上限
        self.logger = logging.getLogger(__name__)
        self.failed_proxies = set()  # 记录失效的代理
        self.lock = threading.Lock()  # 线程锁，防止并发访问问题

        # 验证代理池URL配置
        if not self.proxy_pool_url:
            raise NotConfigured("PROXY_POOL_URL 未在配置中设置")

    @classmethod
    def from_crawler(cls, crawler):
        """
        从Scrapy配置初始化中间件

        Args:
            crawler: Scrapy爬虫实例

        Returns:
            ProxyPoolMiddleware实例
        """
        proxy_pool_url = crawler.settings.get("PROXY_POOL_URL")
        max_retry = crawler.settings.getint("PROXY_MAX_RETRY", 3)
        min_delay = crawler.settings.getint("RETRY_MIN_DELAY", 1)
        max_delay = crawler.settings.getint("RETRY_MAX_DELAY", 5)

        # 创建中间件实例
        middleware = cls(
            proxy_pool_url=proxy_pool_url,
            max_retry=max_retry,
            min_delay=min_delay,
            max_delay=max_delay
        )

        return middleware

    def _get_proxy_from_pool(self, blacklist=None):
        """
        从代理池获取代理地址，避开已知的失效代理

        Args:
            blacklist: 需要避开的代理集合（可选）

        Returns:
            str: 代理地址，格式如 "http://IP:PORT" 或 None（获取失败）
        """
        if blacklist is None:
            blacklist = set()

        retry = 0
        while retry < self.max_retry:
            response = requests.get(self.proxy_pool_url)
            proxy_data = json.loads(response.text)
            # 验证代理数据格式
            if "proxy" not in proxy_data:
                self.logger.error("代理池响应缺少 'proxy' 字段")
                retry += 1
                continue
            proxy_ip_port = proxy_data["proxy"]
            # 检查是否在黑名单中
            if proxy_ip_port in blacklist:
                self.logger.debug(f"跳过黑名单代理: {proxy_ip_port}")
                # 如果是黑名单代理，继续尝试获取其他代理，但不增加重试计数
                retry += 1
                continue
            print(f"获取代理：{proxy_ip_port}")
            return proxy_ip_port
        self.logger.error("超过最大重试次数，未能获取有效代理")
        return None

    def process_request(self, request, spider):
        """
        处理请求的代理设置

        Args:
            request: Scrapy请求对象
            spider: 爬虫实例

        Returns:
            None: 请求处理完成，继续后续中间件处理
        """
        # 如果请求已标记为不使用代理，则跳过
        if request.meta.get("dont_proxy", False):
            return None

        # 如果请求已包含代理且不在失效列表中，则无需重新设置
        if "proxy" in request.meta and request.meta["proxy"] not in self.failed_proxies:
            return None

        # 获取新代理，排除已知失效代理
        with self.lock:
            proxy_url = self._get_proxy_from_pool(blacklist=self.failed_proxies)

        if proxy_url:
            request.meta["proxy"] = proxy_url
            self.logger.debug(f"设置代理: {proxy_url}")
        else:
            ...
            # 如果获取代理失败，标记请求为不使用代理
            # self.logger.warning("未获取到有效代理，本次请求将不使用代理")
            # request.meta["dont_proxy"] = True
            # if "proxy" in request.meta:
            #     del request.meta["proxy"]

    def process_exception(self, request, exception, spider):
        """
        处理请求异常，特别是代理相关的异常

        Args:
            request: 引发异常的请求
            exception: 异常对象
            spider: 爬虫实例

        Returns:
            Request: 重新调度的请求对象（如果需要重试）
            None: 不进行重试，继续后续异常处理
        """
        # 检查是否是代理相关异常
        if "proxy" in request.meta:
            failed_proxy = request.meta["proxy"]
            self.logger.error(f"代理 {failed_proxy} 请求失败: {str(exception)}")

            # 将失效代理添加到黑名单
            with self.lock:
                self.failed_proxies.add(failed_proxy)

            # 创建新的请求副本，但移除当前代理
            new_request = request.copy()
            if "proxy" in new_request.meta:
                del new_request.meta["proxy"]

            # 重置失败计数器，确保请求可以重试
            new_request.meta["retry_times"] = 0

            # 标记为原始请求的重试
            new_request.meta["proxy_retry"] = True
            new_request.dont_filter = True  # 防止被去重过滤器过滤

            self.logger.info(f"使用新代理重新调度请求: {request.url}")
            return new_request

        return None


class TaobaoMiddleware:
    """
    淘宝API请求处理中间件
    处理针对淘宝API的特殊签名和请求参数
    """

    def __init__(self, node_path, max_retries=3):
        """
        初始化淘宝中间件

        Args:
            node_path: Node.js脚本路径
            max_retries: 签名生成最大重试次数
        """
        self.node_path = node_path
        self.h5_tk_extractor = H5TkExtractor()
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        self.auction_num_id = "769361086770"
        self.proxy_middleware = None  # 用于引用ProxyPoolMiddleware实例

    @classmethod
    def from_crawler(cls, crawler):
        """
        从Scrapy配置初始化中间件

        Args:
            crawler: Scrapy爬虫实例

        Returns:
            TaobaoMiddleware实例
        """
        settings = crawler.settings
        node_path = settings.get('NODE_SCRIPT_PATH', 'sign_em.js')
        max_retries = settings.getint('TAOBAO_MAX_RETRIES', 3)
        return cls(node_path=node_path, max_retries=max_retries)



    def _generate_sign(self, token, page_no, auction_num_id, timestamp, app_key, retry=0):
        """
        调用Node.js脚本生成淘宝API签名

        Args:
            token: H5 Token值
            page_no: 评论页码
            auction_num_id: 商品ID
            timestamp: 时间戳
            app_key: 应用Key
            retry: 当前重试次数

        Returns:
            dict: 包含签名的字典，失败返回None
        """
        if retry >= self.max_retries:
            self.logger.error("生成签名超过最大重试次数")
            return None

        # 运行 Node.js 生成签名
        cmd = ['node', self.node_path, token, str(page_no), auction_num_id, timestamp, app_key]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                self.logger.error(f"Node.js 脚本执行失败: {result.stderr}")
                time.sleep(0.5)  # 失败后短暂延迟
                return self._generate_sign(token, page_no, auction_num_id, timestamp, app_key, retry + 1)

            try:
                sign_data = json.loads(result.stdout)
                return sign_data
            except json.JSONDecodeError:
                self.logger.error(f"签名数据解析失败: {result.stdout}")
                time.sleep(0.5)
                return self._generate_sign(token, page_no, auction_num_id, timestamp, app_key, retry + 1)

        except subprocess.SubprocessError as e:
            self.logger.error(f"Node.js 进程调用异常: {str(e)}")
            time.sleep(1)  # 失败后延迟更长时间
            return self._generate_sign(token, page_no, auction_num_id, timestamp, app_key, retry + 1)

        except Exception as e:
            self.logger.error(f"生成签名过程中出现未知异常: {str(e)}")
            return None

    def process_request(self, request, spider):
        """
        处理淘宝API请求，添加必要的签名和参数

        Args:
            request: Scrapy请求对象
            spider: 爬虫实例

        Returns:
            Request: 修改后的请求对象
            None: 请求处理完成，继续后续中间件处理
        """
        # 检查是否已经处理过该请求
        if 'sign_generated' in request.meta:
            return None  # 已处理过的请求直接放行

        # 获取请求参数
        auction_num_id = "769361086770"
        page_no = request.meta.get('page_no', 1)

        # 获取 H5 Token
        h5_tk_data = self.h5_tk_extractor.get_h5_tk(auction_num_id)
        print(f"H5_Token:{h5_tk_data}")

        if not h5_tk_data or h5_tk_data[0] is None or h5_tk_data[1] is None:
            self.logger.error("获取 H5 Token 失败")
            # 如果H5 Token获取失败，建议延迟后重试
            time.sleep(2)
            raise IgnoreRequest("H5 Token获取失败，请求被忽略")

        # 解析token
        token = h5_tk_data[0].split('_')[0]
        app_key = "12574478"  # 固定的app_key
        timestamp = str(int(time.time() * 1000))

        # 生成签名
        sign_data = self._generate_sign(token, page_no, auction_num_id, timestamp, app_key)
        print(f"sign_data:{sign_data}")
        if not sign_data or 'eM' not in sign_data:
            self.logger.error("签名生成失败")
            raise IgnoreRequest("签名生成失败，请求被忽略")

        # 构造API请求参数

        params = {
            'jsv': '2.7.4',
            'appKey': '12574478',
            't': str(timestamp),
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

        # 构造完整URL
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'
        full_url = base_url + '?' + urlencode(params)

        # 设置必要的cookies
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
            '_m_h5_tk': h5_tk_data[0],
            '_m_h5_tk_enc': h5_tk_data[1],
        }

        # 设置请求头
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

        # 创建新请求并标记为已处理
        new_request = request.replace(
            url=full_url,
            callback=spider.parse,  # 确保使用正确的解析函数
            meta={**request.meta, 'sign_generated': True},
            cookies=cookies,
            headers=headers,
        )

        # 记录请求信息
        self.logger.debug(f"代理设置: {new_request.meta.get('proxy', '未设置')}")
        self.logger.debug(f"请求URL: {full_url[:100]}...")

        return new_request

    def process_response(self, request, response, spider):
        print(f"响应：{response}")
        """
        处理响应数据

        Args:
            request: 原始请求对象
            response: 响应对象
            spider: 爬虫实例

        Returns:
            Response: 处理后的响应对象
        """
        # 记录响应信息（仅调试用）
        if spider.settings.getbool('DEBUG', False):
            self.logger.debug(f"响应状态: {response.status}")
            self.logger.debug(f"响应体预览: {response.text[:200]}")

        # 检查响应状态
        if response.status != 200:
            self.logger.error(f"请求失败: 状态码 {response.status}")

        # 检查是否包含错误信息
        if "sign_generated" in request.meta and b'"code":"FAIL"' in response.body:
            error_info = "未知错误"
            try:
                # 尝试从jsonp响应中提取错误信息
                jsonp_text = response.text
                json_start = jsonp_text.find('(') + 1
                json_end = jsonp_text.rfind(')')
                if json_start > 0 and json_end > json_start:
                    json_str = jsonp_text[json_start:json_end]
                    data = json.loads(json_str)
                    if 'ret' in data and data['ret']:
                        error_info = data['ret'][0]
            except (json.JSONDecodeError, IndexError, KeyError):
                pass

            self.logger.error(f"API返回错误: {error_info}")

        return response

    def process_exception(self, request, exception, spider):
        """
        处理请求异常：移除失效代理并重新请求，并输出错误响应体

        Args:
            request: 发生异常的请求对象
            exception: 异常对象
            spider: 爬虫实例

        Returns:
            Request: 重新调度的请求对象
            None: 不进行重试，继续后续异常处理
        """
        # 记录异常详细信息
        self.logger.error(f"请求异常: {type(exception).__name__}: {str(exception)}")

        # 检查是否为超时类异常，这些异常很可能是代理问题
        is_timeout = isinstance(exception, (TimeoutError, TCPTimedOutError,
                                            requests.exceptions.Timeout,
                                            requests.exceptions.ConnectTimeout))

        # 检查是否存在代理设置
        if "proxy" in request.meta:
            failed_proxy = request.meta["proxy"]
            self.logger.error(f"代理 {failed_proxy} 请求异常，已加入黑名单并重新请求")

            # 尝试获取并输出错误响应体（如果存在）
            if hasattr(exception, 'response') and exception.response:
                try:
                    error_body = exception.response.body.decode('utf-8')
                    self.logger.error(f"错误响应体: {error_body[:500]}...")  # 只记录前500个字符
                except (AttributeError, UnicodeDecodeError) as e:
                    self.logger.error(f"无法解析错误响应体: {str(e)}")
            else:
                self.logger.info("异常中不包含响应体信息")

            # 将失效代理添加到ProxyPoolMiddleware的黑名单
            if self.proxy_middleware:
                with self.proxy_middleware.lock:
                    self.proxy_middleware.failed_proxies.add(failed_proxy)
                self.logger.info(f"已将代理 {failed_proxy} 添加到黑名单")
            else:
                # 尝试在spider中查找代理池中间件
                for middleware in spider.crawler.engine.downloader.middleware.middlewares:
                    if isinstance(middleware, ProxyPoolMiddleware):
                        with middleware.lock:
                            middleware.failed_proxies.add(failed_proxy)
                        self.proxy_middleware = middleware  # 缓存引用
                        self.logger.info(f"已找到ProxyPoolMiddleware并将代理 {failed_proxy} 添加到黑名单")
                        break
                else:
                    self.logger.warning("无法更新代理黑名单：未找到ProxyPoolMiddleware")

            # 创建新请求并移除当前代理
            new_request = request.copy()
            del new_request.meta["proxy"]  # 移除失效代理

            # 重置相关状态
            new_request.meta["retry_times"] = 0  # 重置重试次数
            new_request.dont_filter = True  # 防止被去重过滤

            # 根据异常类型添加额外信息
            if is_timeout:
                new_request.meta["timeout_retry"] = True
                self.logger.info(f"超时异常，重新调度请求: {request.url}")
            else:
                new_request.meta["error_retry"] = True
                self.logger.info(f"非超时异常，重新调度请求: {request.url}")

            # 如果存在sign_generated标记，需要移除以便重新生成签名
            if 'sign_generated' in new_request.meta:
                del new_request.meta['sign_generated']
                self.logger.info("移除sign_generated标记，将重新生成签名")

            return new_request

        # 如果请求没有使用代理，或者是其他类型的异常，可以考虑直接重试或者放弃
        if is_timeout:
            # 对于超时异常，即使没有使用代理也尝试重试
            self.logger.info(f"请求超时且未使用代理，将重新调度: {request.url}")
            new_request = request.copy()
            new_request.dont_filter = True
            if 'sign_generated' in new_request.meta:
                del new_request.meta['sign_generated']  # 重新生成签名
            return new_request

        # 其他情况交给Scrapy默认异常处理
        return None