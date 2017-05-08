# MyScraper

Crunchbase scraper written in Python, based on [Scrapy](https://scrapy.org/).

## User guide

### Requirements

- [Python 2.7](https://www.python.org/downloads/release/python-2713/)
- [NodeJS](https://nodejs.org/en/) or [Docker](https://www.docker.com/community-edition) (choose one, repo is tested using NodeJS)
- MySQL >=5
- An account in AWS/DigitalOcean/OVH Cloud/Vscale (repo is using AWS)

Strongly recommended:
- [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- GNU Make ([download link](http://gnuwin32.sourceforge.net/packages/make.htm) if you are on Windows). Without this you need to type out the commands manually by referring to the `Makefile`.

### Setup

1. Install all the requirements following the instructions from their respective websites depending on your platform.

2. Install scrapoxy (follow the instruction [here](https://scrapoxy.readthedocs.io/en/master/quick_start/index.html) up to step 3B `sudo npm install -g scrapoxy`, or follow until the end to verify that it is installed correctly)

    Note that the installation assumes that you are on Ubuntu. Installing build-tools may not be necessary on Windows (tested on Prof Huang's office workstation).

3. In MySQL database, create a database `crunchbase` and an account with the same name. Give it full privileges for `crunchbase` database.

    If you are using XAMPP, you are recommended to create the account by doing the following: Go to `mysql` database > Privileges > Add user > Under Database for user, choose "Create database with same name and grant all privileges".

3b. Recommended: Setup [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in the directory. This is to ensure you are running the correct Python version (2.7), and not polluting your global pip packages.

4. `pip install -r requirements.txt`

    On Windows, you need to `pip install pypiwin32` too.

5. Run `python setupdb.py`

    If this doesn't work, check the connection URL `CONN_URL` in db.py.

### Usage

1. Dump the URLs you want to crawl/scrape into `urls.txt`. Default encoding is UTF-16. If it is not, change it in scraper/spiders/crunchbase_spider.py

2. Run scrapoxy: `scrapoxy start conf.json`

3. Run `make`. Log will be stored in scraper.log.


## Developer guide

### Testing

3 different tests with different levels of scraper protection

1. `make test1`

    No protection whatsoever. Taken from [scrapy's tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html).

2. `make test2`

    Moderate level of protection. Taken from [scrapoxy's tutorial](https://scrapoxy.readthedocs.io/en/master/tutorials/python-scrapy/index.html). Known protections: throttle requests, user-agent check.

3. `make test3`

    Moderate level of protection. Scrape data from crunchbase.com profiles. Known protections: throttle requests, user-agent check, non-resident(?) IP blacklisting.

4. `make test`

    Stores scraped `Item`s to json file so you can compare it with what is stored in the database. Don't forget to run scrapoxy first before running `make test`.

### url_cleaner.py

Normalize URLs scraped by ScrapeBox from Prof Huang. Removes trailing `/investments` etc from crunchbase `/person/` URLs. Default encoding is UTF-16.

## License

[MIT](https://opensource.org/licenses/MIT)
