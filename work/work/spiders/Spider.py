#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from work.items import WorkItem
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class doubanSpider(CrawlSpider):
        name = "doubanmovie"
        allowed_domains = ["movie.douban.com"]
        start_urls = ["http://movie.douban.com/top250"]
        rules = [
                Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
                Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_item"),
        ]

        def parse_item(self,response):
            sel = Selector(response)
	    movie_name = sel.select("//div[@id='content']/h1/span[1]/text()").extract()
	    movie_director = sel.select("//*[@id='info']/span[1]/span[2]/a/text()").extract()
	    movie_writer = sel.select("//*[@id='info']/span[2]/span[2]/a/text()").extract()
	    movie_score = sel.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()").extract()
	    movie_classification = sel.xpath("//span[@property='v:genre']/text()").extract()
	    movie_description_paths = sel.select("//*[@id='link-report']")
		
	    movie_description = []
	    for movie_description_path in movie_description_paths:
	    	movie_description = movie_description_path.select(".//*[@property='v:summary']/text()").extract()
			
	    movie_roles_paths = sel.select("//*[@id='info']/span[3]/span[2]")
	    movie_roles = []
	    for movie_roles_path in movie_roles_paths:
	    	movie_roles = movie_roles_path.select(".//*[@rel='v:starring']/text()").extract()

	    movie_detail = sel.select("//*[@id='info']").extract()
	

	    item = WorkItem()
	    item['movie_name'] = ''.join(movie_name).strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';')
	    item['movie_director'] = movie_director[0].strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';') if len(movie_director) > 0 else ''
	    item['movie_score'] = movie_score[0].strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';') if len(movie_director) > 0 else ''
	    item['movie_classification'] = movie_classification[0].strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';') if len(movie_director) > 0 else ''
	    item['movie_description'] = movie_description[0].strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';') if len(movie_description) > 0 else ''
	    item['movie_writer'] = ';'.join(movie_writer).strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';')
	    item['movie_roles'] = ';'.join(movie_roles).strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';')
		
		
	    movie_detail_str = ''.join(movie_detail).strip()
			
	    movie_language_str = ".*语言:</span>(.+?)<span.*".decode("utf8")
	    movie_date_str = ".*上映日期:</span> <span property=\"v:initialReleaseDate\" content=\"(\S+?)\">(\S+?)</span>.*".decode("utf8")
	    movie_long_str = ".*片长:</span> <span property=\"v:runtime\" content=\"(\d+).*".decode("utf8")
	  	
	    pattern_language =re.compile(movie_language_str,re.S)
	    pattern_date = re.compile(movie_date_str,re.S)
	    pattern_long = re.compile(movie_long_str,re.S)
					

	    movie_language = re.search(pattern_language,movie_detail_str)
	    movie_date = re.search(pattern_date,movie_detail_str)
	    movie_long = re.search(pattern_long,movie_detail_str)

	    item['movie_language'] = ""
	    if movie_language:
	    	item['movie_language'] = movie_language.group(1).replace('<br>','').strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';')
			
	    item['movie_date'] = ""
	    if movie_date:
		item['movie_date'] = movie_date.group(1).strip().replace(',',';').replace('\'','\\\'').replace('\"','\\\"').replace(':',';')
			
	    item['movie_long'] = ""
	    if movie_long:
		item['movie_long'] = movie_long.group(1)

	    yield item
