import urlparse

import scrapy
import mysql.connector

class MySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        # try:
        #     self.db_conn = mysql.connector.connect(user='root', password='',
        #                                             host='localhost',
        #                                             database='ScrapeProject')
        # except mysql.connector.Error as err:
        #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #         print("Wrong user name or password")
        #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #         print("Database does not exist")
        #     else:
        #         print(err)
        #     self.db_conn.close()

        # Get urls to scrape from DB here
        urls = [
            'http://www.nus.edu.sg/',
            'http://www.comp.nus.edu.sg/',
        ]

        for url in urls:
            # proxy = self.get_random_proxy()
            request = scrapy.Request(url=url, callback=self.parse)
            # request.meta['proxy'] = proxy
            yield request

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
            self.log('Saved file %s' % filename)

    def get_random_proxy(self):
        cursor = self.db_conn.cursor()
        query = "SELECT IP, Port FROM tbl_Proxies ORDER BY RAND() LIMIT 1"
        cursor.execute(query)
        res = cursor.fetchone()
        proxy = "http://{}:{}".format(res[0], res[1])
        self.log(proxy)
        return proxy