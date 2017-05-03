import scrapy
from scrapy import spiders
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader, processors
import w3lib.html

from scraper.items import Person, Organization

class CrunchbaseSpider(spiders.CrawlSpider):
    name = "crunchbase"

    def start_requests(self):
        urls = []

        with open('urls.txt', 'rb') as urls_file:
            urls = [line.strip() for line in
              urls_file.read().decode('utf8').splitlines()
              if line.strip()]

        for url in urls:
            yield scrapy.Request(url=url)

    rules = (
        # Crawl and parse person
        spiders.Rule(
            LinkExtractor(allow=r'/person/.*', deny=r'/person/.*/'),
            callback='parse_person', follow=True),
        # Crawl organization
        spiders.Rule(
            LinkExtractor(allow=r'/organization/.*', deny=r'/organization/.*/'),
            callback='parse_organization'),
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
        # loader.add_value('ipo_stock', None)

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
            # Not supposed to fill in employees from here
            if key == 'employees':
                continue
            try:
                overview_loader.add_xpath(key, 'dd[{}]/text()'.format(i+1))
            except KeyError as e:
                # Ignore if key is not in the Item's field
                pass

        loader.add_css('acquisitions', 'div.acquisitions')
        loader.add_css('employees', 'div.people')
        loader.nested_css('div.competitors').add_xpath('competitors', './/ul/li//h4/a/@href')
        loader.nested_css('div.partners').add_xpath('partners', './/ul/li//h4/a/@href')
        loader.add_css('board_members', 'div.advisors')

        return loader.load_item()

    def parse_acquisitions(self, response):
        pass

    def parse_employees(self, response):
        pass

    def parse_competitors(self, response):
        pass

    def parse_partners(self, response):
        pass

    def parse_advisors(self, response):
        pass
