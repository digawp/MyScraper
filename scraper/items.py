# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import processors
from scrapy.selector import Selector
import w3lib

class Person(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    primary_role = scrapy.Field(
        input_processor=processors.MapCompose(w3lib.html.remove_tags))
    born = scrapy.Field()
    gender = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    description = scrapy.Field(
        input_processor=processors.MapCompose(w3lib.html.remove_tags),
        output_processor=processors.Join())

    # Fields that are stored in a different table
    jobs = scrapy.Field(
        input_processor=processors.Identity(),
        output_processor=processors.Identity())
    board_advisors = scrapy.Field()
    investments = scrapy.Field()
    education = scrapy.Field()

class Organization(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    ipo_date = scrapy.Field()
    stock_code = scrapy.Field()
    headquarters = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    website = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    found_date = scrapy.Field()
    aliases = scrapy.Field()

    acquisitions = scrapy.Field()
    founders = scrapy.Field()
    employees = scrapy.Field()
    competitors = scrapy.Field()
    partners = scrapy.Field()
    board_members = scrapy.Field()
