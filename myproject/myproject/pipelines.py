# pipelines.py 修改后的 Elasticsearch 管道类
import logging
from itemadapter import ItemAdapter
from datetime import datetime
from elasticsearch import Elasticsearch, exceptions
from elasticsearch import helpers

class ElasticsearchPipeline:
    def __init__(self):
        self.es = None
        self.index_name = "taobao_comments"  # 更明确的索引名称
        self.bulk_actions = []
        self.bulk_size = 500  # 调整为更合理的批量大小
        self.doc_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self, spider):
        """初始化 Elasticsearch 连接并创建索引"""
        try:
            self.es = Elasticsearch(
                hosts=["https://192.168.43.128:9200"],
                basic_auth=("elastic", "0M*0wVJk0+9Rr7lZpjg6"),
                verify_certs=False,
                ssl_show_warn=False
            )
            if not self.es.ping():
                raise exceptions.ConnectionError("无法连接到 Elasticsearch")
            spider.logger.info("成功连接到 Elasticsearch")

            # 创建索引（如果不存在）并更新映射
            if not self.es.indices.exists(index=self.index_name):
                self._create_index(spider)
            else:
                self._update_mapping(spider)

        except exceptions.ConnectionError as e:
            spider.logger.error(f"连接失败: {str(e)}")
            raise

    def _create_index(self, spider):
        """创建包含更完善映射的索引"""
        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "auction_num_id": {"type": "keyword"},
                    "page_no": {"type": "integer"},
                    "raw_response": {
                        "type": "object",
                        "dynamic": True  # 允许自动检测嵌套字段
                    },
                    "timestamp": {
                        "type": "date",
                        "format": "strict_date_optional_time||epoch_millis"
                    }
                }
            }
        }
        try:
            self.es.indices.create(
                index=self.index_name,
                body=mapping,
                ignore=400
            )
            spider.logger.info(f"成功创建索引 {self.index_name}")
        except exceptions.RequestError as e:
            spider.logger.error(f"创建索引失败: {str(e)}")

    def _update_mapping(self, spider):
        """更新现有索引的映射（如果需要）"""
        try:
            self.es.indices.put_mapping(
                index=self.index_name,
                body={
                    "properties": {
                        "raw_response": {
                            "type": "object",
                            "dynamic": True
                        }
                    }
                },
                ignore=400
            )
        except exceptions.RequestError as e:
            spider.logger.warning(f"更新映射失败: {str(e)}")

    def process_item(self, item, spider):
        """处理并缓存 Item"""
        adapter = ItemAdapter(item)
        doc = adapter.asdict()

        # 生成唯一文档ID（添加时间戳防止覆盖）
        doc_id = (
            f"{doc['auction_num_id']}_"
            f"{doc['page_no']}_"
            f"{doc['timestamp'].split('.')[0].replace(':', '-')}"
        )

        self.bulk_actions.append({
            "_op_type": "index",
            "_index": self.index_name,
            "_id": doc_id,
            "_source": doc
        })

        # 批量插入条件
        if len(self.bulk_actions) >= self.bulk_size:
            self._bulk_insert(spider)

        return item

    def _bulk_insert(self, spider):
        """执行批量插入并处理错误"""
        try:
            success, errors = helpers.bulk(
                self.es,
                self.bulk_actions,
                stats_only=False,
                raise_on_error=False
            )

            # 记录成功数量
            self.doc_count += success
            spider.logger.info(f"成功插入 {success} 文档，累计 {self.doc_count} 条")

            # 处理错误
            if errors:
                error_count = len(errors)
                spider.logger.error(f"批量插入失败 {error_count} 条")
                for error in errors[:5]:  # 记录前5个错误详情
                    error_info = error.get('index', {})
                    spider.logger.error(
                        f"文档ID: {error_info.get('_id')} | "
                        f"状态: {error_info.get('status')} | "
                        f"错误类型: {error_info.get('error', {}).get('type')} | "
                        f"错误原因: {error_info.get('error', {}).get('reason')}"
                    )

            # 清空缓存
            self.bulk_actions = []

        except Exception as e:
            spider.logger.error(f"批量插入异常: {str(e)}")
            self.bulk_actions = []

    def close_spider(self, spider):
        """关闭时提交剩余数据"""
        if self.bulk_actions:
            self._bulk_insert(spider)
        if self.es:
            self.es.close()
            spider.logger.info(f"关闭连接，总计插入 {self.doc_count} 条数据")