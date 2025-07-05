import re

import requests


class H5TkExtractor:
    def __init__(self):
        self.sign = 'd37e5e17062c5012dddfbdbb09f6af2d'
        self.t = '1741094759692'
        self.cookies = {
            'cna': 'pl1ZIATN70kBASQKQs3BtsoX',
            '_m_h5_tk': '20b7c931702c52406c6d013d4b7a0b9f_1741857473207',
            '_m_h5_tk_enc': '0395e3390143da9c7e619a6a43d31a08',
            'xlly_s': '2',
            '_samesite_flag_': 'true',
            '3PcFlag': '1741847771313',
            'isg': 'BLy8yOc-953ussPBOuKaea5GhlhutWDfDf4O6JY9yaeKYV7rscQjbg_TRc-9KZg3',
            'ockeqeudmj': 'umMgpvc%%3D',
            '_w_tb_nick': 'tb528238846663',
            'munb': '2219453037520',
            'WAPFDFDTGFG': '%%2B4cMKKP%%2B8PI%%2BKK8b5ivJlRhvkWJHKcWpmQ%%3D%%3D',
            '_w_app_lg': '0',
            'wk_cookie2': '1fa081a0de06c897f64de39d52884ce8',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%%3D%%3D',
            'sgcookie': 'E100foft2RXRXssZbMDCh9qjtNzdAD%%2F3mrZapxFprnAe8ceav3gTLStKXDt%%2FpCLHTWbolUl1zsYuNOS2haohMMqgnLpGbdH%%2BKDzOqtAJMcGlpmfHLYsVMIPgJpRjRIDOBiYS',
            'last_slid_taobao_taobao_h5': 'E86062448CDC53FB951BA7',
            'unb': '2219453037520',
            'sn': '""',
            'uc3': '"vt3=F8dD2EjMFaquaXMufj0%%3D&id2=UUpgT7v9r1VNs0K1OQ%%3D%%3D&nk2=F5RAQIcpOqF0wFxodeQ%%3D&lg2=URm48syIIVrSKA%%3D%%3D"',
            'uc1': '"existShop=false&cookie21=UIHiLt3xSalX&cookie15=URm48syIIVrSKA%%3D%%3D&cookie14=UoYaiuuj%%2BPzL1g%%3D%%3D"',
            'csg': '7eb7a3f8',
            'lgc': 'tb528238846663',
            'ntm': '1',
            'cancelledSubSites': 'empty',
            't': '8109f29e8d15eacfa15b6bf648865391',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%%3D%%3D',
            'dnk': 'tb528238846663',
            'skt': '8b36eab0c8c7aa8f',
            'cookie2': '13b8dd5d51c2544c99c2393f74908b86',
            'uc4': '"nk4=0%%40FY4L7HgyQ01YvoqPicBCi%%2BYt%%2FDt9zkK2bg%%3D%%3D&id4=0%%40U2gqwARzFIUfVaMSaLM2EjsVPTSBUEzo"',
            'tracknick': 'tb528238846663',
            '_cc_': 'W5iHLLyFfA%%3D%%3D',
            '_l_g_': 'Ug%%3D%%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%%3D',
            '_tb_token_': '7e53b77b4575a',
        }

        self.ids = ""
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://s.taobao.com/search?_input_charset=utf-8&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E8%A1%A3%E6%9C%8D&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.201856.d13&ssid=s5-e&suggest_query=&tab=all&wq=',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        }

    def get_h5_tk(self, ids):
        params = {
            'jsv': '2.7.4',
            'appKey': '12574478',
            't': self.t,
            'sign': self.sign,
            'api': 'mtop.taobao.mercury.checkCollect',
            'v': '1.0',
            'needEcodeSign': 'true',
            'bizName': 'msoa.taobao.check.collect.h5',
            'sceneName': 'main_check_collect_h5',
            'timeout': '10000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp14',
            'data': f'{{"ids":"[\\"{ids}\\"]","type":"1"}}',
        }

        response = requests.get(
            'https://h5api.m.taobao.com/h5/mtop.taobao.mercury.checkcollect/1.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        )
        h5_tk = response.headers.get('Set-Cookie')
        matches = dict(re.findall(r'(_m_h5_tk(?:_enc)?)=([^;]+)', h5_tk))
        # 获取 `_m_h5_tk` 和 `_m_h5_tk_enc`，如果找不到则返回默认值
        _m_h5_tk = matches.get('_m_h5_tk', "未找到 _m_h5_tk")
        _m_h5_tk_enc = matches.get('_m_h5_tk_enc', "未找到 _m_h5_tk_enc")
        return [_m_h5_tk, _m_h5_tk_enc]


if __name__ == '__main__':
    # 使用示例
    h5_tk_extractor = H5TkExtractor()
    print(h5_tk_extractor.get_h5_tk("637706025521"))
