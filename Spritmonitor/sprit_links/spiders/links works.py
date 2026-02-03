import scrapy
##################WORKS############

class LinksSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['www.spritmonitor.de']
 
    start_urls = ['https://www.spritmonitor.de/en/overview/0-All_manufactures/0-All_models.html?vehicletype=1&constyear_s=2020&constyear_e=2022&page=1812']
    custom_settings = {'COOKIES_ENABLED': False,
                       'DOWNLOAD_DELAY': 3,
                       'AUTOTHROTTLE_ENABLED': True,
                       'AUTOTHROTTLE_DEBUG': True,
                       'RANDOMIZE_DOWNLOAD_DELAY':True
                       }
         
    
    def parse(self, response):
        base_url = 'https://www.spritmonitor.de'

        #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        #'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        #'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
        
        links = response.css('td.description a::attr(href)')
        for link in links:
            yield{
                'link': base_url + str(link.get())
                }
            #yield response.follow(link.extract(), callback = self.parse_links)
        next_page = response.xpath('//*[@id="searchresultbox"]/div/a[last()]/@href').extract()
        if next_page:
            next_url = ''.join(map(str, next_page)) 
            yield response.follow(next_url, callback=self.parse)
        
                        
            
      #base_url + str(response.xpath('//*[@id="searchresultbox"]/table/tbody/tr/td[2]/a/@href').get()  
    #def parse_links(self,response):

            
#C:\Users\DELL\OneDrive\Έγγραφα\Toyota\sprit_links\sprit_links\spiders\links works.py
    