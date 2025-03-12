# 基础项目配置
BOT_NAME = "myproject"  # 项目标识，用于User-Agent和日志中
SPIDER_MODULES = ["myproject.spiders"]  # 存放爬虫的模块路径
NEWSPIDER_MODULE = "myproject.spiders"  # 用于生成新爬虫的默认位置
NODE_SCRIPT_PATH = "myproject/utils/crypto/sign_em.js"  # （需确认）可能的JS加密脚本路径，确保路径正确性

# User-Agent配置
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    # 移动端
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"

]

# 代理配置
PROXY_API = 'http://192.168.43.128:5010/get/'  # 代理池API接口地址
PROXY_POOL_URL = 'http://192.168.43.128:5010/get/'
PROXY_HEALTH_CHECK_URL = "https://www.taobao.com/help/getip.php"  # 建议改为目标域名的IP检测接口
PROXY_POOL_SIZE = 5  # 代理池容量，根据代理API性能调整（建议5-10）

# 爬虫行为配置
ROBOTSTXT_OBEY = False  # 禁用robots协议（根据目标网站合规要求决定）
LOG_LEVEL = 'INFO'  # 日志级别（调试时可设为DEBUG）
DOWNLOAD_TIMEOUT = 10  # 单请求超时时间（秒），根据网络状况调整

# 并发控制（重要优化点）
CONCURRENT_REQUESTS = 3  # 全局最大并发数（建议根据机器性能设置）
CONCURRENT_REQUESTS_PER_DOMAIN = 3  # 单域名并发上限（建议与DOWNLOAD_DELAY配合）
CONCURRENT_REQUESTS_PER_IP = 2  # 设为0禁用，避免与PER_DOMAIN冲突（除非有特殊IP限制）

# 请求频率控制
DOWNLOAD_DELAY = 2  # 基础延迟（秒），建议2-5秒
RANDOMIZE_DOWNLOAD_DELAY = True  # 启用±50%随机延迟（2±1秒）
AUTOTHROTTLE_ENABLED = True  # 启用动态限速（建议保留）
AUTOTHROTTLE_START_DELAY = 3.0  # 新增：初始延迟（建议大于DOWNLOAD_DELAY）
AUTOTHROTTLE_MAX_DELAY = 15.0  # 新增：最大延迟上限
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # 目标并发请求数（AutoThrottle 尝试动态调整到此值）
# 功能模块配置
COOKIES_ENABLED = True  # 启用Cookies（需配合中间件处理）
RETRY_ENABLED = True  # 建议启用重试（提升稳定性）
RETRY_TIMES = 2  # 新增：重试次数
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]  # 新增：需重试的状态码

# 中间件配置（优化顺序）
DOWNLOADER_MIDDLEWARES = {
    # 禁用默认中间件
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,

    # 自定义中间件（执行顺序：数字越小越早处理）
    'myproject.middlewares.RandomUserAgentMiddleware': 542,  # 优先设置UA
    'myproject.middlewares.ProxyPoolMiddleware': 543,  # 次之设置代理
    'myproject.middlewares.TaobaoMiddleware': 544,  # 最后处理业务逻辑
}

# 数据管道配置
ITEM_PIPELINES = {
    'myproject.pipelines.ElasticsearchPipeline': 300,  # ES数据存储
    # 建议添加数据验证管道：'myproject.pipelines.ValidationPipeline': 200,
}

# Elasticsearch配置（安全优化）
ES_HOSTS = ['http://192.168.43.128:9200']
ES_INDEX = 'taobao_comments_2024'  # 建议添加时间后缀（如按月份划分）
ES_USER = 'elastic'  # 建议改用环境变量读取
ES_PASSWORD = '0M*0wVJk0+9Rr7lZpjg6'  # 强烈建议使用加密存储

# 高级配置
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"  # 异步IO配置
FEED_EXPORT_ENCODING = "utf-8"  # 数据导出编码
