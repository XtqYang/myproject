import requests

cookies = {
    'cookie2': '17af0ee9c37ba35e43e3ca54a8cebd2f',
    't': '20c1b8c96e003a04455d570c7d82bc72',
    '_tb_token_': '58e33aa81eba5',
    'thw': 'cn',
    '_hvn_lgc_': '0',
    'wk_cookie2': '151177e5c67f84d11997af48b49e9de2',
    'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
    'lgc': 'tb528238846663',
    'cancelledSubSites': 'empty',
    'dnk': 'tb528238846663',
    'tracknick': 'tb528238846663',
    'cna': 'GolZIM8I01MBASQKQs0CK2jW',
    'sn': '',
    '_samesite_flag_': 'true',
    '3PcFlag': '1742969558582',
    'sgcookie': 'E100aqQ9zY7Cd5lyKpGRSjVMkuN1h1N9Tmt6xM2SFc03cPN0u94eaxOwsF6DekMrnCLoQkoI%2BoPT%2FQDQb88DmA3aHghKGJ6pb1mnNhBIhiYGPT8%3D',
    'havana_lgc2_0': 'eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiMDM2NjE2MWIyMGU4NzBiMTQ2MGExOTgzNzE1NjNkZWIiLCJzaXRlIjowLCJ0b2tlbiI6IjEyMDMzWVN3VTR3OXZ6Yk5JT1hiWXBRIn0',
    'havana_lgc_exp': '1774073569083',
    'cookie3_bak': '17af0ee9c37ba35e43e3ca54a8cebd2f',
    'cookie3_bak_exp': '1743228769083',
    'unb': '2219453037520',
    'uc1': 'existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie21=WqG3DMC9Eman&pas=0&cookie14=UoYaibnatzyfKg%3D%3D',
    'uc3': 'vt3=F8dD2EnoKtvgwvLMgkY%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D&lg2=URm48syIIVrSKA%3D%3D',
    'csg': '69f10b74',
    'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
    'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
    'skt': '094dae581673270f',
    'existShop': 'MTc0Mjk2OTU2OQ%3D%3D',
    'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FxqYu8enGQ%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsWMsqt61vw',
    '_cc_': 'V32FPkk%2Fhw%3D%3D',
    '_l_g_': 'Ug%3D%3D',
    'sg': '308',
    '_nk_': 'tb528238846663',
    'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
    'isg': 'BAYG-st4nfLXG0q-NjxLazYsV_yIZ0ohl0zmYvAvoSkU86cNWPXjMHmKzi8_v0I5',
    'mtop_partitioned_detect': '1',
    'sdkSilent': '1743320468273',
    'havana_sdkSilent': '1743320468273',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://item.taobao.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'cookie2=17af0ee9c37ba35e43e3ca54a8cebd2f; t=20c1b8c96e003a04455d570c7d82bc72; _tb_token_=58e33aa81eba5; thw=cn; _hvn_lgc_=0; wk_cookie2=151177e5c67f84d11997af48b49e9de2; wk_unb=UUpgT7v9r1VNs0K1OQ%3D%3D; lgc=tb528238846663; cancelledSubSites=empty; dnk=tb528238846663; tracknick=tb528238846663; cna=GolZIM8I01MBASQKQs0CK2jW; sn=; _samesite_flag_=true; 3PcFlag=1742969558582; sgcookie=E100aqQ9zY7Cd5lyKpGRSjVMkuN1h1N9Tmt6xM2SFc03cPN0u94eaxOwsF6DekMrnCLoQkoI%2BoPT%2FQDQb88DmA3aHghKGJ6pb1mnNhBIhiYGPT8%3D; havana_lgc2_0=eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiMDM2NjE2MWIyMGU4NzBiMTQ2MGExOTgzNzE1NjNkZWIiLCJzaXRlIjowLCJ0b2tlbiI6IjEyMDMzWVN3VTR3OXZ6Yk5JT1hiWXBRIn0; havana_lgc_exp=1774073569083; cookie3_bak=17af0ee9c37ba35e43e3ca54a8cebd2f; cookie3_bak_exp=1743228769083; unb=2219453037520; uc1=existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie21=WqG3DMC9Eman&pas=0&cookie14=UoYaibnatzyfKg%3D%3D; uc3=vt3=F8dD2EnoKtvgwvLMgkY%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D&lg2=URm48syIIVrSKA%3D%3D; csg=69f10b74; env_bak=FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5; cookie17=UUpgT7v9r1VNs0K1OQ%3D%3D; skt=094dae581673270f; existShop=MTc0Mjk2OTU2OQ%3D%3D; uc4=nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FxqYu8enGQ%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsWMsqt61vw; _cc_=V32FPkk%2Fhw%3D%3D; _l_g_=Ug%3D%3D; sg=308; _nk_=tb528238846663; cookie1=BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D; isg=BAYG-st4nfLXG0q-NjxLazYsV_yIZ0ohl0zmYvAvoSkU86cNWPXjMHmKzi8_v0I5; mtop_partitioned_detect=1; sdkSilent=1743320468273; havana_sdkSilent=1743320468273',
}

params = {
    'jsv': '2.7.4',
    'appKey': '12574478',
    't': '1743236858557',
    'sign': 'de80f510755b4d3aecc00b39d9eb91ad',
    'api': 'mtop.taobao.rate.detaillist.get',
    'v': '6.0',
    'isSec': '0',
    'ecode': '1',
    'timeout': '20000',
    'type': 'jsonp',
    'dataType': 'jsonp',
    'jsonpIncPrefix': 'pcdetail',
    'callback': 'mtopjsonppcdetail21',
    'data': '{"showTrueCount":false,"auctionNumId":"728865743739","pageNo":3,"pageSize":20,"rateType":"","searchImpr":"-8","orderType":"","expression":"","rateSrc":"pc_rate_list"}',
}

response = requests.get(
    'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/',
    params=params,
    cookies=cookies,
    headers=headers,
)