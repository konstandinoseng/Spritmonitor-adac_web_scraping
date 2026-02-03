# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpritLinksItem(scrapy.Item):
    ID = scrapy.Field()
    Title = scrapy.Field()
    Description = scrapy.Field()
    Avg_FC = scrapy.Field()

