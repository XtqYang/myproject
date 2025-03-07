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
        self.auction_num_id = auction_num_id or "769361086770"
        self.max_pages = 50

    def start_requests(self):
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'
        for page in range(1, self.max_pages + 1):
            print(f"正在执行第{page}条数据")
            yield Request(
                url=base_url,
                method='GET',
                meta={'auction_num_id': self.auction_num_id, 'page_no': page},
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response, **kwargs):
        # 提取 JSONP 数据
        match = re.search(r'mtopjsonp\w*\((\{.*\})\)', response.text)
        if not match:
            self.logger.error("响应格式不正确")
            return
        try:
            json_data = json.loads(match.group(1))
        except json.JSONDecodeError:
            self.logger.error("JSON 解析失败")
            return
        # 提取需要存储的核心数据
        item = CommentItem()
        item['auction_num_id'] = response.meta['auction_num_id']
        item['page_no'] = response.meta['page_no']
        item['raw_response'] = json_data.get('data', {})  # 存储完整data字段
        item['timestamp'] = datetime.now().isoformat()

        yield item
