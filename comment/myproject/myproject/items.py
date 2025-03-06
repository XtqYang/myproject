# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#
import scrapy


class CommentItem(scrapy.Item):
    """
    淘宝商品评论数据模型

    定义评论数据的各个字段及其含义

    Fields:
        auction_num_id (str): 淘宝商品的唯一数字标识ID
        page_no (int): 评论所在的分页页码
        title (str): 评论标题（淘宝评论通常无标题）
        content (str): 用户撰写的详细评论文本
        user_id (str): 发表评论用户的唯一标识
        raw_response (dict): 原始API响应数据（用于调试和容错处理）
        rating (int): 用户给出的星级评分（1-5星）
        timestamp (str): 评论爬取时间（ISO格式）
    """
    auction_num_id = scrapy.Field()  # 商品ID: "653962244590"
    page_no = scrapy.Field()  # 页码: 2
    title = scrapy.Field()  # 标题: "质量超好！"（通常为空）
    content = scrapy.Field()  # 内容: "衣服质量不错，会回购"
    user_id = scrapy.Field()  # 用户ID: "tbuser_123456"
    raw_response = scrapy.Field()  # 原始数据（必须包含）
    rating = scrapy.Field()  # 评分: 5（1-5星）
    timestamp = scrapy.Field()  # 时间戳: "2025-03-05T10:23:45.123456"