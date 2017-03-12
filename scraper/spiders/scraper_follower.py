import scrapy

def generate_next_urls(response):
    '''
    Sample crawler. Replace with your own implementation.
    https://doc.scrapy.org/en/1.3/intro/tutorial.html#following-links
    '''
    next_page = response.css('li.next a::attr(href)').extract_first()
    if next_page is not None:
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page)