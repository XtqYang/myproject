import requests

cookies = {
    'lid': 'tb528238846663',
    'cookie3_bak': '17af0ee9c37ba35e43e3ca54a8cebd2f',
    'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
    'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
    'wk_cookie2': '151177e5c67f84d11997af48b49e9de2',
    'cookie3_bak_exp': '1742114742462',
    'havana_lgc_exp': '1772965846161',
    '_l_g_': 'Ug%3D%3D',
    'lgc': 'tb528238846663',
    'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
    'login': 'true',
    'cookie2': '17af0ee9c37ba35e43e3ca54a8cebd2f',
    'cancelledSubSites': 'empty',
    'sg': '308',
    'sn': '',
    '_tb_token_': '58e33aa81eba5',
    'dnk': 'tb528238846663',
    'uc3': 'nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dD2EjME%2BYP7XAx3uc%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D',
    'tracknick': 'tb528238846663',
    'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDt%2Fh4xCoA%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVPTbtaxjC',
    'unb': '2219453037520',
    'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
    '_nk_': 'tb528238846663',
    'sgcookie': 'E1004cA73k5ovrB%2Fi1Jh%2BTylMpULGEILR8V6W7QrMRyavuHgtP5mGQktvgNtNfs4UxblrFTOCGdQeM7eOM0bWYzT1kVya8eRXRGwKiC0wjYXNYk%3D',
    't': '20c1b8c96e003a04455d570c7d82bc72',
    'csg': '1107a33b',
    'havana_sdkSilent': '1741952221075',
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '36ea4f80e768db811787e2cd63bf723f_1741942085014',
    '_m_h5_tk_enc': '6a9d917e5d8ecfd6f8c1b48d3d5514c5',
    'cna': 'Bn1NIIRCWV8BASQKQs0iQwHG',
    'x5sectag': '400787',
    'x5sec': '7b2274223a313734313933383638392c22733b32223a2264366666633861663138663332616438222c22617365727665723b33223a22307c434f792f7a373447454b476c71706743476841794d6a45354e44557a4d444d334e5449774f7a45354967646a623235755a574e304d506d33684d5943227d',
    'isg': 'BC4ueFC8xcrUYTMvQTxn15Blf4TwL_IpjxQ-6lj1VDHsO8uVwL96OUh48yfX-OpB',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://detail.tmall.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'lid=tb528238846663; cookie3_bak=17af0ee9c37ba35e43e3ca54a8cebd2f; env_bak=FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5; wk_unb=UUpgT7v9r1VNs0K1OQ%3D%3D; wk_cookie2=151177e5c67f84d11997af48b49e9de2; cookie3_bak_exp=1742114742462; havana_lgc_exp=1772965846161; _l_g_=Ug%3D%3D; lgc=tb528238846663; cookie1=BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D; login=true; cookie2=17af0ee9c37ba35e43e3ca54a8cebd2f; cancelledSubSites=empty; sg=308; sn=; _tb_token_=58e33aa81eba5; dnk=tb528238846663; uc3=nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dD2EjME%2BYP7XAx3uc%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D; tracknick=tb528238846663; uc4=nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDt%2Fh4xCoA%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVPTbtaxjC; unb=2219453037520; cookie17=UUpgT7v9r1VNs0K1OQ%3D%3D; _nk_=tb528238846663; sgcookie=E1004cA73k5ovrB%2Fi1Jh%2BTylMpULGEILR8V6W7QrMRyavuHgtP5mGQktvgNtNfs4UxblrFTOCGdQeM7eOM0bWYzT1kVya8eRXRGwKiC0wjYXNYk%3D; t=20c1b8c96e003a04455d570c7d82bc72; csg=1107a33b; havana_sdkSilent=1741952221075; mtop_partitioned_detect=1; _m_h5_tk=36ea4f80e768db811787e2cd63bf723f_1741942085014; _m_h5_tk_enc=6a9d917e5d8ecfd6f8c1b48d3d5514c5; cna=Bn1NIIRCWV8BASQKQs0iQwHG; x5sectag=400787; x5sec=7b2274223a313734313933383638392c22733b32223a2264366666633861663138663332616438222c22617365727665723b33223a22307c434f792f7a373447454b476c71706743476841794d6a45354e44557a4d444d334e5449774f7a45354967646a623235755a574e304d506d33684d5943227d; isg=BC4ueFC8xcrUYTMvQTxn15Blf4TwL_IpjxQ-6lj1VDHsO8uVwL96OUh48yfX-OpB',
}

params = {
    'jsv': '2.7.4',
    'appKey': '12574478',
    't': '1741938711880',
    'sign': 'accad7c600f57f1bff5b06bfe0bdeeed',
    'api': 'mtop.taobao.rate.detaillist.get',
    'v': '6.0',
    'isSec': '0',
    'ecode': '1',
    'timeout': '20000',
    'type': 'jsonp',
    'dataType': 'jsonp',
    'jsonpIncPrefix': 'pcdetail',
    'callback': 'mtopjsonppcdetail16',
    'data': '{"showTrueCount":false,"auctionNumId":"894921485965","pageNo":1,"pageSize":20,"rateType":"","searchImpr":"-8","orderType":"","expression":"","rateSrc":"pc_rate_list"}',
}


for i in range(19):
    response = requests.get(
        'https://h5api.m.tmall.com/h5/mtop.taobao.rate.detaillist.get/6.0/',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.text)
    # time.sleep(3)
