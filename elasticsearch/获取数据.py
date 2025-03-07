from elasticsearch import Elasticsearch
from pprint import pprint  # 用于美化输出嵌套结构


class ElasticsearchClient:
    """Elasticsearch 客户端操作封装类"""

    def __init__(self, hosts, basic_auth, index, verify_certs=False, ssl_show_warn=False):
        """
        初始化Elasticsearch连接客户端

        :param hosts: ES集群地址列表
        :param basic_auth: 基础认证信息 (用户名, 密码)
        :param index: 默认操作的索引名称
        :param verify_certs: 是否验证SSL证书
        :param ssl_show_warn: 是否显示SSL警告
        """
        self.es = Elasticsearch(
            hosts=hosts,
            basic_auth=basic_auth,
            verify_certs=verify_certs,
            ssl_show_warn=ssl_show_warn
        )
        self.default_index = index

    def check_connection(self):
        """检查与Elasticsearch集群的连接状态"""
        try:
            return self.es.ping()
        except Exception as e:
            print(f"连接异常: {str(e)}")
            return False

    def execute_search(self, query_body=None, size=100):
        """
        执行搜索查询

        :param query_body: 自定义查询DSL，默认使用基础查询
        :param size: 返回文档数量
        :return: 查询结果字典
        """
        # 默认查询：获取按时间倒序排列的文档
        if query_body is None:
            query_body = {
                "query": {"match_all": {}},
                "sort": [{"timestamp": {"order": "desc"}}]
            }

        try:
            return self.es.search(
                index=self.default_index,
                body=query_body,
                size=size
            )
        except Exception as e:
            raise RuntimeError(f"查询执行失败: {str(e)}")

    @staticmethod
    def parse_results(response, max_display=50):
        """
        解析并展示查询结果

        :param response: ES查询响应结果
        :param max_display: 最大展示文档数量
        """
        # 解析基础信息
        total = response['hits']['total']['value']
        print(f"\n找到 {total} 条匹配记录")

        # 展示前N条记录的概要信息
        print(f"\n前{max_display}条结果概要：")
        for hit in response['hits']['hits'][:max_display]:
            source = hit['_source']
            print(f"\n文档ID: {hit['_id']}")
            print(f"页码: {source.get('page_no', 'N/A')}")
            print(f"商品ID: {source.get('auction_num_id', 'N/A')}")
            print(f"抓取时间: {source.get('timestamp', 'N/A')}")

            # 展示原始响应中的部分内容
            if 'raw_response' in source:
                print("原始响应摘要:")
                pprint(source['raw_response'], depth=1)  # 限制嵌套层级展示

        # 大数据量提示
        if total > 100:
            print("\n注意: 数据量超过100条，建议使用scroll API处理大数据集")


def main():
    # 配置参数
    es_config = {
        "hosts": ["https://192.168.43.128:9200"],
        "basic_auth": ("elastic", "0M*0wVJk0+9Rr7lZpjg6"),
        "index": "taobao_comments",
        "verify_certs": False,
        "ssl_show_warn": False
    }

    try:
        # 初始化客户端
        es_client = ElasticsearchClient(**es_config)

        # 检查连接状态
        if not es_client.check_connection():
            print("连接失败，请检查网络和认证配置")
            return

        print("成功连接到Elasticsearch集群")

        # 执行基础查询
        response = es_client.execute_search(size=100)

        # 解析并展示结果
        es_client.parse_results(response, max_display=50)

    except Exception as e:
        print(f"程序执行异常: {str(e)}")


if __name__ == "__main__":
    main()