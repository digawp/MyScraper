test1:
	cp test_data/scraper_parser1.py scraper/spiders/scraper_parser.py
	cp test_data/scraper_follower1.py scraper/spiders/scraper_follower.py
	cp test_data/urls1.txt urls.txt
	scrapy crawl spider -o out.csv

test2:
	cp test_data/scraper_parser2.py scraper/spiders/scraper_parser.py
	cp test_data/scraper_follower2.py scraper/spiders/scraper_follower.py
	cp test_data/urls2.txt urls.txt
	scrapy crawl spider -o out.csv

test3:
	cp test_data/scraper_parser3.py scraper/spiders/scraper_parser.py
	cp test_data/scraper_follower3.py scraper/spiders/scraper_follower.py
	cp test_data/urls3.txt urls.txt
	scrapy crawl spider -o out.csv

clean:
	rm -f **/*.pyc **/*.csv **/*.json **/*.xml
