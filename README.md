# scrapy使用教程


---
### 安装
> ###### python -m pip install Scrapy

### 生成框架

> #### scrapy startproject tutorial


```python
tutorial/
    scrapy.cfg            # 部署配置文件

    tutorial/             # 项目内容
        __init__.py

        items.py          # 项目的items定义文件

        middlewares.py    # 项目中间件

        pipelines.py      # 项目管道

        settings.py       # 项目设置

        spiders/          # 爬虫文件
            __init__.py
```

### 分析scrapy.Spider类



```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```



> ##### name:每个爬虫的唯一标识

> ##### start_requests():一个URL队列，迭代其中的网页（类似广度遍历）

> ##### parse():处理得到的页面内容逻辑（通常用来提取页面内容保存为dicts的字典类型）

> ##### TextResponse: 用来保存页面的内容

#### 运行爬虫
> ##### scrapy crawl quotes


---


#### 实现通过shell+CSS实现内容筛选

##### 执行命令

> ##### scrapy shell "http://quotes.toscrape.com/page/1/"

```golang
response.css("标签名") //进行筛选
response.css('标签名::text').extract() //提取文本内容
.extract() //得到一个列表

.extract_first() //得到第一条结果
response.css('title::text')[0].extract() //两者功能类似

response.css('title::text').re(r'Q\w+')//通过正则提取
```
##### 更多内容:URL[https://docs.scrapy.org/en/latest/intro/tutorial.html#creating-a-project](https://docs.scrapy.org/en/latest/intro/tutorial.html#creating-a-project)

##### 注：可使用
##### Firebug([https://docs.scrapy.org/en/latest/topics/firefox.html#topics-firefox](https://docs.scrapy.org/en/latest/topics/firefox.html#topics-firefox))进行抓取和使用
##### Firefox([https://docs.scrapy.org/en/latest/topics/firefox.html#topics-firefox](https://docs.scrapy.org/en/latest/topics/firefox.html#topics-firefox))进行部分的抓取

#### XPath选择器


```
response.xpath('//title')

response.xpath('//title/text()').extract_first()
```
##### 更多内容:URL[https://docs.scrapy.org/en/latest/topics/selectors.html#topics-selectors](https://docs.scrapy.org/en/latest/topics/selectors.html#topics-selectors)



---


### 让我们来完成一个完整流程(shell版本)

##### 在shell运行scrapy

> ##### scrapy shell 'http://quotes.toscrape.com'


```python

scrapy shell 'http://quotes.toscrape.com'


response.css("div.quote")
quote = response.css("div.quote")[0]
title = quote.css("span.text::text").extract_first()
title
#......context

author = quote.css("small.author::text").extract_first()
author
#...context

tags = quote.css("div.tags a.tag::text").extract()
tags
#....context...

for quote in response.css("div.quote"):
     text = quote.css("span.text::text").extract_first()
     author = quote.css("small.author::text").extract_first()
     tags = quote.css("div.tags a.tag::text").extract()
     print(dict(text=text, author=author, tags=tags))

#.....context

```


### Python版本


> ##### scrapy startproject scrapy_test

myspider.py


```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "spider"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```



> ##### scrapy crawl spider



```
2018-09-11 15:29:00 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': '“I like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.”', 'author': 'Dr. Seuss', 'tags':
['fantasy']}
2018-09-11 15:29:00 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': '“I may not have gone where I intended to go, but I think I have ended up where I needed to be.”', 'author': 'Douglas Adams', 'tags': ['life', 'navigation']}
2018-09-11 15:29:00 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': "“The opposite of love is not hate, it's indifference. The opposite of art is not ugliness, it's indifference. The opposite of
faith is not heresy, it's indifference. And the opposite of life is not death, it's indifference.”", 'author': 'Elie Wiesel', 'tags': ['activism', 'apathy', 'hate', 'indifference', 'inspirational', 'love', 'opposite', 'philosophy']}
2018-09-11 15:29:00 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
//.........
```

#### 导出数据

> ##### scrapy crawl spider -o spider.json


```json
[
{"text": "\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d", "author": "Albert Einstein", "tags": ["change", "deep-thoughts", "thinking", "world"]},
{"text": "\u201cIt is our choices, Harry, that show what we truly are, far more than our abilities.\u201d", "author": "J.K. Rowling", "tags": ["abilities", "choices"]},
{"text": "\u201cThere are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.\u201d", "author": "Albert Einstein", "tags": ["inspirational", "life", "live", "miracle", "miracles"]},
{"text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d", "author": "Jane Austen", "tags": ["aliteracy", "books", "classic", "humor"]},
{"text": "\u201cImperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.\u201d", "author": "Marilyn Monroe", "tags": ["be-yourself", "inspirational"]},
{"text": "\u201cTry not to become a man of success. Rather become a man of value.\u201d", "author": "Albert Einstein", "tags": ["adulthood", "success", "value"]},
{"text": "\u201cIt is better to be hated for what you are than to be loved for what you are not.\u201d", "author": "Andr\u00e9 Gide", "tags": ["life", "love"]},
{"text": "\u201cI have not failed. I've just found 10,000 ways that won't work.\u201d", "author": "Thomas A. Edison", "tags": ["edison", "failure", "inspirational", "paraphrased"]},
{"text": "\u201cA woman is like a tea bag; you never know how strong it is until it's in hot water.\u201d", "author": "Eleanor Roosevelt", "tags": ["misattributed-eleanor-roosevelt"]},
{"text": "\u201cA day without sunshine is like, you know, night.\u201d", "author": "Steve Martin", "tags": ["humor", "obvious", "simile"]},
{"text": "\u201cThis life is what you make it. No matter what, you're going to mess up sometimes, it's a universal truth. But the good part is you get to decide how you're going to mess it up. Girls will be your friends - they'll act like it anyway. But just remember, some come, some go. The ones that stay with you through everything - they're your true best friends. Don't let go of them. Also remember, sisters make the best friends in the world. As for lovers, well, they'll come and go too. And baby, I hate to say it, most of them - actually pretty much all of them are going to break your heart, but you can't give up because if you give up, you'll never find your soulmate. You'll never find that half who makes you whole and that goes for everything. Just because you fail once, doesn't mean you're gonna fail at everything. Keep trying, hold on, and always, always, always believe in yourself, because if you don't, then who will, sweetie? So keep your head high, keep your chin up, and most importantly, keep smiling, because life's a beautiful thing and there's so much to smile about.\u201d", "author": "Marilyn Monroe", "tags": ["friends", "heartbreak", "inspirational", "life", "love", "sisters"]},
{"text": "\u201cIt takes a great deal of bravery to stand up to our enemies, but just as much to stand up to our friends.\u201d", "author": "J.K. Rowling", "tags": ["courage", "friends"]},
{"text": "\u201cIf you can't explain it to a six year old, you don't understand it yourself.\u201d", "author": "Albert Einstein", "tags": ["simplicity", "understand"]},
{"text": "\u201cYou may not be her first, her last, or her only. She loved before she may love again. But if she loves you now, what else matters? She's not perfect\u2014you aren't either, and the two of you may never be perfect together but if she can make you laugh, cause you to think twice, and admit to being human and making mistakes, hold onto her and give her the most you can. She may not be thinking about you every second of the day, but she will give you a part of her that she knows you can break\u2014her heart. So don't hurt her, don't change her, don't analyze and don't expect more than she can give. Smile when she makes you happy, let her know when she makes you mad, and miss her when she's not there.\u201d", "author": "Bob Marley", "tags": ["love"]},
{"text": "\u201cI like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.\u201d", "author": "Dr. Seuss", "tags": ["fantasy"]},
{"text": "\u201cI may not have gone where I intended to go, but I think I have ended up where I needed to be.\u201d", "author": "Douglas Adams", "tags": ["life", "navigation"]},
{"text": "\u201cThe opposite of love is not hate, it's indifference. The opposite of art is not ugliness, it's indifference. The opposite of faith is not heresy, it's indifference. And the opposite of life is not death, it's indifference.\u201d", "author": "Elie Wiesel", "tags": ["activism", "apathy", "hate", "indifference", "inspirational", "love", "opposite", "philosophy"]},
{"text": "\u201cIt is not a lack of love, but a lack of friendship that makes unhappy marriages.\u201d", "author": "Friedrich Nietzsche", "tags": ["friendship", "lack-of-friendship", "lack-of-love", "love", "marriage", "unhappy-marriage"]},
{"text": "\u201cGood friends, good books, and a sleepy conscience: this is the ideal life.\u201d", "author": "Mark Twain", "tags": ["books", "contentment", "friends", "friendship", "life"]},
{"text": "\u201cLife is what happens to us while we are making other plans.\u201d", "author": "Allen Saunders", "tags": ["fate", "life", "misattributed-john-lennon", "planning", "plans"]}
]
```

---

### 提取网页链接

> ##### 提取该内容链接
```
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```
> ##### response.css('li.next a').extract_first()


```
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
```

> ##### response.css('li.next a::attr(href)').extract_first()


```
'/page/2/'
```



---

### 循环提取
> ##### 深度优先


```python
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
```

> ##### 广度优先


```python
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
```


---

### 执行命令的传参操作
> ##### 传参内容参考URL[:https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs](https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs)


----
###### 编著人：Allen guo
###### 日期：  2018/9/11
