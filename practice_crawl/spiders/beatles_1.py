import re
import time
import scrapy
from practice_crawl.items import SongCrawlItem

from bs4 import BeautifulSoup

class Beatles1Spider(scrapy.Spider):
    name = 'Beatles1'
    allowed_domains = ['lyrics.az']
    start_urls = ['https://lyrics.az/the-beatles/allsongs.html']

    def parse(self, response):

        for song in response.css('tbody').css('tr'):
            item = SongCrawlItem()
            song_title = song.css('a::text').extract_first()
            item['title'] = song_title
            song_path = song.css('a::attr(href)').extract_first()
            print(song_title)
            song_url = song_path
            print(song_url)
            print('aaaaaa')
            # 1秒間停止する
            time.sleep(1)
            yield scrapy.Request(
                song_url,
                callback=self.parse_lyrics,
                meta={'item': item}
            )

    def parse_lyrics(self, response):
       # 歌詞自体を抽出する
       print('bbbbbbbbb')
       item = response.meta['item']
       item['url'] = response.url

       # text
       text = response.css('.song-lyrics').extract_first()
       soup = BeautifulSoup(text, 'html')
       print(text)
       song_lyrics = soup.getText()

       # テキストのクリーニング
       song_lyrics = song_lyrics

       # 歌詞
       print(song_lyrics)
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