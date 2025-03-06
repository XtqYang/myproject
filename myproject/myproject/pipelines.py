# pipelines.py
import json
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter
from datetime import datetime
import os


class RawResponsePipeline:
    def __init__(self):
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self, spider):
        # 按时间创建存储目录
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"raw_responses/{self.timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)

        # 创建JSON文件
        self.file = open(f"{self.output_dir}/responses.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        # 转换Item为字典并导出
        adapter = ItemAdapter(item)
        self.exporter.export_item(adapter.asdict())
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()