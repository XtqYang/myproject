import unittest
from scrapy.http import HtmlResponse
from your_project.spiders.my_spider import MySpider


class TestMySpider(unittest.TestCase):
    def setUp(self):
        # 初始化爬虫实例
        self.spider = MySpider()

    def _load_test_response(self, filename):
        # 从本地文件加载测试用 HTML 响应
        with open(f"tests/sample_data/{filename}", "r", encoding="utf-8") as f:
            content = f.read()
        return HtmlResponse(
            url="http://example.com",
            body=content.encode("utf-8"),
            encoding="utf-8"
        )

    def test_parse(self):
        # 测试 parse 方法
        response = self._load_test_response("sample_page.html")
        results = list(self.spider.parse(response))

        # 断言返回的 Item 数量
        self.assertEqual(len(results), 3)

        # 检查第一个 Item 的字段
        first_item = results[0]
        self.assertEqual(first_item["title"], "Example Title")
        self.assertIn("2023-10-01", first_item["date"])

    def test_next_page_request(self):
        # 测试是否生成下一页请求
        response = self._load_test_response("sample_page.html")
        results = list(self.spider.parse(response))

        # 查找是否有 Request 对象
        requests = [r for r in results if isinstance(r, Request)]
        self.assertTrue(len(requests) > 0)

        next_request = requests[0]
        self.assertEqual(next_request.url, "http://example.com/page2")