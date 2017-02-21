import urlparse

import scrapy
import mysql.connector

class MySpider(scrapy.Spider):
    name = "myspider"
    handle_httpstatus_list = [111]

    def start_requests(self):
        try:
            self.db_conn = mysql.connector.connect(user='root', password='root',
                                                    host='localhost',
                                                    database='ScrapeProject')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Wrong user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            self.db_conn.close()

        # Get urls to scrape from DB here
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            proxy = self.get_random_proxy()
            request = scrapy.Request(url=url, callback=self.parse)
            # request.meta['proxy'] = proxy
            request.meta['proxy'] = 'http://127.0.0.1:'
            yield request

    def parse(self, response):
        if response.status_code == 111:
            self.log("Failed to access page using proxy {}".format(response.meta['proxy']))
            # remove proxy from db
            cursor = self.db_conn.cursor()
            parsed_proxy = urlparse.urlparse(response.meta['proxy'])
            delete_query = "DELETE FROM tbl_Proxies WHERE IP = %s AND Port = %s"
            cursor.execute(delete_query, (parsed_proxy.hostname, parsed_proxy.port))
            self.db_conn.commit()
            new_proxy = self.get_random_proxy()
            request = scrapy.Request(url=ur, callback=self.parse)
            request.meta['proxy'] = proxy
            yield request
        else :
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