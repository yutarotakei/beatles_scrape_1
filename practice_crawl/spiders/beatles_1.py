import re
import time
import scrapy
from practice_crawl.items import SongCrawlItem

from bs4 import BeautifulSoup

class Beatles1Spider(scrapy.Spider):
    name = 'Beatles1'
    allowed_domains = ['j-lyric.net']
    start_urls = ['https://j-lyric.net/artist/a04d22c/']

    def parse(self, response):

        for song in response.css('#ly1'):
            item = SongCrawlItem()
            song_title = song.css('a::text').extract_first()
            item['title'] = song_title
            pattern = r'/artist/'
            song_path = song.css('a::attr(href)').extract_first()
            print(song_path)
            if re.search(pattern, song_path):
                print('aaaaaaaaaaaaaaaaaaaaa')
                song_url = 'http://' + self.allowed_domains[0] + song_path
                # 1秒間停止する
                time.sleep(1)

                yield scrapy.Request(
                    song_url,
                    callback=self.parse_lyrics,
                    meta={'item': item}
                )

    def parse_lyrics(self, response):
       # 歌詞自体を抽出する
       item = response.meta['item']
       item['url'] = response.url

       # text
       text = response.css('#Lyric').extract_first()
       soup = BeautifulSoup(text, 'html')
       song_lyrics = soup.getText()

       # テキストのクリーニング
       song_lyrics = song_lyrics

       # 歌詞
       item['lyric'] = song_lyrics
       yield item

    def text_cleaning(self, text):
       song_lyrics = text.replace('\n', '')
       song_lyrics = song_lyrics.replace(' ', '')

       # 英数字の排除
       song_lyrics = re.sub(r'[a-zA-Z0-9]', '', song_lyrics)
       # 記号の排除
       song_lyrics = re.sub(
           r'[ ＜＞♪`''“”・…_!?!-/:-@[-`{-~]', '', song_lyrics
       )

       return song_lyrics