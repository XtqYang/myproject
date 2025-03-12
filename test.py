import requests

# 定义请求的 URL
params = {
    "jsv": "2.7.4",
    "appKey": "12574478",
    "t": "1741747744019",
    "sign": "574e625c007f27db20461de5ec3c4272",
    "api": "mtop.taobao.rate.detaillist.get",
    "v": "6.0",
    "isSec": "0",
    "ecode": "1",
    "timeout": "20000",
    "type": "jsonp",
    "dataType": "jsonp",
    "jsonpIncPrefix": "pcdetail",
    "callback": "mtopjsonppcdetail25",
    "data": '{"showTrueCount":false,"auctionNumId":"769361086770","pageNo":1,"pageSize":20,"rateType":"","searchImpr":"-8","orderType":"","expression":"","rateSrc":"pc_rate_list"}'
}

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://h5.m.taobao.com/",
    "Origin": "https://h5.m.taobao.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

# 定义 Cookie
cookies = {
    "_samesite_flag_": "true",
    "cookie2": "17af0ee9c37ba35e43e3ca54a8cebd2f",
    "t": "20c1b8c96e003a04455d570c7d82bc72",
    "_tb_token_": "58e33aa81eba5",
    "thw": "cn",
    "_hvn_lgc_": "0",
    "cookie3_bak": "17af0ee9c37ba35e43e3ca54a8cebd2f",
    "wk_cookie2": "151177e5c67f84d11997af48b49e9de2",
    "wk_unb": "UUpgT7v9r1VNs0K1OQ%3D%3D",
    "lgc": "tb528238846663",
    "cancelledSubSites": "empty",
    "env_bak": "FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5",
    "dnk": "tb528238846663",
    "tracknick": "tb528238846663",
    "sgcookie": "E100EukvQfosjPXXEQdYSGhLUS9oUZf4Uzz%2FhykDpSfFfRJDzmSS8gSSSL4xDCezKLksA2YLV6HroKqr2HrA%2BaoLzIC0dlK752fN31BmZeevMKo%3D",
    "havana_lgc2_0": "eyJoaWQiOjIyMTk0NTMwMzc1MjAsInNnIjoiODcxNTZhYzE2NTk3ZjU3MGNjZjZlZDNlMTUyYmU4YmMiLCJzaXRlIjowLCJ0b2tlbiI6IjFNOWVNSzhUSGhkVXhPWndtQkZlRlh3In0",
    "havana_lgc_exp": "1772730920811",
    "cookie3_bak_exp": "1741886120812",
    "uc3": "lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dD2EjKML%2BJUk1PXv0%3D&nk2=F5RAQIcpOqF0wFxodeQ%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D",
    "csg": "16ac354f",
    "skt": "30456cdcabcd41ba",
    "existShop": "MTc0MTYyNjkyMA%3D%3D",
    "uc4": "id4=0%40U2gqwARzFIUfVaMSaLM2EjsVMwls%2FYrV&nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDWmQ7bHpQ%3D%3D",
    "_cc_": "UIHiLt3xSw%3D%3D",
    "x5sec": "7b2274223a313734313734353934322c22733b32223a2261653836646632373139343538653138222c22617365727665723b33223a22307c43492f6577373447454f664a784b6342476738794d6a45354e44557a4d444d334e5449774f7a4569436d4e6863484e736157526c646a49772b6265457867493d227d",
    "mtop_partitioned_detect": "1",
    "sdkSilent": "1741832345046",
    "havana_sdkSilent": "1741832345046",
    "3PcFlag": "1741746140697",
    "_m_h5_tk": "828ecc200313ebd1afc79991df7a1f0f_1741755663102",
    "_m_h5_tk_enc": "6a1ed09cf0a18d151424a27e71cb7adf"
}
url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'

# 发送 GET 请求
response = requests.get(url, params=params, headers=headers, cookies=cookies)

# 输出响应内容
print(response.text)
