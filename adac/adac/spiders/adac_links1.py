import scrapy
from scrapy import Request

class AdacLinksSpider(scrapy.Spider):
    name = 'adac_links_m'
    allowed_domains = ['www.adac.de']
    start_urls = ['https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/vw/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/mercedes-benz/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/bmw/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/audi/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/opel/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/skoda/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/ford/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/seat/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/hyundai/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/renault/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/fiat/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/toyota/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/kia/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/peugeot/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/volvo/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/mini/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/citroen/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/mazda/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/mitsubishi/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/suzuki/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/nissan/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/smart/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/jeep/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/land-rover/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/honda/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/subaru/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/jaguar/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/lexus/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/alfa-romeo/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/daihatsu/?filter=ONLY_RECENT&sort=SORTING_DESC',
    'https://www.adac.de//rund-ums-fahrzeug/autokatalog/marken-modelle/chevrolet/?filter=ONLY_RECENT&sort=SORTING_DESC'
    ]

    def requests(self,response):
       r = Request(url=self.start_urls,callback=self.parse,dont_filter=False)
       yield r
       
    def parse(self, response):
        base = 'https://www.adac.de/'
        
        links = response.css('main > div ::attr(href)').extract()
        for link in links:
            yield{
                'link': base + str(link)
                }