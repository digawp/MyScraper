# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Person(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    primary_role = scrapy.Field()
    born = scrapy.Field()
    gender = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    description = scrapy.Field()

    # Fields that are stored in a different table
    jobs = scrapy.Field()
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
