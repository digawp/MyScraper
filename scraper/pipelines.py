# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from contextlib import contextmanager
from datetime import datetime

from pymysql.err import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db
import items

class ScraperPipeline(object):
    def open_spider(self, spider):
        engine = create_engine('mysql+pymysql://crunchbase@localhost/crunchbase?charset=utf8')
        self.Session = sessionmaker(bind=engine)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item_type = type(item)
        if item_type == items.Person:
            self.store_person(item)
        elif item_type == items.Organization:
            self.store_org(item)
        elif item_type == items.Acquisition:
            self.store_acq(item)
        elif item_type == items.Employee:
            self.store_employee(item)
        elif item_type == items.Competitor:
            self.store_competitor(item)
        elif item_type == items.Partner:
            self.store_partner(item)
        elif item_type == items.BoardMember:
            self.store_board_member(item)
        else:
            raise Exception('Item type cannot be identified')
        return item

    def store_person(self, item):
        with self.session_scope() as session:
            person = db.Person(
                name=item['name'],
                url=item['url'],
            )
            person.primary_role = item.get('primary_role', None)
            if item.get('born', None):
                person.born = datetime.strptime(item['born'], '%B %d, %Y').date()
            person.gender = item.get('gender', None)
            person.location = item.get('location', None)
            person.website = item.get('website', None)
            person.facebook = item.get('facebook', None)
            person.twitter = item.get('twitter', None)
            person.linkedin = item.get('linkedin', None)
            person.description = item.get('description', None)
            session.add(person)


    def store_org(self, item):
        pass

    def store_acq(self, item):
        pass

    def store_employee(self, item):
        pass

    def store_competitor(self, item):
        pass

    def store_partner(self, item):
        pass

    def store_board_member(self, item):
        pass

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except IntegrityError:
            session.rollback()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
