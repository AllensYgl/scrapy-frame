import scrapy


class QuotesSpider(scrapy.Spider):
    name = "spider"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        # 获取网页列表的广度遍历
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)