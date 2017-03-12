# import scrapy

def parse(response):
    '''
    Sample parser. Replace with your own implementation.
    https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data-in-our-spider
    '''
    for quote in response.css('div.quote'):
        yield {
            'text': quote.css('span.text::text').extract_first(),
            'author': quote.css('small.author::text').extract_first(),
            'tags': quote.css('div.tags a.tag::text').extract(),
        }
