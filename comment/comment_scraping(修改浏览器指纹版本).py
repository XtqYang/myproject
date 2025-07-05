# --Unicode=utf-8--
import json
import re
import time
import subprocess
from m_h5_tk import H5TkExtractor
import requests_go

tls = requests_go.tls_config.TLSConfig()
tls.ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,16-18-5-27-0-13-11-43-45-35-51-23-10-65281-17513-21,29-23-24,0"
tls.pseudo_header_order = [
    ":method",
    ":authority",
    ":scheme",
    ":path",
]
tls.tls_extensions.cert_compression_algo = ["brotli"]
tls.tls_extensions.supported_signature_algorithms = [
    "ecdsa_secp256r1_sha256",
    "rsa_pss_rsae_sha256",
    "rsa_pkcs1_sha256",
    "ecdsa_secp384r1_sha384",
    "rsa_pss_rsae_sha384",
    "rsa_pkcs1_sha384",
    "rsa_pss_rsae_sha512",
    "rsa_pkcs1_sha512"
]
tls.tls_extensions.supported_versions = [
    "GREASE",
    "1.3",
    "1.2"
]
tls.tls_extensions.psk_key_exchange_modes = [
    "PskModeDHE"
]
tls.tls_extensions.key_share_curves = [
    "GREASE",
    "X25519"
]
tls.http2_settings.settings = {
    "HEADER_TABLE_SIZE": 65536,
    "ENABLE_PUSH": 0,
    "MAX_CONCURRENT_STREAMS": 1000,
    "INITIAL_WINDOW_SIZE": 6291456,
    "MAX_HEADER_LIST_SIZE": 262144
}
tls.http2_settings.settings_order = [
    "HEADER_TABLE_SIZE",
    "ENABLE_PUSH",
    "MAX_CONCURRENT_STREAMS",
    "INITIAL_WINDOW_SIZE",
    "MAX_HEADER_LIST_SIZE"
]
tls.http2_settings.connection_flow = 15663105


class TaobaoRateScraper:
    def __init__(self, script_path, _m_h5_tk, _m_h5_tk_enc, token, pageNo, auctionNumId, eE, eT):
        self.script_path = script_path
        self._m_h5_tk = _m_h5_tk
        self._m_h5_tk_enc = _m_h5_tk_enc
        self.token = token
        self.pageNo = pageNo
        self.auctionNumId = auctionNumId
        self.eE = eE
        self.eT = eT
        self.cookies = {
            '_samesite_flag_': 'true',
            'cookie2': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            't': '20c1b8c96e003a04455d570c7d82bc72',
            '_tb_token_': '58e33aa81eba5',
            'thw': 'cn',
            '_hvn_lgc_': '0',
            'cookie3_bak': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            'wk_cookie2': '151177e5c67f84d11997af48b49e9de2',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'lgc': 'tb528238846663',
            'cancelledSubSites': 'empty',
            'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
            'dnk': 'tb528238846663',
            'tracknick': 'tb528238846663',
            'sgcookie': 'E100EukvQfosjPXXEQdYSGhLUS9oUZf4Uzz%2FhykDpSfFfRJDzmSS8gSSSL4xDCezKLksA2YLV6HroKqr2HrA%2BaoLzIC0dlK752fN31BmZeevMKo%3D',
            'havana_lgc2_0': 'eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiODcxNTZhYzE2NTk3ZjU3MGNjZjZlZDNlMTUyYmU4YmMiLCJzaXRlIjowLCJ0b2tlbiI6IjFNOWVNSzhUSGhkVXhPWndtQkZlRlh3In0',
            'havana_lgc_exp': '1772730920811',
            'cookie3_bak_exp': '1741886120812',
            'uc3': 'lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dD2EjKML%2BJUk1PXv0%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D',
            'csg': '16ac354f',
            'skt': '30456cdcabcd41ba',
            'existShop': 'MTc0MTYyNjkyMA%3D%3D',
            'uc4': 'id4=0%40U2gqwARzFIUfVaMSaLM2EjsVMwls%2FYrV&nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDWmQ7bHpQ%3D%3D',
            '_cc_': 'UIHiLt3xSw%3D%3D',
            'x5sec': '7b2274223a313734313734353934322c22733b32223a2261653836646632373139343538653138222c22617365727665723b33223a22307c43492f6577373447454f664a784b6342476738794d6a45354e44557a4d444d334e5449774f7a4569436d4e6863484e736157526c646a49772b6265457867493d227d',
            'mtop_partitioned_detect': '1',
            'sdkSilent': '1741832345046',
            'havana_sdkSilent': '1741832345046',
            '3PcFlag': '1741746140697',
            '_m_h5_tk': str(_m_h5_tk),
            '_m_h5_tk_enc': str(_m_h5_tk_enc),
        }
        self.headers = {
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

        args = self.run_js_script_with_args(self.token, self.pageNo, self.auctionNumId, self.eE, eT).strip()
        self.loads = json.loads(args)

    def run_js_script_with_args(self, *args):
        cmd = ['node', self.script_path] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result.stdout

    def get_rate_data(self):
        params = {
            'jsv': '2.7.0',
            'appKey': '12574478',
            't': str(self.eE),
            'sign': str(self.loads["eM"]),
            'api': 'mtop.taobao.rate.detaillist.get',
            'v': '6.0',
            'isSec': '0',
            'ecode': '1',
            'timeout': '20000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'jsonpIncPrefix': 'pcdetail',
            'callback': 'mtopjsonppcdetail25',
            'data': f'{{"showTrueCount":false,"auctionNumId":"{self.auctionNumId}","pageNo":{int(self.pageNo)},"pageSize":20,"rateType":"","searchImpr":"-8","orderType":"","expression":"","rateSrc":"pc_rate_list"}}',
        }
        response = requests_go.get(
            'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            tls_config=tls,
            verify=False
        )
        return response.text


def fetch_taobao_rate_data(auction_num_id, page_no):
    """
    封装函数：获取淘宝评价数据
    :param script_path: JavaScript 文件路径
    :param auction_num_id: 商品编号
    :param page_no: 页码
    :return: 解析后的 JSON 数据
    """
    script_path = "sign_em.js"
    # 获取 H5 Token
    h_tk_extractor = H5TkExtractor()
    get_h__tk = h_tk_extractor.get_h5_tk(auction_num_id)
    print(get_h__tk)
    token = get_h__tk[0].split('_')[0]  # 取 `_` 前面的部分
    e_e = str(int(time.time() * 1000))  # 当前时间戳
    e_t = "12574478"  # 固定值
    # 创建 TaobaoRateScraper 实例
    scraper = TaobaoRateScraper(script_path, get_h__tk[0], get_h__tk[1], token, page_no, auction_num_id, e_e, e_t)
    data_str = scraper.get_rate_data()
    # 解析 JSON 数据
    match = re.search(r'mtopjsonp\w*\((\{.*\})\)', data_str)
    if match:
        json_data = json.loads(match.group(1))

        return json_data
    else:
        raise ValueError("未找到有效的 JSON 数据")


# 使用示例
if __name__ == "__main__":
    auction_num_id = "769361086770"
    page_no = "2"
    for i in range(5):
        print(f"正在获取第{i}条数据")
        result = fetch_taobao_rate_data(auction_num_id, str(i + 1))
        print((result))
        print((result)["ret"])
