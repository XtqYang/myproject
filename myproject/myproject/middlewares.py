import time
import subprocess
import json
from urllib.parse import urlencode

import requests
from scrapy import signals
from myproject.spiders.m_h5_tk import H5TkExtractor  # 保持原有 m_h5_tk.py 不变


class MyprojectSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TaobaoMiddleware:
    def __init__(self, node_path):
        self.node_path = node_path
        self.h5_tk_extractor = H5TkExtractor()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(node_path=settings.get('NODE_SCRIPT_PATH', 'sign_em.js'))

    def process_request(self, request, spider):
        print("请求")
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        }
        # 更新请求
        print(f"full_url:{full_url},request.meta:{request.meta},cookies:{cookies},headers:{headers}")
        # 构造新请求并标记已处理
        new_request = request.replace(
            url=full_url,
            # 交给 parse 方法处理
            callback=spider.parse,
            meta={**request.meta, 'proxy': 'http://127.0.0.1:8080', 'sign_generated': True},
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
