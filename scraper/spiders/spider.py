import scrapy

import scraper_parser
import scraper_crawler

class Spider(scrapy.Spider):
    name = "spider"

    def start_requests(self):
        urls = []

        with open('urls.txt', 'rb') as urls_file:
            urls = [line.strip() for line in
              urls_file.read().decode('utf8').splitlines()
              if line.strip()]

        for url in urls:
            yield scrapy.Request(url=url)

    def parse(self, response):
        for res in scraper_parser.parse(response):
            yield res
        for res in scraper_crawler.generate_next_urls(response):
            yield res
