# pipelines.py
import json
import os
from datetime import datetime

from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter


class RawResponsePipeline:
    """
    原始响应数据管道

    将爬取的数据以JSON格式保存到指定目录。
    每次爬取会创建一个基于时间戳的新目录，避免数据覆盖。
    """

    def __init__(self):
        """初始化管道"""
        self.file = None
        self.exporter = None
        self.item_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        """
        从crawler创建管道实例

        Args:
            crawler: Scrapy crawler对象

        Returns:
            管道实例
        """
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self, spider):
        """
        爬虫启动时的处理

        创建输出目录和文件

        Args:
            spider: 爬虫实例
        """
        # 创建基于时间戳的目录名
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"raw_responses/{self.timestamp}_{spider.name}_{spider.auction_num_id}"

        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        spider.logger.info(f"创建输出目录: {self.output_dir}")

        # 创建并初始化JSON导出器
        self.file = open(f"{self.output_dir}/responses.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

        # 记录爬虫参数到元数据文件
        with open(f"{self.output_dir}/metadata.json", 'w', encoding='utf-8') as f:
            json.dump({
                'spider_name': spider.name,
                'auction_num_id': spider.auction_num_id,
                'max_pages': spider.max_pages,
                'start_time': self.timestamp,
            }, f, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        """
        处理单个数据项

        将数据项导出到JSON文件

        Args:
            item: 爬虫生成的数据项
            spider: 爬虫实例

        Returns:
            处理后的数据项
        """
        # 转换Item为字典并导出
        adapter = ItemAdapter(item)
        self.exporter.export_item(adapter.asdict())

        # 记录处理的数据项数量
        self.item_count += 1
        if self.item_count % 10 == 0:  # 每处理10个项目记录一次日志
            spider.logger.info(f"已处理 {self.item_count} 条数据")

        return item

    def close_spider(self, spider):
        """
        爬虫关闭时的处理

        完成数据导出，关闭文件

        Args:
            spider: 爬虫实例
        """
        self.exporter.finish_exporting()
        self.file.close()

        # 记录爬取完成信息
        spider.logger.info(f"爬取完成，共处理 {self.item_count} 条数据")
        with open(f"{self.output_dir}/metadata.json", 'r+', encoding='utf-8') as f:
            metadata = json.load(f)
            metadata.update({
                'end_time': datetime.now().strftime("%Y%m%d_%H%M%S"),
                'item_count': self.item_count,
            })
            f.seek(0)
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 如果需要，可以在这里添加数据处理或转换逻辑