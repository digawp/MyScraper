import scrapy

def generate_next_urls(response):
    next_page = response.css('li.next a::attr(href)').extract_first()
    if next_page is not None:
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page)