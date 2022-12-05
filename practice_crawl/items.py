# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongCrawlItem(scrapy.Item):
    title = scrapy.Field()  # 曲のタイトル
    url = scrapy.Field()  # 曲のURL
    lyric = scrapy.Field()  # 歌詞
