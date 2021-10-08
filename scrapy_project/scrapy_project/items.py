# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlipkartScraperItem(scrapy.Item):
    title = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    list_price = scrapy.Field()
    offer_price = scrapy.Field()
    colour = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    description = scrapy.Field()
    ram = scrapy.Field()
    rom = scrapy.Field()
    processor = scrapy.Field()
