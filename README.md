# MyScraper

A customizable (to some extent) scraper written in Python, based on [Scrapy](https://scrapy.org/).

## User guide

### Requirements

- Python

### Usage

1. `pip install -r requirements.txt`

2. Dump the URLs you want to crawl/scrape into `urls.txt`

3. Dump the proxies you have (if any) into `proxies.txt`.
    Currently we only support public proxies and private proxies with `user:password@ip:port` form of authentication (and you should write the proxies accordingly).

4. Write your parser implementation (the algorithm that extracts the information you want) in `spiders/scraper_parser.py`. (Here's a sample from scrapy tutorial)[https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data-in-our-spider].

5. Write your crawler implementation (the algorithm that decides the next URL to visit) in `spiders/scraper_crawler.py`. (Here's a sample from scrapy tutorial)[https://doc.scrapy.org/en/1.3/intro/tutorial.html#following-links].

6. `scrapy crawl spider -o <output-file-name>.<xml|jsonlines|jl|json|csv|pickle|marshal>`

# License

[MIT](https://opensource.org/licenses/MIT)
