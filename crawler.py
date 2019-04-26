# General libraries
import sys
import os
import time
import json
import re

# Scrapy components
import scrapy
from scrapy.selector import Selector

# Selenium components
import selenium
from selenium import webdriver

class Crawler(scrapy.Spider):
	name = "medium_spider"
	handle_httpstatus_list = [401,400]
	
	#start_urls = ["https://medium.com/@jack/followers"]
	start_urls = ["https://medium.com/@stervy/followers"]

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		self.driver.get(response.url)
		SCROLL_PAUSE_TIME = 0.5

		# Get scroll height
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		# Half-seconds of page not scrolling
		time_out = 0
		while True:
			# Scroll down to bottom
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)

			# Calculate new scroll height and compare with last scroll height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height: # Scroll didn't happen in last half second
				time_out += 1 # Increment time out count
				self.driver.execute_script("window.scrollTo(0, " + str(new_height-int(new_height*0.05)) + ");")
				if time_out == 10: # No progress in last 5s == end of infinite scroll
					break
			else: # Reset time out
				time_out = 0
			last_height = new_height
		page_source = self.driver.page_source
		#self.driver.close()
		
		# Get the link tags (<a href...>) for each follower
		usernameLinks = Selector(text=page_source).css(".screenContent").css(".streamItem-cardInner").css(".u-flexCenter").css(".ui-captionStrong")
		usernameRe = "(?<=\\@)(.*?)(?=\\?)"
		usernameList = []
		for usernameLink in usernameLinks:
			usernameStr = re.search(usernameRe, usernameLink.css("a::attr(href)").extract_first()).group(0)
			usernameList.append(usernameStr)
		print(usernameList[0] + " | " + usernameList[len(usernameList)-1])


		#print(test[len(test)-1])

	# def parse(self, response):
	#   print(len(response.css(".screenContent").css(".streamItem-cardInner").css(".u-flexCenter").getall()))
		

		
			
	
			










