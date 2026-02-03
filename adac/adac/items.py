# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdacItem(scrapy.Item):
    Brand = scrapy.Field()
    Model = scrapy.Field()
    Series = scrapy.Field()
    Enginetype= scrapy.Field()
    Systempowerkw  = scrapy.Field()
    Systempowerps = scrapy.Field()  
    RatedpwrKW =    scrapy.Field()
    
    Torque = scrapy.Field()
    Cylinders =scrapy.Field()
    Valves_count = scrapy.Field()
    Power_rpm = scrapy.Field()
    Torque_rpm = scrapy.Field()
    wheelbase = scrapy.Field()
    wheel_size = scrapy.Field()
    
    Displacement = scrapy.Field()
    Emission_class = scrapy.Field()
    Weight = scrapy.Field()
    WLTP_FC = scrapy.Field()
