# import scrapy

def parse(response):
    for quote in response.css('div.quote'):
        yield {
            'text': quote.css('span.text::text').extract_first(),
            'author': quote.css('small.author::text').extract_first(),
            'tags': quote.css('div.tags a.tag::text').extract(),
        }
