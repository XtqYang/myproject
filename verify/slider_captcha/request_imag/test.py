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
    'cna': 'Bn1NIIRCWV8BASQKQs0iQwHG',
    'isg': 'BMnJK-piyq2IFbTeErUYFtOs2PUjFr1IrO15O2s8D7DvsuLEs2eSGJGk9JYE8VWA',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://h5api.m.tmall.com//h5/mtop.taobao.pcdetail.data.get/1.0/_____tmd_____/punish?x5secdata=xde49f70ad088a37dc2bed62b782d82750a89fe4eedd255d9d1742018760a-717315356a683744249abaac3en2219453037520kcapslidev2__bx__h5api.m.tmall.com%3A443%2Fh5%2Fmtop.taobao.pcdetail.data.get%2F1.0&x5step=2&action=captchacapslidev2&pureCaptcha=',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'lid=tb528238846663; cookie3_bak=17af0ee9c37ba35e43e3ca54a8cebd2f; env_bak=FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5; wk_unb=UUpgT7v9r1VNs0K1OQ%3D%3D; wk_cookie2=151177e5c67f84d11997af48b49e9de2; cookie3_bak_exp=1742114742462; havana_lgc_exp=1772965846161; _l_g_=Ug%3D%3D; lgc=tb528238846663; cookie1=BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D; login=true; cookie2=17af0ee9c37ba35e43e3ca54a8cebd2f; cancelledSubSites=empty; sg=308; sn=; _tb_token_=58e33aa81eba5; dnk=tb528238846663; uc3=nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dD2EjME%2BYP7XAx3uc%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D; tracknick=tb528238846663; uc4=nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDt%2Fh4xCoA%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVPTbtaxjC; unb=2219453037520; cookie17=UUpgT7v9r1VNs0K1OQ%3D%3D; _nk_=tb528238846663; sgcookie=E1004cA73k5ovrB%2Fi1Jh%2BTylMpULGEILR8V6W7QrMRyavuHgtP5mGQktvgNtNfs4UxblrFTOCGdQeM7eOM0bWYzT1kVya8eRXRGwKiC0wjYXNYk%3D; t=20c1b8c96e003a04455d570c7d82bc72; csg=1107a33b; havana_sdkSilent=1741952221075; cna=Bn1NIIRCWV8BASQKQs0iQwHG; isg=BMnJK-piyq2IFbTeErUYFtOs2PUjFr1IrO15O2s8D7DvsuLEs2eSGJGk9JYE8VWA',
}

params = {
    'token': '2bed62b782d82750a89fe4eedd255d9d',
    'appKey': 'X82Y__d366b44467147323c70b42d8a2d852f5',
    'x5secdata': 'xde49f70ad088a37dc2bed62b782d82750a89fe4eedd255d9d1742018760a-717315356a683744249abaac3en2219453037520kcapslidev2__bx__h5api.m.tmall.com:443/h5/mtop.taobao.pcdetail.data.get/1.0',
    'language': 'cn',
    'v': '09273032060834112',
}

response = requests.get(
    'https://h5api.m.tmall.com/h5/mtop.taobao.pcdetail.data.get/1.0/_____tmd_____/newslidecaptcha',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.text)


