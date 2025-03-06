import json
import re
import time
import requests
import subprocess
from m_h5_tk import H5TkExtractor


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
            'cna': 'FxR3H2WkqwUCAbRbsI99XbR5',
            'thw': 'cn',
            'tfstk': 'gHAt0vm5gDmGcDUUgoMhn8lCPK0nEILZdh87iijghHKpxFFMInx0MtspPVSi3A-vpntFIGOcsIFAvhNcI1sgknLVvO0woArYMMtViGji7iavAEtA3VScciKDld0nZbYw7s5XD0coZchGZ6KTfR6jlM_5502qaSGy7s5jxyVjEbLwV96aNd_fR2QcoPwXcOsQOaIC5i66cM6CPaq1GstjJ6_PuPa1CsZIOM7fGitfGAm3Wi41DSpq_4jpi0l7MSddWOIviMFAEBVldgNOx7F-oNBTpFsLGSOpK_K1nGMz-i5GbF790bPN1tpXs6OsAj1WUHdAF_Hm7_OwlLJX8l3Afexww1O-X5bhHGpB19UbGUT1v9pvXceNfdxdUw6Qkb7HqMTw1p34AFtlX1_CKbgJRt9H_TRiA5CWUFfMh3i3IG9RlgoMZQQmxujRoRgKJ-yVCw895Tw9aPcCnwIo-J2439bFJg0KJ-yVCw7dq2233-Wh8',
            't': '67b05d17a37c35cb6ae723fb2bb2e6ea',
            'wk_cookie2': '16d3a798cbf114b38ff160f1765ef328',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'lgc': 'tb528238846663',
            'dnk': 'tb528238846663',
            'tracknick': 'tb528238846663',
            'ariaDefaultTheme': 'default',
            'ariaFixed': 'true',
            'ariaScale': '1',
            'ariaMousemode': 'true',
            'ariaReadtype': '1',
            'ariaoldFixedStatus': 'false',
            'ariaStatus': 'false',
            'cookie2': '2b91f6190001f7e3a2ce903dd0b7d7f9',
            '_tb_token_': 'eeb67a673b705',
            '_samesite_flag_': 'true',
            'unb': '2219453037520',
            'cancelledSubSites': 'empty',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            '_l_g_': 'Ug%3D%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            'sgcookie': 'E100xgMaPo8vwbKntgtd2xPLiP%2BMBWhW0bqYoasRRpAhIXO7B0n5%2FPg6fFzvR%2B9ZkB2%2F35oIUgsLvcPgu7gotbZ5KBA53IA0RXzUhgRM3fUUZtA%3D',
            'havana_lgc2_0': 'eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiNjdiNWViYjE3ZGRiYTNkNjYwODBlNDc2M2QxZGJkNzUiLCJzaXRlIjowLCJ0b2tlbiI6IjE0UWJlMm9UOVJpMVZDb1B5bWxzRVNRIn0',
            '_hvn_lgc_': '0',
            'havana_lgc_exp': '1772272968018',
            'cookie3_bak': '2b91f6190001f7e3a2ce903dd0b7d7f9',
            'cookie3_bak_exp': '1741428168019',
            'sn': '',
            'uc3': 'vt3=F8dD2E8a4r73pJYE5vw%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D',
            'csg': '955e16fc',
            'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
            'skt': 'cfcac2f75d85f030',
            'existShop': 'MTc0MTE2ODk2OA%3D%3D',
            'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDIi31xxlQ%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVNKYikFnO',
            '_cc_': 'Vq8l%2BKCLiw%3D%3D',
            'havana_sdkSilent': '1741255373608',
            'uc1': 'existShop=false&pas=0&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie14=UoYaiuKfh6WWbQ%3D%3D&cookie21=UtASsssmfufd&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D',
            'sdkSilent': '1741255403532',
            '3PcFlag': '1741196888677',
            'isg': 'BGdnacRezLZV60s5P6ca1A8X9psx7DvO6o4cJDnV8fZTKIPqQbnmH0RhTqi22xNG',
            'mtop_partitioned_detect': '1',
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
        print(args)
        self.loads = json.loads(args)

    def run_js_script_with_args(self, *args):
        cmd = ['node', self.script_path] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result.stdout

    def get_rate_data(self):
        params = {
            'jsv': '2.7.4',
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
        print(str(self.loads["eM"]))
        response = requests.get(
            'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
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
    token = get_h__tk[0].split('_')[0]  # 取 `_` 前面的部分
    print(get_h__tk)
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
    auction_num_id = "680107621134"
    page_no = "2"
    try:
        for i in range(10):
            result = fetch_taobao_rate_data(auction_num_id, str(i + 1))
            print(result)
    except Exception as e:
        print(f"发生错误: {e}")
