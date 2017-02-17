#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 第一个版本
# import scrapy
# class QuotesSpider(scrapy.Spider):
# 	name = "quotes"

# 	def start_requests(self):
# 		urls = [
# 			'http://quotes.toscrape.com/page/1/',
#             'http://quotes.toscrape.com/page/2/',
# 		]
# 		for url in urls:
# 			yield scrapy.Request(url=url, callback=self.parse)

# 	def parse(self, response):
# 		page = response.url.split('/')[-2]
# 		filename = 'quotes-%s.html' % page
# 		with open(filename, 'wb') as f:
# 			f.write(response.body)
# 		self.log('Saved file %s' % filename)


#第二个版本，简化start_request,迭代打印抓取的内容
# import scrapy
# class QuotesSpider(scrapy.Spider):
# 	name = 'quotes'
# 	start_urls = [
# 		'http://quotes.toscrape.com/page/1/',
#         'http://quotes.toscrape.com/page/2/',
# 	]

# 	def parse(self, response):
# 		for quote in response.css('div.quote'):
# 			yield {
# 				'text':	quote.css('span.text::text').extract_first(),
# 				'author': quote.css('small.author::text').extract_first(),
# 				'tags': quote.css('div.tags a.tag::text').extract()
# 			}

#第三个版本，自动翻页爬取
import scrapy
class QuoteSpider(scrapy.Spider):
	name = 'quotes'
	start_urls = [
		'http://quotes.toscrape.com/page/1/',
	]

	def parse(self, response):
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first(),
				'tags':	quote.css('div.tags a.tag::text').extract(),
			}

		next_page = response.css('li.next a::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

# 第四个版本
import scrapy
class AuthorSpider(scrapy.Spider):
	name = 'author'
	start_urls = ['http://quotes.toscrape.com/']

	def parse(self, response):
		for href in response.css('.author + a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href), callback=self.parse_author)

		next_page = response.css('li.next a::sttr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

	def parse_author(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip()

		yield {
			'name': extract_with_css('h3.author-title::text'),
			'birthdate': extract_with_css('.author-born-date::text'),
			'bio': extract_with_css('.author-description::text'),
		}
