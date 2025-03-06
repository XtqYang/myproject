# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#
import scrapy


# CommentItem类是一个数据容器，用于规范化和存储从淘宝商品评论中提取的结构化数据。

class CommentItem(scrapy.Item):
    """
    auction_num_id	字符串/数字	淘宝商品的唯一数字标识ID	"653962244590"
    page_no	整型	评论所在的分页页码	2
    title	字符串	评论标题（需注意淘宝评论通常无标题，可能需要移除该字段）	"质量超好！"
    content	字符串	用户撰写的详细评论文本	"衣服质量不错，会回购"
    user_id	字符串	发表评论用户的唯一标识	"tbuser_123456"
    raw_response	字符串	原始API响应数据（用于调试和容错处理）	JSON格式的原始响应文本
    rating	整型	用户给出的星级评分（淘宝一般为1-5星）	5
    timestamp	时间戳	评论发表时间或爬取时间（建议使用ISO格式）	"2025-03-05T10:23:45.123456"
    """
    auction_num_id = scrapy.Field()
    page_no = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    user_id = scrapy.Field()
    raw_response = scrapy.Field()  # 必须包含这个字段
    rating = scrapy.Field()
    timestamp = scrapy.Field()
