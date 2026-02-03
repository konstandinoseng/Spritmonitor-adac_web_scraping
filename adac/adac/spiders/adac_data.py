import scrapy
from scrapy import Request
from ..items import AdacItem
class AdacDataSpider(scrapy.Spider):
    name = 'adac_data'
    allowed_domains = ['www.adac.de']
    with open("C:\\Users\\DELL\\OneDrive\\Έγγραφα\\Toyota\\adac\\data\\adac_links_m\\adac_links_m.txt") as f: 
         start_urls = [url.strip() for url in f.readlines()]
    
    def requests(self,response):
        r = Request(url = self.start_urls,callback=self.parse,dont_filter=False)
        yield r
    def parse(self,response):
        base = 'https://www.adac.de'
        #all series of cars
        
        l1 = response.xpath("//a[contains(.,'seit 201')]/@href").extract()
        l2 =  response.xpath("//a[contains(., '202')]/@href").extract() 
        links = l1 + l2
        for i in range(len(links)):
            links[i]= ''.join(map(str, links[i])) 
            links[i] =  base + str(links[i])
            req = links[i]
            r = Request(url= req ,callback=self.parsemodel,dont_filter= False)
            yield r
        
    def parsemodel(self, response):
        ftype = response.xpath('.//td[contains(@data-th,"Kraftstoff")]/text()').extract()
        modlinks = response.css('tr ::attr(href)').extract()
        title = response.css('tr p::text').extract()
        dict_ = {}

            #model links
            
        for key in title:
            for value in modlinks:
                 dict_[key] = value
                 modlinks.remove(value)
                 break
        for x, y in dict_.items():
                 if '/20)' in x or '/21)' in x or '/22)' in x or '(ab' in x :
                     ftype = response.xpath('.//td[contains(@data-th,"Kraftstoff")]/text()').get()
                     if ftype != 'Strom' and ftype != 'Erdgas' :
                            url1 = ''.join(map(str, y)) 
                            url = 'https://www.adac.de/' + url1 + '#technische-daten'
                            car_req = Request(url=url,callback=self.parse_details,dont_filter=False)
                            yield car_req


    
        
        
        
        
        
        
    def parse_details(self,response):
        Adac_details = AdacItem()
        #car specs
        table = response.css('main ::text ').extract()
        Brand = response.css('tr:contains("Marke") ::text ').extract()[-1]
        Model =  table[table.index("Modell") + 1]
        Series =  table[table.index("Baureihe") +1]
        Enginetype=  table[table.index("Motorart") +1]
        Systempowerkw  =  table[table.index("Leistung maximal in kW (Systemleistung)") +1]
        Systempowerps =  table[table.index("Leistung maximal in PS (Systemleistung)") +1]
        ratedpwrKW =  table[table.index("Leistung / Drehmoment (Verbrennungsmotor)") + 1].split('(')[0] #DOES NOT EXIST EVERYWHERE

        
        displacement =  response.css('p:contains("cc")::text').get()
        emission_class = table[table.index("Schadstoffklasse") +1]
        weight = table[table.index("Leergewicht (EU)") +1]
        WLTP_FC = response.css('p:contains("l/100 km")::text').get()
        
        Adac_details['Brand'] = Brand 
        Adac_details['Model'] = Model
        Adac_details['Series'] = Series
        Adac_details['Enginetype']= Enginetype
        Adac_details['Systempowerkw']  = Systempowerkw
        Adac_details['Systempowerps'] = Systempowerps
        Adac_details['RatedpwrKW'] = ratedpwrKW
        

        
        Adac_details['Displacement'] = displacement 
        Adac_details['Emission_class'] = emission_class
        Adac_details['Weight'] = weight
        Adac_details['WLTP_FC'] = WLTP_FC 
        yield Adac_details
        
        