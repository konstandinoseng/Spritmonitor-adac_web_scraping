import scrapy
from scrapy import Request
from ..items import AdacItem
class AdacDataSpider(scrapy.Spider):
    name = 'adac_data1'
    allowed_domains = ['www.adac.de']
    with open("C:\\Users\\DELL\\OneDrive\\Έγγραφα\\Toyota\\adac\\data\\adac_links_m\\adac_links_m.txt") as f:
         start_urls = [url.strip() for url in f.readlines()]
    
    def requests(self,response):
        r = Request(url = self.start_urls,callback=self.parse,dont_filter=False)
        yield r
    def parse(self,response):
        base = 'https://www.adac.de'
        #all series of cars
        
        
        links = response.xpath("//a[contains(., 'seit')]/@href").extract()
        for i in range(len(links)):
            links[i]= ''.join(map(str, links[i])) 
            links[i] =  base + str(links[i])
            req = links[i]
            r = Request(url= req ,callback=self.parsemodel,dont_filter= False)
            yield r
        
    def parsemodel(self, response):
        check = response.xpath('descendant-or-self::table/tbody/tr[1]/td[2]/text()').get()
        if check != 'Strom' :
            #model links
            modlinks = response.css('tr ::attr(href)').extract()
            title = response.css('tr p::text').extract()
            dict_ = {}
            for key in title:
                for value in modlinks:
                     dict_[key] = value
                     modlinks.remove(value)
                     break
            for x, y in dict_.items():
                if '/20)' in x or '/21)' in x or '/22)' in x :
                    url1 = ''.join(map(str, y)) 
                    url = 'https://www.adac.de/' + url1 + '#technische-daten'
                    car_req = Request(url=url,callback=self.parse_details,dont_filter=False)
                    yield car_req
                else:
                    pass
        elif check =='Strom':
           pass
        
        
        
        
        
        
        
        
    def parse_details(self,response):
        Adac_details = AdacItem()
        table = response.xpath ('descendant-or-self::main/div[3]')
        #car specs
        Brand = table.css('tr:contains("Marke") ::text ').extract()[-1]
        Model =  table.css('tr:contains("Modell") ::text ').extract()[1]
        Series = table.css('tr:contains("Baureihe") ::text ').extract()[1]
        Enginetype= table.xpath('descendant-or-self::table/tbody/tr[1]/td[2]/text()').extract()[1]
        Systempowerkw  = table.css('tr:contains("Leistung maximal in kW (Systemleistung)") ::text ').extract()[-1]
        Systempowerps = table.css('tr:contains("Leistung maximal in PS (Systemleistung)") ::text ').extract()[-1]
        ratedpwrKW = table.css('tr:contains("Nennleistung in kW") ::text ').extract()
        
        
        displacement = table.css('tr:contains("Hubraum (Verbrennungsmotor)") ::text ').extract()[-1]
        emission_class = table.css('tr:contains("Schadstoffklasse") ::text ').extract()[0]
        weight = table.css('tr:contains("Leergewicht (EU)") ::text ').extract()[-1]
        WLTP_FC = response.css('p:contains("l/100") ::text ').get()
            
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