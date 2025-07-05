import re
import requests


class H5TkExtractor:
    def __init__(self):
        self.sign = 'd37e5e17062c5012dddfbdbb09f6af2d'
        self.t = '1741094759692'
        self.ids = ""
        self.cookies = cookies = {
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
            'x5sec': '7b2274223a313734313739313931322c22733b32223a2234646636613734386433313635623464222c22617365727665723b33223a22307c434b5046787234474549662b76507a392f2f2f2f2f774561447a49794d546b304e544d774d7a63314d6a41374f43494b59324677633278705a4756324d6a44357434544741673d3d227d',
            'mtop_partitioned_detect': '1',
            '_m_h5_tk_enc': 'db62d6bb065c78df9dc8003b534577e6',
            'isg': 'BMDAvfV2s1JSr0xM_OJVuRzqkU6SSaQTOWNbcTpRjFtvtWDf4ll0o5aDzZ11Hlzr',
        }
        self.headers = headers = {
            'accept': 'text/event-stream, text/event-stream',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://s.taobao.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://s.taobao.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        }

    def get_h5_tk(self, ids):
        params = {
            'dataType': 'stream',
            'method': 'post',
            'api': 'mtop.relationrecommend.wirelessrecommend.recommendstream',
            'v': '1.0',
            'timeout': '60000',
            'experimental': '[object Object]',
            'subDomain': 'm',
            'jsv': '0.0.1',
            'appKey': '12574478',
            't': self.t,
            'sign': self.sign,
            'xAcceptStream': 'true',
            'data': '{"appId":"44124","params":"{\\"appId\\":\\"44124\\",\\"requestType\\":\\"aiNavigation\\",\\"data\\":\\"{\\\\\\"query\\\\\\":\\\\\\"%E8%A1%A3%E6%9C%8D\\\\\\",\\\\\\"searchParams\\\\\\":\\\\\\"{\\\\\\\\\\\\\\"device\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"HMA-AL00\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"isBeta\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"grayHair\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"from\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"nt_history\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"brand\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"HUAWEI\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"info\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"wifi\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"index\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"4\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"rainbow\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"schemaType\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"auction\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"elderHome\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"isEnterSrpSearch\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"true\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"newSearch\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"network\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"wifi\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"subtype\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"hasPreposeFilter\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"prepositionVersion\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"v2\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"client_os\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"Android\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"gpsEnabled\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"searchDoorFrom\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"srp\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"debug_rerankNewOpenCard\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"homePageVersion\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"v7\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"searchElderHomeOpen\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"false\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"search_action\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"initiative\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"sugg\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"_4_1\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"sversion\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"13.6\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"style\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"list\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"ttid\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"600000@taobao_pc_10.7.0\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"needTabs\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"true\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"areaCode\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"CN\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"vm\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"nw\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"countryNum\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"156\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"m\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"pc\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"page\\\\\\\\\\\\\\":1,\\\\\\\\\\\\\\"n\\\\\\\\\\\\\\":48,\\\\\\\\\\\\\\"q\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"%E8%A1%A3%E6%9C%8D\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"qSource\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"url\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"pageSource\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"a21bo.jianhua/a.201856.d13\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"tab\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"all\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"pageSize\\\\\\\\\\\\\\":48,\\\\\\\\\\\\\\"totalPage\\\\\\\\\\\\\\":100,\\\\\\\\\\\\\\"totalResults\\\\\\\\\\\\\\":4800,\\\\\\\\\\\\\\"sourceS\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"0\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"sort\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"_coefp\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"bcoffset\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"ntoffset\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"filterTag\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"service\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"prop\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"loc\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"start_price\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"end_price\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"startPrice\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"endPrice\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"itemIds\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"p4pIds\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"p4pS\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"categoryp\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"ha3Kvpairs\\\\\\\\\\\\\\":null,\\\\\\\\\\\\\\"myCNA\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"\\\\\\\\\\\\\\"}\\\\\\",\\\\\\"llm\\\\\\":null}\\"}"}',
        }

        response = requests.get(
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
