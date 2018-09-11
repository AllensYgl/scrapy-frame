
```golang
response.css("标签名") //进行筛选
response.css('标签名::text').extract() //提取文本内容
.extract() //得到一个列表

.extract_first() //得到第一条结果
response.css('title::text')[0].extract() //两者功能类似

response.css('title::text').re(r'Q\w+')//通过正则提取

//XPath
response.xpath('//title')

response.xpath('//title/text()').extract_first()
```