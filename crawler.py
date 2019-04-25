import scrapy
import json
import selenium
from selenium import webdriver
import time

class Crawler(scrapy.Spider):
	name = "medium_spider"
	handle_httpstatus_list = [401,400]
	
	start_urls = ["https://medium.com/@jack/followers"]

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		self.driver.get(response.url)
		SCROLL_PAUSE_TIME = 1.0

		# Get scroll height
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
			# Scroll down to bottom
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)

			# Calculate new scroll height and compare with last scroll height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height
		page_source = self.driver.page_source
		self.driver.close()
		print(page_source)

	# def parse(self, response):
	#   print(len(response.css(".screenContent").css(".streamItem-cardInner").css(".u-flexCenter").getall()))
		

		
			
	
			










