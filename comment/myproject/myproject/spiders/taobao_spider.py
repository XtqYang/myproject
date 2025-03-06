import json
import re
import scrapy
from scrapy import Request
from myproject.items import CommentItem
from datetime import datetime


class TaobaoSpider(scrapy.Spider):
    """
    淘宝评论爬虫

    该Spider负责抓取淘宝商品评论数据，通过淘宝API获取评论列表。
    评论获取需要通过中间件处理签名等特殊请求参数。
    """
    name = "taobao_comments"
    allowed_domains = ["h5api.m.taobao.com"]

    def __init__(self, auction_num_id=None, max_pages=3, *args, **kwargs):
        """
        初始化爬虫参数

        Args:
            auction_num_id (str): 淘宝商品ID，如未提供则使用默认值
            max_pages (int): 最大爬取页数
            *args, **kwargs: 父类参数
        """
        super().__init__(*args, **kwargs)
        self.auction_num_id = auction_num_id or "680107621134"  # 默认商品ID
        self.max_pages = int(max_pages)  # 确保max_pages是整数
        self.logger.info(f"开始爬取商品 {self.auction_num_id} 的评论，计划爬取 {self.max_pages} 页")

    def start_requests(self):
        """
        生成初始请求

        为每个页码创建请求，添加必要的元数据。
        实际请求URL将由中间件处理和构建。
        """
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/'
        for page in range(1, self.max_pages + 1):
            self.logger.debug(f"创建第 {page} 页请求")
            yield Request(
                url=base_url,
                method='GET',
                meta={
                    'auction_num_id': self.auction_num_id,
                    'page_no': page,
                },
                callback=self.parse,
                dont_filter=True,  # 不过滤重复URL，因为URL会被中间件修改
                errback=self.handle_error
            )

    def parse(self, response):
        """
        解析评论数据

        从API响应中提取评论列表，并创建Item对象。

        Args:
            response: Scrapy响应对象

        Yields:
            CommentItem: 包含评论数据的Item对象
        """
        self.logger.info(f"解析第 {response.meta['page_no']} 页评论")

        try:
            # 匹配JSONP响应格式
            match = re.search(r'mtopjsonp\w*\((\{.*\})\)', response.text)
            if not match:
                self.logger.error(f"响应格式不正确: {response.text[:200]}...")
                return

            # 解析JSON数据
            json_data = json.loads(match.group(1))
            print(json_data)
            # 检查API响应状态
            api_code = json_data.get('ret', [''])[0].split('::')[0] if 'ret' in json_data and json_data['ret'] else ''
            if api_code != 'SUCCESS':
                self.logger.error(f"API返回错误: {json_data.get('ret')}")
                return

            # 提取评论列表
            rate_list = json_data.get('data', {}).get('rateList', [])
            print(rate_list)
            item = CommentItem()
            item['auction_num_id'] = response.meta['auction_num_id']
            item['page_no'] = response.meta['page_no']
            yield item

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}")
        except Exception as e:
            self.logger.error(f"解析过程中出现异常: {e}")

    def handle_error(self, failure):
        """
        处理请求失败

        记录请求失败的详细信息，便于问题排查。

        Args:
            failure: Twisted失败对象
        """
        self.logger.error(f"请求失败: {repr(failure)}")
        request = failure.request
        self.logger.error(f"失败的请求URL: {request.url}")
        self.logger.error(f"失败的请求Meta: {request.meta}")

        # 可以在这里添加重试逻辑或其他处理