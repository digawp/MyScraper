import scrapy

import scraper_parser2

def generate_next_urls(response):
    '''
    Sample crawler. Replace with your own implementation.
    https://doc.scrapy.org/en/1.3/intro/tutorial.html#following-links
    '''
    if response.url != 'http://scraping-challenge-2.herokuapp.com':
        return
    urls = response.xpath(u'//a/@href').extract()
    for url in urls:
        yield scrapy.Request(
            url=response.urljoin(url),
            callback=scraper_parser2.parse,
        )