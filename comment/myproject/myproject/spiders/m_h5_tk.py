import re

import requests
from functools import lru_cache


class H5TkExtractor:
    def __init__(self):
        self.sign = 'd37e5e17062c5012dddfbdbb09f6af2d'
        self.t = '1741094759692'
        self.ids = ""
        self.cookies = {
            'cna': 'FxR3H2WkqwUCAbRbsI99XbR5',
            'thw': 'cn',
            'tfstk': 'gHAt0vm5gDmGcDUUgoMhn8lCPK0nEILZdh87iijghHKpxFFMInx0MtspPVSi3A-vpntFIGOcsIFAvhNcI1sgknLVvO0woArYMMtViGji7iavAEtA3VScciKDld0nZbYw7s5XD0coZchGZ6KTfR6jlM_5502qaSGy7s5jxyVjEbLwV96aNd_fR2QcoPwXcOsQOaIC5i66cM6CPaq1GstjJ6_PuPa1CsZIOM7fGitfGAm3Wi41DSpq_4jpi0l7MSddWOIviMFAEBVldgNOx7F-oNBTpFsLGSOpK_K1nGMz-i5GbF790bPN1tpXs6OsAj1WUHdAF_Hm7_OwlLJX8l3Afexww1O-X5bhHGpB19UbGUT1v9pvXceNfdxdUw6Qkb7HqMTw1p34AFtlX1_CKbgJRt9H_TRiA5CWUFfMh3i3IG9RlgoMZQQmxujRoRgKJ-yVCw895Tw9aPcCnwIo-J2439bFJg0KJ-yVCw7dq2233-Wh8',
            't': '67b05d17a37c35cb6ae723fb2bb2e6ea',
            '_tb_token_': 'f3e657fa10eee',
            '_samesite_flag_': 'true',
            'cookie2': '1f8db2010899859f7ae746c37c3e4ab9',
            'wk_cookie2': '16d3a798cbf114b38ff160f1765ef328',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'lgc': 'tb528238846663',
            'cancelledSubSites': 'empty',
            'dnk': 'tb528238846663',
            'tracknick': 'tb528238846663',
            'ariaDefaultTheme': 'default',
            'ariaFixed': 'true',
            'ariaScale': '1',
            'ariaMousemode': 'true',
            '3PcFlag': '1741063745713',
            'sgcookie': 'E100u1S%2BGl7sm0p6MlOfwWKPx5TSaYJFIHNTSn1PAJVGNWXR%2BMdrX8O2nIU99N1LGujvH0v1%2BXlOpunQGVLVoRotSJdnaqqDaUo7vg%2BcP2OcSpY%3D',
            'unb': '2219453037520',
            'uc1': 'cookie21=VFC%2FuZ9aj3yE&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&cookie14=UoYaiuNDpQqbsA%3D%3D&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&pas=0',
            'uc3': 'id2=UUpgT7v9r1VNs0K1OQ%3D%3D&vt3=F8dD2E8bey%2FMF9ThvrU%3D&lg2=UIHiLt3xD8xYTw%3D%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D',
            'csg': '865d7563',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'skt': '7b49ba586a4ccefd',
            'existShop': 'MTc0MTA2MzkzNQ%3D%3D',
            'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDOvXOpAmQ%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVNR4bEqrr',
            '_cc_': 'VT5L2FSpdA%3D%3D',
            '_l_g_': 'Ug%3D%3D',
            'sg': '308',
            '_nk_': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            'ariaReadtype': '1',
            'ariaoldFixedStatus': 'false',
            'ariaStatus': 'false',
            'mtop_partitioned_detect': '1',
            '_m_h5_tk_enc': '2f78eec9caddf8c0aac80dc039dfddef',
            'isg': 'BJ6eNwbCdQ_b9KJmbjRTow6U7zTgX2LZi22120gmC-Hcaz5Fse8-6EkFY_fnyFrx',
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
        _m_h5_tk = matches.get('_m_h5_tk', "未找到 _m_h5_tk")
        _m_h5_tk_enc = matches.get('_m_h5_tk_enc', "未找到 _m_h5_tk_enc")
        return [_m_h5_tk, _m_h5_tk_enc]

    # def refresh_cookies(self):
    #     """模拟登录获取最新cookie（需根据实际情况实现）"""
    #     session = requests.Session()
    #     login_url = 'https://login.taobao.com'
    #     # 这里需要添加实际的登录逻辑
    #     return {
    #         'cna': '更新后的cookie值',
    #         # ...其他cookie字段
    #     }


if __name__ == '__main__':
    # 使用示例
    h5_tk_extractor = H5TkExtractor()
    print(h5_tk_extractor.get_h5_tk("637706025521"))
