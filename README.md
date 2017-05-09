# MyScraper

Crunchbase scraper written in Python, based on [Scrapy](https://scrapy.org/).

## User guide

### Requirements

- [Python 2.7](https://www.python.org/downloads/release/python-2713/)
- [NodeJS](https://nodejs.org/en/) or [Docker](https://www.docker.com/community-edition) (choose one, repo is tested using NodeJS)
- MySQL >=5 (XAMPP recommended)
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

0. Recommended: Activate virtualenv. (on Windows, and assuming your virtualenv directory is called `env`, the command is `env\Scripts\activate`)

1. Dump the URLs you want to crawl/scrape into `urls.txt`. Default encoding is UTF-16. If encoding is not UTF-16, change it in scraper/spiders/crunchbase_spider.py. If you are continuing a paused job, this step is not necessary.

2. Run the MySQL database. This step depends on the MySQL bundle you use (XAMPP/standalone).

3. Run scrapoxy: `scrapoxy start conf.json`

4. Run `make`. Log will be stored in scraper.log.

The scraper can pause and resume job. To pause simply issue an interrupt signal (Ctrl+C) once and wait until it shuts down (may take a while, a few minutes). It will automatically continue if you run `make` or `make test`. To start over from `urls.txt`, delete the `jobs` directory. Run `python setupdb.py` if you want to start over the database too.

If you intend to terminate and not to continue the job, forcing unclean shut down is fine (send interrupt twice) for quick termination. After the scraper has terminated, send interrupt signal to scrapoxy to terminate it too.

## Developer guide

### Technology stack used

These are the main frameworks/libraries used in this project. Read up on the getting started/tutorials of the respective stack if you are not familiar with it.

- Scrapy (the main framework)
- Scrapoxy (manages the proxies)
- SQL Alchemy (ORM)
- MySQL (DB)

For Scrapy, the important parts include the tutorial, Spider, Items, ItemLoader, Pipelines, and Settings.

For Scrapoxy, the important parts are just the getting started tutorial, integration with Scrapy, and Managing Blacklisting

For SQL Alchemy, read up the ORM getting started tutorial.

MySQL knowledge is not necessary as most of the detais are hidden behind the SQL Alchemy ORM, however, it would be good to have some knowledge in it too so that you can check if the changes you made on the ORM layer is correct.

### Project structure

The structure mostly follows Scrapy project structure. Some important files to take note:

- scraper/spiders/crunchbase_spider.py

    The main spider/scraper. This is where the crawling rules, start URL generation, and parsing of data is carried out.

- scraper/items.py

    Scrapy `Item` of the things that we want to scrape from the web pages. This is like the Model of MVC framework. Read the Items section of Scrapy docs for details.

- scraper/pipelines.py

    The pipeline that all scraped items will go through. Read the Pipelines section of Scrapy docs for details.

- scraper/settings.py

    The crawler configurations such as setting User-Agent, concurrent requests per domain, HTTP status code to mark response as blacklist, etc.

- scraper/db.py

    The ORM model. This is like the Model of MVC framework like scraper/items.py, except this is model for SQL Alchemy instead of Scrapy.

- conf.json

    Scrapoxy's config file.

- proxies.txt

    Previously used to keep the list of proxies to connect through. Obsolete, replaced with Scrapoxy. Kept just in case we want to revert to normal proxy

- setupdb.py

    A simple script to set up the Database according to the ORM model (scraper/db.py)

- url_cleaner.py

    Normalize URLs scraped by ScrapeBox from Prof Huang. Removes trailing `/investments` etc from crunchbase `/person/` URLs. Default encoding is UTF-16.

- scraper/spiders/{spider.py,scraper_follower.py,scraper_parser.py} and files under test_data

    Previously used in early stage of development. Understanding them is not required. They are kept only to let `make test1`, 2, and 3 (see below) to still run. Maybe useful if you want to play around with the settings.py and see how it performs under the different levels of scraper protections.

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

5. `scrapy shell "<target-url>"`

    Testing Xpath and CSS selectors. More info [here](https://doc.scrapy.org/en/1.3/intro/tutorial.html#extracting-data).

## License

[MIT](https://opensource.org/licenses/MIT)
