# import scrapy

def parse(response):
    '''
    Sample parser. Replace with your own implementation.
    https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data-in-our-spider
    '''
    name_el = response.css(u'.profile-info-name::text').extract()
    if len(name_el) > 0:
        yield {
            'name': name_el[0]
        }
