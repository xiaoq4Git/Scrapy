#!/usr/bin/env python
# coding=utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import DmozItem

class DmozSpider(BaseSpider):
        name = "dmoz"
        allowed_domains = ["movie.douban.com"]
        start_urls = [
      #      "http://movie.douban.com/annual2015/#2"
      #      "http://movie.douban.com/annual2015/#3"
      #      "http://movie.douban.com/chart"
            u"http://movie.douban.com/review/best/"
        ]

        def parse(self, response):
            test = HtmlXPathSelector(response)
       #     sites = test.xpath("//div[@class='subjects-wrapper clearfix']")
            sites = test.xpath("//ul[@class='tlst clearfix']/li[@class='ilst']")
            for site in sites:
                item = DmozItem()
                item['title'] = site.xpath('a/@title').extract()
   #             item['link'] = site.xpath('a/@href').extract()
   #             item['desc'] = site.xpath('text()').extract()
 #               items.append(item)
            return item
