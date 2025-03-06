import time
import subprocess
import json
from urllib.parse import urlencode

import scrapy
from scrapy import signals
from myproject.spiders.m_h5_tk import H5TkExtractor


class MyprojectSpiderMiddleware:
    """
    Spider中间件基类

    处理爬虫的输入输出和异常。
    """

    @classmethod
    def from_crawler(cls, crawler):
        """从crawler创建中间件实例并连接信号"""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """处理爬虫的输入响应"""
        return None

    def process_spider_output(self, response, result, spider):
        """处理爬虫的输出结果"""
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """处理爬虫异常"""
        pass

    def process_start_requests(self, start_requests, spider):
        """处理初始请求"""
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """爬虫启动时的处理"""
        spider.logger.info("Spider opened: %s" % spider.name)


class TaobaoMiddleware:
    """
    淘宝API请求中间件

    负责处理淘宝API的签名生成、请求参数构建等特殊逻辑。
    通过调用外部Node.js脚本生成API所需的签名值。
    """

    def __init__(self, node_path, proxy=None):
        """
        初始化中间件

        Args:
            node_path (str): Node.js脚本路径
            proxy (str): 代理服务器地址
        """
        self.node_path = node_path
        self.proxy = proxy
        self.h5_tk_extractor = H5TkExtractor()

    @classmethod
    def from_crawler(cls, crawler):
        """
        从crawler创建中间件实例

        从settings中获取配置参数

        Args:
            crawler: Scrapy crawler对象

        Returns:
            TaobaoMiddleware实例
        """
        settings = crawler.settings
        return cls(
            node_path=settings.get('NODE_SCRIPT_PATH', 'sign_em.js'),
            proxy=settings.get('PROXY')
        )

    def process_request(self, request, spider):
        """
        处理请求

        为淘宝API请求生成正确的签名、URL参数和头信息

        Args:
            request: 原始请求对象
            spider: 爬虫实例

        Returns:
            None或新的请求对象
        """
        # 检查是否已处理过该请求
        if 'sign_generated' in request.meta:
            spider.logger.debug("请求已处理，直接放行")
            return None

        spider.logger.debug(f"处理请求: {request.url}")

        # 获取关键参数
        auction_num_id = request.meta.get('auction_num_id')
        page_no = request.meta.get('page_no')

        if not auction_num_id or not page_no:
            spider.logger.error("缺少必要参数: auction_num_id或page_no")
            return None

        # 获取H5 Token
        spider.logger.debug(f"获取商品 {auction_num_id} 的H5 Token")
        try:
            get_h__tk = self.h5_tk_extractor.get_h5_tk(auction_num_id)
            if not get_h__tk or len(get_h__tk) < 2:
                spider.logger.error("获取H5 Token失败")
                return None

            token = get_h__tk[0].split('_')[0]
            e_e = str(int(time.time() * 1000))  # 当前时间戳

            # 运行Node.js脚本生成签名
            spider.logger.debug("调用Node.js脚本生成签名")
            cmd = ['node', self.node_path, token, str(page_no), auction_num_id, e_e, "12574478"]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                if result.returncode != 0:
                    spider.logger.error(f"Node.js脚本执行失败: {result.stderr}")
                    return None
            except subprocess.CalledProcessError as e:
                spider.logger.error(f"Node.js调用异常: {e}")
                return None
            except FileNotFoundError:
                spider.logger.error(f"找不到Node.js或脚本: {self.node_path}")
                return None

            # 解析签名结果
            try:
                sign_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                spider.logger.error(f"签名结果解析失败: {result.stdout}")
                return None

            # 获取签名值
            sign = sign_data.get('eM', '')
            if not sign:
                spider.logger.error("签名值为空")
                return None

            # 构造API请求参数
            spider.logger.debug("构造API请求参数")
            params = {
                'jsv': '2.7.4',
                'appKey': '12574478',
                't': str(e_e),
                'sign': sign,
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

            # 构造Cookies
            cookies = {
                # 这里应该使用更安全的Cookie管理机制，而不是硬编码
                '_m_h5_tk': get_h__tk[0],
                '_m_h5_tk_enc': get_h__tk[1],
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
            }

            # 构造请求头
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
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            }

            # 创建新请求并标记为已处理
            spider.logger.info(f"为商品 {auction_num_id} 的第 {page_no} 页评论创建请求")

            # 添加代理设置(如果有)
            meta = {**request.meta, 'sign_generated': True}
            if self.proxy:
                meta['proxy'] = self.proxy

            new_request = request.replace(
                url=full_url,
                callback=spider.parse,
                meta=meta,
                cookies=cookies,
                headers=headers,
            )

            return new_request

        except Exception as e:
            spider.logger.error(f"处理请求过程中出现异常: {e}")
            return None

    def process_response(self, request, response, spider):
        """
        处理响应

        检查响应状态，记录必要信息

        Args:
            request: 请求对象
            response: 响应对象
            spider: 爬虫实例

        Returns:
            response对象
        """
        spider.logger.debug(f"处理响应: {response.url}")

        if response.status != 200:
            spider.logger.error(f"请求失败，状态码: {response.status}")

        return response

    def process_exception(self, request, exception, spider):
        """
        处理请求异常

        记录异常信息，便于问题排查

        Args:
            request: 请求对象
            exception: 异常对象
            spider: 爬虫实例

        Returns:
            None
        """
        spider.logger.error(f"请求异常: {type(exception).__name__}: {exception}")
        spider.logger.error(f"异常请求URL: {request.url}")
        spider.logger.error(f"异常请求Meta: {request.meta}")

        return None
