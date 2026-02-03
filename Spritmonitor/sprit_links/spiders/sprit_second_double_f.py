import scrapy
from scrapy import Request
import re
from ..items import   SpritLinksItem
import csv



class SpritCharSpider(scrapy.Spider):

    rate = 0.5

    custom_settings = {
            'COOKIES_ENABLED': False,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1,
            'FEEDS' : {'data/%(name)s/%(name)s_%(time)s.csv':{'format': 'csv'}
            }
        }	

    name = 'sprit_second_csv'
    allowed_domains = ['www.spritmonitor.de']
    with open("C:\\Users\\KPA5367\\sprit_link_final_text.txt") as f:   #iterate through the URL text file
        start_urls = [url.strip() for url in f.readlines()]  #assing all links to a list in a form of string


    
    
    def requests (self,response):  #The function responsible for making the requests in the website
        
 
        r = Request(url=self.start_urls,callback=self.parse,dont_filter=False,meta={'download_timeout': 20}) 
        
        yield r  
  
    def parse(self, response):  #definition of a function which parses and saves the data acquired from the approved (by website's host) requests 
        #Define Items which will follow the default pipeline
        s_item = SpritLinksItem()
###########################################################################STRING FILTER######################
        def scrape_filter (string,prev_str,next_str):   #saves the value between 2 strings 
            y = re.search(prev_str + '(.*)' + next_str,string)
            new_val = y.group(1)
            return new_val
        def string_filter(text):  #removes '  ', '\n','\t' from data
            new_text = text.replace('\t','').replace('\n','').replace('  ','')
            return new_text
        
##############################################################################################################
##############################################################################################################
        link = str(response.url)
        if 'page=' not in link:  #if cased used in case of the existence of pagination in the table section
            #assign each of the data's location to variables
            ID =str(response.url.replace('https://www.spritmonitor.de/en/detail/','').replace('.html','')),
            Title = str(response.css('#vehicledetails h1::text').get()),
            Description = str(response.xpath('//*[@id="vehicledetails"]/text()[2]').get())
            Description = string_filter(Description)
     
            Avg_FC =str(response.css('td strong::text').get())

            Avg_FC = Avg_FC.replace('.','').replace(',', '.')
            #Matching variables with their equivalent position in the database which they will be saved
            s_item['ID'] = ID
            s_item['Title'] = Title
            s_item['Description'] =Description
            s_item['Avg_FC'] = Avg_FC
            s_item['Title'] = Title
            yield s_item #write all scraped variables to their columns in "Summary" dataset
        id_= scrape_filter(link,'https://www.spritmonitor.de/en/detail/' , '.html')
        id1 = id_.removeprefix('https://www.spritmonitor.de/en/detail/')
        with open('C:\\Users\KPA5367\\sprit_links\\test_table\\'+ id1 +'.csv','a',newline='') as file: #create a new csv file with each car's unique id as name in different location path
            #locate all table values needed
            date = response.css('#content-left > div.itemtable_wrapper > table > tbody > tr > td.fueldate ::text').getall()
            table_headers = ['ID','Date','Odometer','Distance','Refuel_Quantity','Refuel_Type','Fuel_Consumption'] #assign every csv's column names
            writer = csv.DictWriter(file, fieldnames= table_headers)
            writer.writeheader()
            for i in range(len(date)): #dates only variable with no nan values so the loop never stops when its not supposed to
               #get a list of all the values found in location of each column from the table
                try:
                    Odometer = response.css('td.fuelkmpos').extract()[i].replace('.','') or 'na' 
                except IndexError: #filter nan values to avoid errors
                    Odometer = 'na'
                
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
                Refuel_Quantity = str(Refuel_Quantity).replace('.','').replace(',', '.')
                Refuel_Type = scrape_filter(Refuel_Type,'showTooltip(', ')'),
                try:
                    FC = scrape_filter(FC,'<td class="consumption" onmouseover="showTooltip',' l/100km')
                    FC = str(FC).replace('(','').replace("'", '').replace(',', '.')
                except  AttributeError:
                    FC = 'na'

                #create a dictionary with all the lists created from the scraped page
                table ={ 'ID' : id_,
                        'Date' : Date,
                        'Odometer' :  Odometer,
                        'Distance' : Distance,
                        'Refuel_Quantity' :Refuel_Quantity,
                        'Refuel_Type' : Refuel_Type,
                        'Fuel_Consumption': FC
                        }
                writer.writerow(table) #write each row of the table in the id specific 
                
               #check for pagination inside the table 
                next_page = response.xpath('//*[@id="content-left"]/div/a[last()]/@href').extract() #location of "next page" button in refuelling table

                
            if next_page is not None: #if a string is found yield a request before proceeding to next car
                next_url1 = ''.join(map(str, next_page)) 
                next_url = 'https://www.spritmonitor.de' + next_url1
                    
                yield scrapy.Request(url=next_url,callback= self.parse,dont_filter=False,meta={'download_timeout': 20})
                    

            else:
                pass  


                            
                
                

            
            #'<td class="consumption" onmouseover="showTooltip(\'5,20 l/100km\')"
