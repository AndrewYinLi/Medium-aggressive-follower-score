import scrapy
import json

class Crawler(scrapy.Spider):
	name = "medium_spider"
	handle_httpstatus_list = [401,400]
	
	start_urls = ["https://medium.com/@andrewyinli/followers"]

	def parse(self, response):
		print(len(response.css(".screenContent").css(".streamItem-cardInner").getall()))
			
	
			










