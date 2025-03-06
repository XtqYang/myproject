import json
import re

import scrapy
from scrapy import Request
from myproject.items import CommentItem
from datetime import datetime


class TaobaoSpider(scrapy.Spider):
    name = "taobao_comments"
    allowed_domains = ["h5api.m.taobao.com"]

    def __init__(self, auction_num_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auction_num_id = auction_num_id or "680107621134"  # 默认商品ID
        self.max_pages = 3  # 最大爬取页数

    def start_requests(self):
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'
        for page in range(1, self.max_pages + 1):
            yield Request(
                url=base_url,
                method='GET',
                meta={
                    'auction_num_id': self.auction_num_id,
                    'page_no': page,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response, **kwargs):
        print("响应")
        print(response.text)
        match = re.search(r'mtopjsonp\w*\((\{.*\})\)', response.text)
        if not match:
            self.logger.error("响应格式不正确")
        json_data = json.loads(match.group(1))
        rate_list = json_data.get('data', {}).get('rateList', [])
        item = CommentItem()
        item['auction_num_id'] = response.meta['auction_num_id']
        item['page_no'] = response.meta['page_no']
        item['raw_response'] = rate_list  # 存储原始响应文本
        item['timestamp'] = datetime.now().isoformat()  # 添加时间戳
        yield item
