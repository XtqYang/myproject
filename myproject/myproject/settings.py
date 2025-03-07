BOT_NAME = "myproject"
SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"
NODE_SCRIPT_PATH = "sign_em.js"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
]
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'INFO'
# 配置 Scrapy 执行的最大并发请求数（默认值：16）
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.5  # 增加间隔
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
AUTOTHROTTLE_ENABLED = True  # 启用自动限速
COOKIES_ENABLED = True  # 启用自动Cookie处理
# TELNETCONSOLE_ENABLED = False
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }
# SPIDER_MIDDLEWARES = {
#    "myproject.middlewares.MyprojectSpiderMiddleware": 543,
# }
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.TaobaoMiddleware': 543,  # 543 是优先级，数字越小优先级越高
    # 禁用默认的 ProxyMiddleware
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}
PROXY = "http://127.0.0.1:8080"
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 30
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }
ITEM_PIPELINES = {
    'myproject.pipelines.ElasticsearchPipeline': 300,
}
# Elasticsearch 配置
ES_HOSTS = ['http://192.168.43.128:9200']  # ES 服务器地址
ES_INDEX = 'taobao_comments'  # 索引名称
ES_USER = 'elastic'
ES_PASSWORD = '0M*0wVJk0+9Rr7lZpjg6'
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
