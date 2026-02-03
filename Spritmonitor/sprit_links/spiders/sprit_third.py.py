import scrapy
from scrapy import Request
from numpy import random
from time import sleep
import re
from ..items import SpritLinksItem , SpritTableItem

class SpritCharSpider(scrapy.Spider):
    rate = 0.5
    #def __init__(self):
       # self.download_delay = 1/float(self.rate)
    sleeptime = random.uniform(1,1.5)
    sleep(sleeptime)
    print("sleeping for:", sleeptime, "seconds")
    
    print("sleeping is over")
    custom_settings = {
            'COOKIES_ENABLED': False,
            'CONCURRENT_REQUESTS': 2,
            'DOWNLOAD_DELAY': 2,
            'ROTATED_PROXY_ENABLED' : True
            }	

    name = 'sprit_third'
    allowed_domains = ['www.spritmonitor.de']
    with open("C:\\Users\\KPA5367\\sprit_link_final_text.txt") as f:
        start_urls = [url.strip() for url in f.readlines()]
        

    
    
    def requests (self,response):
        r = Request(url=self.start_urls,callback=self.parse,headers=())
        yield r
        
    
    def parse(self, response):
        s_item = SpritLinksItem()
        t_item = SpritTableItem()

        next_page = response.xpath('//*[@id="content-left"]/div[7]/a[last()]/@href').extract()
        #######################STRING FILTER######################
        def scrape_filter (string,prev_str,next_str):   #saves the value between 2 strings 
            y = re.search(prev_str + '(.*)' + next_str,string)
            new_val = y.group(1)
            return new_val
        def string_filter(text):  #removes ' ', '\n','\t' from data
            text = text.replace(' ' , '').replace('\t','').replace('\n','')
        ##########################################################
        id_ex = response.css('#navilinks')
        ID=id_ex.xpath ('//*[@id="navilinks"]/text()').extract()[1].replace (" > Vehicle",'').replace("\t",'').strip()
        Title=  response.css('#vehicledetails h1::text').get()
        Description=response.xpath('//*[@id="vehicledetails"]/text()[2]').get()
        Avg_FC= response.css('td strong::text').get()
        dist_driven =response.xpath('//*[@id="content-left"]/table/tr/td[6]//text()').get().replace(' ','').replace('\n','').replace('\t','')
        s_item['ID'] = ID
        s_item['Title'] = Title
        s_item['Description'] = Description
        s_item['Avg_FC'] =  Avg_FC
        s_item['dist_driven'] = dist_driven
       
        
        table  = response.css ('#content-left > div.itemtable_wrapper > table')
        date = response.css('#content-left > div.itemtable_wrapper > table > tbody > tr > td.fueldate ::text').getall()

        for i in range(len(date)):
            Date= table.css(' td.fueldate ::text').extract()[i]
            Odometer = table.css('td.fuelkmpos').extract()[i]
            Distance = table.css('td.trip').extract()[i]
            Refuel_Quantity = table.css('td.quantity').extract()[i]
            Refuel_Type = table.css('td.fuelsort ::attr(onmouseover)').extract()[i]
            FC = table.css('td.consumption').extract()[i]
            t_item['Date']= Date
            t_item['Odometer'] = scrape_filter(Odometer,'<td class="fuelkmpos">','</td>')
            t_item['Distance'] = scrape_filter(Distance,'    \t\t  \n    \t\t        \t\t    \t','    \t\t        \t\t</td')
            t_item['Refuel_Quantity'] = scrape_filter(Refuel_Quantity, '\n    \t\t        \t\t    \t', '    \t\t        \t\t</td')
            t_item['Refuel_Type'] = scrape_filter(Refuel_Type,'showTooltip(', ')')
            t_item['FC'] = scrape_filter(FC,'<td class="consumption" onmouseover="showTooltip',' l/100km')
        yield s_item
        yield t_item
            


        if next_page:
            next_url = ''.join(map(str, next_page)) 
            yield response.follow(next_url, callback=self.parse)