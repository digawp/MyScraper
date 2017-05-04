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

    # Helper functions
    def _current_jobs_processor(node_list):
        jobs = []
        for node in node_list:
            selector = Selector(text=node)
            title = selector.xpath('//h4/text()').extract_first()
            company_url = selector.xpath('//a/@href').extract_first()
            appointment_period = \
                selector.xpath('//h5[@class="date"]/text()').extract_first()
            jobs.append((title, company_url, appointment_period))
        return jobs

    def _past_jobs_processor(node_list):
        if not node_list:
            return
        selector = Selector(text=node_list[0])
        title = selector.css('.title::text').extract()
        company_url = selector.xpath('//a/@href').extract()
        start = selector.xpath('//div[@class="cell date"][1]/text()').extract()
        end = selector.xpath('//div[@class="cell date"][2]/text()').extract()
        return zip(title, company_url, start, end)

    def _board_advisors_processor(node_list):
        jobs = []
        for node in node_list:
            selector = Selector(text=node)
            title = selector.xpath('//h5[not(@class)]/text()').extract_first()
            company_url = selector.xpath('//a/@href').extract_first()
            jobs.append((title, company_url))
        return jobs

    def _investments_processor(node_list):
        investments = []
        for node in node_list:
            selector = Selector(text=node)
            company_url = selector.xpath('//a/@href').extract_first()
            date = selector.css('td.date::text').extract_first()
            investments.append((company_url, date))
        return investments

    def _education_processor(node_list):
        edu = []
        for node in node_list:
            selector = Selector(text=node)
            school_url = selector.xpath('//a/@href').extract_first()
            period = selector.xpath('//div/text()').extract_first()
            edu.append((school_url, period))
        return edu

    # Fields
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
    description = scrapy.Field(output_processor=processors.Join())

    # Fields that are stored in a different table
    # Current and past jobs stored in different fields because they will be
    # processed differently in the item pipeline
    current_jobs = scrapy.Field(
        input_processor=processors.Compose(_current_jobs_processor),
        output_processor=processors.Identity())
    past_jobs = scrapy.Field(
        input_processor=processors.Compose(_past_jobs_processor),
        output_processor=processors.Identity())
    board_advisors = scrapy.Field(
        input_processor=processors.Compose(_board_advisors_processor),
        output_processor=processors.Identity())
    investments = scrapy.Field(
        input_processor=processors.Compose(_investments_processor),
        output_processor=processors.Identity())
    education = scrapy.Field(
        input_processor=processors.Compose(_education_processor),
        output_processor=processors.Identity())

class Organization(scrapy.Item):

    name = scrapy.Field()
    url = scrapy.Field()
    ipo_stock = scrapy.Field()
    headquarters = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    website = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    founded = scrapy.Field()
    aliases = scrapy.Field()
    founders = scrapy.Field()

class Acquisition(scrapy.Item):
    focal_company_url = scrapy.Field()
    acquired_url = scrapy.Field()
    date = scrapy.Field()

class Employee(scrapy.Item):
    company_url = scrapy.Field()
    person_url = scrapy.Field()
    title = scrapy.Field()

class Competitor(scrapy.Item):
    focal_company_url = scrapy.Field()
    competitor_url = scrapy.Field()

class Partner(scrapy.Item):
    focal_company_url = scrapy.Field()
    partner_url = scrapy.Field()

class BoardMember(scrapy.Item):
    company_url = scrapy.Field()
    person_url = scrapy.Field()
    title = scrapy.Field()
