import scrapy
from scrapy import Request
from numpy import random
from time import sleep
import re
from ..items import   SpritLinksItem
import csv


class SpritCharSpider(scrapy.Spider):
    rate = 0.5

    custom_settings = {
            'COOKIES_ENABLED': False,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 2,
            'FEEDS' : {'data/%(name)s/%(name)s_%(time)s.csv':{'format': 'csv'}
            }
        }	

    name = 'sprit_second'
    allowed_domains = ['www.spritmonitor.de']
    with open("C:\\Users\\KPA5367\\sprit_link_final_text.txt") as f:
        start_urls = [url.strip() for url in f.readlines()]


    
    
    def requests (self,response):
        r = Request(url=self.start_urls,dont_filter=False,callback=self.parse,headers=())
        #Random sleep between requests
        sleeptime = random.uniform(1,1.5)
        sleep(sleeptime)
        print("sleeping for:", sleeptime, "seconds")
        
        print("sleeping is over")
        yield r
        
    
    def parse(self, response):
        #Define Items
        s_item = SpritLinksItem()
###########################################################################STRING FILTER######################
        def scrape_filter (string,prev_str,next_str):   #saves the value between 2 strings 
            y = re.search(prev_str + '(.*)' + next_str,string)
            new_val = y.group(1)
            return new_val
        def string_filter(text):  #removes ' ', '\n','\t' from data
            text = text.replace(' ' , '').replace('\t','').replace('\n','')
        
##############################################################################################################
##############################################################################################################
        check = response.url
        c = re.search('.html' +'(.*)' + '',check)
        c1 = c.group(1)
        if   c1 =='':
        
            ID =str(response.url.replace('https://www.spritmonitor.de/en/detail/','').replace('.html','')),
            Title = str(response.css('#vehicledetails h1::text').get()),
            Description = str(response.xpath('//*[@id="vehicledetails"]/text()[2]').get()),
 
            Avg_FC = response.css('td strong::text').get()
            s_item['ID'] = ID
            s_item['Title'] = Title
            s_item['Description'] =Description
            s_item['Avg_FC'] = Avg_FC
            s_item['Title'] = Title
            yield s_item   
   
        id_ = str(response.url)
        id_= scrape_filter(id_,'https://www.spritmonitor.de/en/detail/' , '.html')
        id1 = id_.removeprefix('https://www.spritmonitor.de/en/detail/')
        with open('C:\\Users\KPA5367\\sprit_links\\table_data\\'+ id1 +'.csv','w') as file:
            date = response.css('#content-left > div.itemtable_wrapper > table > tbody > tr > td.fueldate ::text').getall()
            
            for i in range(len(date)):
                table_headers = ['ID','Date','Odometer','Distance','Refuel_Quantity','Refuel_Type','Fuel_Consumption']
                writer = csv.DictWriter(file, fieldnames= table_headers)
                writer.writeheader()
                Odometer = response.css('td.fuelkmpos').extract()[i] or 'na'
                
                Distance = response.css('td.trip').extract()[i] or 'na'
                Refuel_Quantity = response.css('td.quantity').extract()[i] or 'na'
                Refuel_Type = (response.css('td.fuelsort ::attr(onmouseover)').extract()[i]).replace('(','').replace('"','').replace(')','').replace (',','') or 'na'
                FC = response.css('#content-left > div.itemtable_wrapper > table > tbody > tr > td.consumption').extract()[i] or 'na'
                Date = response.css('#content-left > div.itemtable_wrapper > table > tbody > tr > td.fueldate ::text').extract()[i]  or 'na'
                
                Odometer =  scrape_filter(Odometer,'<td class="fuelkmpos">','</td>')  or 'na'
                try:
                    Distance =  scrape_filter(Distance,'    \t\t  \n    \t\t        \t\t    \t','    \t\t        \t\t</td')  or 'na'
                    Distance = str(Distance).replace('.','').replace(',', '.')
                except AttributeError:
                    Distance = 'na'
                Refuel_Quantity = scrape_filter(Refuel_Quantity, '\n    \t\t        \t\t    \t', '    \t\t        \t\t</td')  or 'na'
                Refuel_Type = scrape_filter(Refuel_Type,'showTooltip(', ')'),
                try:
                    FC = scrape_filter(FC,'<td class="consumption" onmouseover="showTooltip',' l/100km')
                    FC = str(FC).replace('(','').replace("'", '').replace(',', '.')
                except  AttributeError:
                    FC = 'na'
    
                
                table ={ 'ID' : id_,
                        'Date' : Date,
                        'Odometer' :  Odometer,
                        'Distance' : Distance,
                        'Refuel_Quantity' :Refuel_Quantity,
                        'Refuel_Type' : Refuel_Type,
                        'Fuel_Consumption': FC
                        }
                writer.writerow(table)
                
                
            next_page = response.xpath('//*[@id="content-left"]/div[7]/a[last()]/@href').get()
            
            if next_page:
                next_url = 'https://www.spritmonitor.de'+ str(next_page)
                
                yield scrapy.Request(url=next_url,callback=self.parse)

                

            
            #'<td class="consumption" onmouseover="showTooltip(\'5,20 l/100km\')"
