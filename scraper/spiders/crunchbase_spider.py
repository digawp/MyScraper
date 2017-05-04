import scrapy
from scrapy import spiders
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader, processors
import w3lib.html

from scraper.items import *

class CrunchbaseSpider(spiders.CrawlSpider):
    name = "crunchbase"

    # TODO: find out if pages with 416 status code is re-crawled or not!
    # handle_httpstatus_list = [416]

    def start_requests(self):
        urls = []

        with open('urls.txt', 'rb') as urls_file:
            urls = [line.strip() for line in
              urls_file.read().decode('utf8').splitlines()
              if line.strip()]

        for url in urls:
            yield self.make_requests_from_url(url)

    rules = (
        # Crawl and parse person
        spiders.Rule(
            LinkExtractor(allow=r'/person/.*', deny=r'/person/.*[/\.]'),
            callback='parse_employees', follow=True),
        # Crawl organization
        spiders.Rule(
            LinkExtractor(allow=r'/organization/.*', deny=r'/organization/.*[/\.]'),
            callback='parse_organization', follow=True),
        # Crawl acquisitions table
        spiders.Rule(
            LinkExtractor(allow=r'/acquisitions$', deny=r'/app/search', restrict_css='.acquisitions'),
            callback='parse_acquisitions'),
        # Crawl employees
        spiders.Rule(
            LinkExtractor(allow=r'/people$', deny=r'/app/search', restrict_css='.people'),
            callback='parse_employees'),
        # Crawl competitors
        spiders.Rule(
            LinkExtractor(allow=r'/competitors$', restrict_css='.competitors'),
            callback='parse_competitors'),
        # Crawl partners
        spiders.Rule(
            LinkExtractor(allow=r'/partners$', restrict_css='.partners'),
            callback='parse_partners'),
        # Crawl advisors
        spiders.Rule(
            LinkExtractor(allow=r'/advisors$', restrict_css='.advisors'),
            callback='parse_advisors'),
    )

    def parse_start_url(self, response):
        if response.url.find('/person/') >= 0:
            self.parse_person(response)
        if response.url.find('/organization/') >= 0:
            self.parse_organization(response)
        else:
            raise Exception('Start url is neither person nor organization')

    """
    NOTE: there might be field-specific processors under scraper/items.py
    """
    def parse_person(self, response):
        loader = ItemLoader(item=Person(), response=response)
        loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
        loader.default_output_processor = processors.TakeFirst()

        loader.add_xpath('name', '//*[@id="profile_header_heading"]/a/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('primary_role', '//*[@id="info-card-overview-content"]/div/dl/div/dd')

        # Fields expected: born, gender, location, website
        overview = response.xpath('//*[@id="info-card-overview-content"]/div/dl/dt/text()')
        overview_loader = loader.nested_xpath('//*[@id="info-card-overview-content"]/div/dl')
        for i in range(len(overview)):
            key = overview[i].extract()
            key = key[:key.find(':')].lower()
            try:
                overview_loader.add_xpath(key, 'dd[{}]/text()'.format(i+1))
            except KeyError as e:
                # Ignore if key is not in the Item's field
                pass

        loader.add_xpath('facebook', '(//a[contains(@class,"facebook")])[1]/@href')
        loader.add_xpath('twitter', '(//a[contains(@class,"twitter")])[1]/@href')
        loader.add_xpath('linkedin', '(//a[contains(@class,"linkedin")])[1]/@href')
        loader.add_xpath('description', '//*[@id="description"]/span/div')
        loader.add_css('current_jobs', '.current_job')
        loader.add_css('past_jobs', '.past_job')
        loader.nested_css('.advisory_roles').add_xpath('board_advisors', './/ul/li')
        loader.nested_css('table.investors').add_xpath('investments', './/tr[not(@class="thead")]')
        loader.nested_css('.education').add_xpath('education', './/ul/li')

        return loader.load_item()

    def parse_organization(self, response):
        loader = ItemLoader(item=Organization(), response=response)
        loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
        loader.default_output_processor = processors.TakeFirst()

        loader.add_xpath('name', '//*[@id="profile_header_heading"]/a/text()')
        loader.add_value('url', response.url)
        # loader.add_value('ipo_stock', None) # TODO!

        # Fields expected: headquarters, description, founders, categories, website
        overview = response.xpath('//*[@id="info-card-overview-content"]/div/dl/dt/text()')
        overview_loader = loader.nested_xpath('//*[@id="info-card-overview-content"]/div/dl')
        for i in range(len(overview)):
            key = overview[i].extract()
            key = key[:key.find(':')].lower()
            try:
                overview_loader.add_xpath(key, 'dd[{}]/text()'.format(i+1))
            except KeyError as e:
                # Ignore if key is not in the Item's field
                pass

        loader.add_xpath('facebook', '(//a[contains(@class,"facebook")])[1]/@href')
        loader.add_xpath('twitter', '(//a[contains(@class,"twitter")])[1]/@href')
        loader.add_xpath('linkedin', '(//a[contains(@class,"linkedin")])[1]/@href')

        # Fields expected: founded and aliases
        details = response.xpath('//div[@class="details definition-list"]/dt/text()')
        details_loader = loader.nested_xpath('//div[@class="details definition-list"]')
        for i in range(len(details)):
            key = details[i].extract()
            key = key[:key.find(':')].lower()
            try:
                overview_loader.add_xpath(key, 'dd[{}]/text()'.format(i+1))
            except KeyError as e:
                # Ignore if key is not in the Item's field
                pass

        yield loader.load_item()

        for item in self.parse_acquisitions(response):
            yield item
        for item in self.parse_employees(response):
            yield item
        for item in self.parse_competitors(response):
            yield item
        for item in self.parse_partners(response):
            yield item
        for item in self.parse_advisors(response):
            yield item

    def parse_acquisitions(self, response):
        company_url = response.xpath('//*[@id="profile_header_heading"]/a/@href').extract_first()
        acq_selectors = response.css('div.acquisitions').xpath('.//tr[not(th)]')

        for sel in acq_selectors:
            loader = ItemLoader(item=Acquisition(), selector=sel)
            loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
            loader.default_output_processor = processors.TakeFirst()

            loader.add_value('focal_company_url', company_url)
            loader.add_xpath('date', 'td[1]/text()')
            loader.add_xpath('acquired_url', 'td[2]/a/@href')
            yield loader.load_item()


    def parse_employees(self, response):
        company_url = response.xpath('//*[@id="profile_header_heading"]/a/@href').extract_first()
        employee_selector = response.css('div.people').xpath('.//ul/li')

        for sel in employee_selector:
            loader = ItemLoader(item=Employee(), selector=sel)
            loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
            loader.default_output_processor = processors.TakeFirst()
            loader.add_value('company_url', company_url)
            loader.add_xpath('person_url', './/h4/a/@href')
            loader.add_xpath('title', './/h5/text()')
            yield loader.load_item()

    def parse_competitors(self, response):
        company_url = response.xpath('//*[@id="profile_header_heading"]/a/@href').extract_first()
        comp_selectors = response.css('div.competitors').xpath('.//ul/li//h4/a')

        for sel in comp_selectors:
            loader = ItemLoader(item=Competitor(), selector=sel)
            loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
            loader.default_output_processor = processors.TakeFirst()
            loader.add_value('focal_company_url', company_url)
            loader.add_xpath('competitor_url', '@href')
            yield loader.load_item()

    def parse_partners(self, response):
        company_url = response.xpath('//*[@id="profile_header_heading"]/a/@href').extract_first()
        partner_selectors = response.css('div.partners').xpath('.//ul/li//h4/a')

        for sel in partner_selectors:
            loader = ItemLoader(item=Partner(), selector=sel)
            loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
            loader.default_output_processor = processors.TakeFirst()
            loader.add_value('focal_company_url', company_url)
            loader.add_xpath('partner_url', '@href')
            yield loader.load_item()

    def parse_advisors(self, response):
        company_url = response.xpath('//*[@id="profile_header_heading"]/a/@href').extract_first()
        employee_selector = response.css('div.advisors').xpath('.//ul/li')

        for sel in employee_selector:
            loader = ItemLoader(item=BoardMember(), selector=sel)
            loader.default_input_processor = processors.MapCompose(w3lib.html.remove_tags)
            loader.default_output_processor = processors.TakeFirst()
            loader.add_value('company_url', company_url)
            loader.add_xpath('person_url', './/h4/a/@href')
            loader.add_xpath('title', './/h5/text()')
            yield loader.load_item()

    def parse_default(self, response):
        print('Found response 416. Pushing redirected URL back to queue.')
        if response.status == 416:
            return scrapy.Request(url=response.meta['redirect_urls'][0])
