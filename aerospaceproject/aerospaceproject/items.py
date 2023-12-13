# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Name 	Status 	Launch Service Provider 	Rocket 	Mission 	Net 	Pad
"""

class AerospaceprojectItem(scrapy.Item):
    name = scrapy.Field()
    status = scrapy.Field()
    launch_service_provider = scrapy.Field()
    rocket = scrapy.Field()
    mission = scrapy.Field()
    net = scrapy.Field()
    pad = scrapy.Field()

