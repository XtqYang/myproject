import re

import requests
from functools import lru_cache


class H5TkExtractor:
    def __init__(self):
        self.sign = 'd37e5e17062c5012dddfbdbb09f6af2d'
        self.t = '1741094759692'
        self.ids = ""
        self.cookies = {
            'mtop_partitioned_detect': '1',
            '_samesite_flag_': 'true',
            'cookie2': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            't': '20c1b8c96e003a04455d570c7d82bc72',
            '_tb_token_': '58e33aa81eba5',
            'thw': 'cn',
            '3PcFlag': '1741588158513',
            'sgcookie': 'E100%2F3tX3pKiqc6whFudxlW5aKRzsZaOI0bes86DYucXBMvSSV25gClqiUjn%2BcAhJWPfLq4Pxz5kVhA5kKdXvuTNHX%2FgNLv7gfAgohc6cC4nniw%3D',
            'havana_lgc2_0': 'eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiNzA5MzkxNDhkOGNmZmNlYTIwNzAwZWViZDA5ZTE4YmEiLCJzaXRlIjowLCJ0b2tlbiI6IjFfcmdPUG5OeWxMNWlLMU12ZWp1UXRnIn0',
            '_hvn_lgc_': '0',
            'havana_lgc_exp': '1772692173956',
            'cookie3_bak': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            'cookie3_bak_exp': '1741847373956',
            'wk_cookie2': '151177e5c67f84d11997af48b49e9de2',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'unb': '2219453037520',
            'uc1': 'cookie14=UoYaiuZTr2HPQg%3D%3D&existShop=false&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=W5iHLLyFfoaZ',
            'uc3': 'id2=UUpgT7v9r1VNs0K1OQ%3D%3D&vt3=F8dD2EjJrbF7Be4ozYw%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D',
            'csg': '23c53e0c',
            'lgc': 'tb528238846663',
            'cancelledSubSites': 'empty',
            'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'dnk': 'tb528238846663',
            'skt': 'a112d729cbd4d32a',
            'existShop': 'MTc0MTU4ODE3Mw%3D%3D',
            'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDbroXhLuA%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVMI7tupYH',
            'tracknick': 'tb528238846663',
            '_cc_': 'VT5L2FSpdA%3D%3D',
            '_l_g_': 'Ug%3D%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            '_m_h5_tk_enc': '6beb17d8e189bb7b42de3183ca30b127',
            'isg': 'BHFxDh1ass54mh3f1ZW0GsVlgP0LXuXQ8JwqglOF1zgfepHMmq-roN6UnI4cqX0I',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&q=%E8%A1%A3%E6%9C%8D&search_type=item&sourceId=tb.index&spm=a21bo.jianhua%2Fa.201856.d13&ssid=s5-e&tab=all',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        }

    @lru_cache(maxsize=1000)
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
        _m_h5_tk = matches.get('_m_h5_tk')
        _m_h5_tk_enc = matches.get('_m_h5_tk_enc')
        return [_m_h5_tk, _m_h5_tk_enc]

if __name__ == '__main__':
    # 使用示例
    h5_tk_extractor = H5TkExtractor()
    print(h5_tk_extractor.get_h5_tk("637706025521"))


