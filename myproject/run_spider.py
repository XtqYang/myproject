# run_spider.py
from scrapy import cmdline

# 运行 Scrapy 命令

cmdline.execute(f"scrapy crawl taobao_comments".split())

