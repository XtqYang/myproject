import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
import aiofiles
from urllib.parse import urljoin


class AsyncCrawler:
    def __init__(self, base_url, concurrency=10, timeout=10):
        self.base_url = base_url
        self.concurrency = concurrency  # 最大并发数
        self.timeout = ClientTimeout(total=timeout)  # 超时设置
        self.semaphore = asyncio.Semaphore(concurrency)  # 并发信号量
        self.seen_urls = set()  # 已爬取的 URL 去重

    async def fetch(self, session: ClientSession, url: str):
        """异步请求页面"""
        try:
            async with self.semaphore:  # 控制并发量
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"请求失败: {url} 状态码 {response.status}")
                        return None
        except (ClientError, asyncio.TimeoutError) as e:
            print(f"请求异常: {url} - {str(e)}")
            return None

    async def parse(self, html: str, url: str):
        """解析页面（示例：提取链接）"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if link not in self.seen_urls:
                links.add(link)
        return links

    async def save_data(self, data: str):
        """异步保存数据到文件"""
        async with aiofiles.open('output.txt', 'a', encoding='utf-8') as f:
            await f.write(data + '\n')

    async def crawl(self, session: ClientSession, url: str):
        """爬取单个页面的完整流程"""
        html = await self.fetch(session, url)
        if not html:
            return
        # 解析并存储数据
        await self.save_data(f"URL: {url}\nContent: {html[:100]}...")

    async def run(self):
        """启动爬虫"""
        # 创建一个异步 HTTP 客户端会话（ClientSession）。
        # async with 确保会话结束后自动关闭连接，避免资源泄漏
        async with aiohttp.ClientSession() as session:
            # 初始任务
            await self.crawl(session, self.base_url)


if __name__ == "__main__":
    crawler = AsyncCrawler(
        base_url="https://freeproxyupdate.com/",  # 目标网站
        concurrency=20,  # 并发数
        timeout=15  # 超时时间（秒）
    )
    asyncio.run(crawler.run())
