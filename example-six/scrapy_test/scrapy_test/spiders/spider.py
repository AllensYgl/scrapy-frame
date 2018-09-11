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
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
     # 获取网页列表的深度遍历
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page) #把取到的页面再次放入队列中进行爬取
            yield scrapy.Request(next_page, callback=self.parse)