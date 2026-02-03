import scrapy
from scrapy import Request
from numpy import random
from time import sleep
 			

class SpritCharSpider(scrapy.Spider):
    rate = 0.5
    #def __init__(self):
       # self.download_delay = 1/float(self.rate)
    
    custom_settings = {
            'COOKIES_ENABLED': False,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 2,
            'ROTATED_PROXY_ENABLED' : True
            }	

    name = 'sprit_char'
    allowed_domains = ['www.spritmonitor.de']
    with open("C:\\Users\\KPA5367\\sprit_link_final_text.txt") as f:
        start_urls = [url.strip() for url in f.readlines()]
    
    
    def requests (self,response):
        r = Request(url=self.start_urls,callback=self.parse,headers=())
        yield r
        
    
    def parse(self, response):
        sleeptime = random.uniform(2, 3.5)
        print("sleeping for:", sleeptime, "seconds")
        sleep(sleeptime)
        print("sleeping is over")
        yield {
            'ID': str(response.url.replace('https://www.spritmonitor.de/en/detail/','').replace('.html','')),
            'Title':str(response.css('#vehicledetails h1::text').get()),
            'Description': str(response.xpath('//*[@id="vehicledetails"]/text()[2]').get()),
            'Avg_FC':response.css('td strong::text').get(),
            
            'Odometer': response.css('td.fuelkmpos::text').getall(),
            'Distance': response.css('td.trip::text').getall(),
            'Refuel_Quantity':response.css('td.quantity::text').getall(),
            'Refuel_Type':response.css('td.fuelsort ::attr(onmouseover)').getall(),
            'FC': response.css(' td.consumption > b::text').getall(),
            
            }
        
      
        
      
        
      
        
      
        
      
        
      # next_page = response.xpath('//*[@id="content-left"]/div[7]/a[last()]/@href').get()
        
  