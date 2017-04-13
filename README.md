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

4. Write your parser implementation (the algorithm that extracts the information you want) in `spiders/scraper_parser.py`. [Here's a sample from scrapy tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data-in-our-spider).

5. Write your link follower implementation (the algorithm that decides the next URL to visit) in `spiders/scraper_follower.py`. [Here's a sample from scrapy tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html#following-links).

6. `scrapy crawl spider -o <output-file-name>.<xml|jsonlines|jl|json|csv|pickle|marshal>`

## Developer guide

### Testing

3 different tests with different levels of scraper protection

1. `make test1`

    No protection whatsoever. Taken from [scrapy's tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html).

2. `make test2`

    Moderate level of protection. Taken from [scrapoxy's tutorial](https://scrapoxy.readthedocs.io/en/master/tutorials/python-scrapy/index.html). Known protections: throttle requests, user-agent check.

3. `make test3`

    Moderate level of protection. Scrape data from crunchbase.com profiles. Known protections: throttle requests, user-agent check, non-resident(?) IP blacklisting.

## License

[MIT](https://opensource.org/licenses/MIT)
