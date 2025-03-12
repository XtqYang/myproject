import re

import requests


class H5TkExtractor:
    def __init__(self):
        self.sign = 'd37e5e17062c5012dddfbdbb09f6af2d'
        self.t = '1741094759692'
        self.ids = ""
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
            'havana_sdkSilent': '1741832345046',
            'cna': '',
            'mtop_partitioned_detect': '1',
            'sdkSilent': '1741855380474',
            'sgcookie': 'E100X3onHcOUYDPxxenuu9EqPKbEBN999fmmPiOtWk1EfKPuhptYMR3t1fK7Fy11KUkvukFZPdR9IJD2erf0hmd9HeDsgSNdlkDeWnhMwdmAJak%3D',
            'havana_lgc2_0': 'eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiZTRhZWYyODk4NTkzZDkwZjZiYTNiNTE1ZmViNjRiZjAiLCJzaXRlIjowLCJ0b2tlbiI6IjFtUUNZT0Z6UDd0TGN2S19SLWpqQ2F3In0',
            'havana_lgc_exp': '1772873011544',
            'cookie3_bak_exp': '1742028211544',
            'unb': '2219453037520',
            'sn': '',
            'uc3': 'vt3=F8dD2EjLGxE937Kl%2Bh4%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=WqG3DMC9VAQiUQ%3D%3D',
            'csg': '587cf53a',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'skt': 'd3521e1383f59d26',
            'existShop': 'MTc0MTc2OTAxMQ%3D%3D',
            'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDT7ZfxIdQ%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVMgQQqM%2Bl',
            '_cc_': 'WqG3DMC9EA%3D%3D',
            '_l_g_': 'Ug%3D%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            'uc1': 'cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=U%2BGCWk%2F7oPIg&cookie14=UoYaiuTRq1ikAg%3D%3D&existShop=false&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D',
            '3PcFlag': '1741769015116',
            'fastSlient': '1741769015167',
            'x5sectag': '256651',
            'x5sec': '7b2274223a313734313737333532362c22733b32223a2235653738663064353963656634663164222c22617365727665723b33223a22307c434d7931786234474550536a6d744542476738794d6a45354e44557a4d444d334e5449774f7a6369436d4e6863484e736157526c646a49772b6265457867493d227d',
            'isg': 'BF1dZI4S5i1RiYEbmXFgllHJbDlXepHM5OBWxh8jubTj1n4I58rtnS8FAEpQDamE',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.taobao.com/',
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
            'api': 'mtop.relationrecommend.WirelessRecommend.recommend',
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
            # 'https://h5api.m.taobao.com/h5/mtop.taobao.mercury.checkcollect/1.0/',
            'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/',
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
