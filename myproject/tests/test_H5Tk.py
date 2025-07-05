from urllib.parse import urlparse

url = 'https://h5api.m.taobao.com/h5/mtop.taobao.mercury.checkcollect/1.0/'
path_parts = urlparse(url).path.split('/')  # 拆分路径
api_value = path_parts[2] if len(path_parts) > 3 else None
print(api_value)
