# import scrapy

def parse(response):
    '''
    Sample parser. Replace with your own implementation.
    https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data-in-our-spider
    '''
    name = response.css('#profile_header_heading > a::text').extract_first()
    details = response.css('#description > span > div > p::text').extract_first()
    yield {
        'name': name,
        'details': details
    }
