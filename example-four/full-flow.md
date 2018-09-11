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
