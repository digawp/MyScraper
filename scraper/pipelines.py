# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from contextlib import contextmanager
from datetime import datetime
import logging

from pymysql import err
from sqlalchemy import create_engine, orm, exc

import db
import items

class ScraperPipeline(object):
    def open_spider(self, spider):
        engine = create_engine(db.CONN_URL)
        self.Session = orm.sessionmaker(bind=engine)

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
            person = db.Person(name=item['name'], url=item['url'])
            person.primary_role = item.get('primary_role')
            if item.get('born'):
                person.born = self.parse_date(item['born'])
            person.gender = item.get('gender')
            person.location = item.get('location')
            person.website = item.get('website')
            person.facebook = item.get('facebook')
            person.twitter = item.get('twitter')
            person.linkedin = item.get('linkedin')
            person.description = item.get('description')

            for raw_job in item.get('current_jobs', []):
                job = db.Job(title=raw_job[0], organization_url=raw_job[1], appointment_period=raw_job[2])
                person.jobs.append(job)
            for raw_job in item.get('past_jobs', []):
                job = db.Job(title=raw_job[0], organization_url=raw_job[1], start=raw_job[2], end=raw_job[3])
                person.jobs.append(job)

            for advisor_role in item.get('board_advisors', []):
                role = db.BoardAdvisorRole(title=advisor_role[0], organization_url=advisor_role[1])
                person.board_advisors.append(role)

            for investment in item.get('investments', []):
                inv = db.Investment(organization_url=investment[0])
                inv.date = self.parse_date(investment[1])
                person.investments.append(inv)

            for raw_edu in item.get('education', []):
                edu = db.Education(organization_url=raw_edu[0], period=raw_edu[1])
                person.education.append(edu)

            session.add(person)

    def store_org(self, item):
        with self.session_scope() as session:
            org = db.Organization(name=item['name'], url=item['url'])
            org.headquarters = item.get('headquarters')
            org.description = item.get('description')
            org.categories = item.get('categories')
            org.website = item.get('website')
            org.facebook = item.get('facebook')
            org.twitter = item.get('twitter')
            org.linkedin = item.get('linkedin')
            org.aliases = item.get('aliases')
            if item.get('founded'):
                org.found_date = self.parse_date(item['founded'])
            session.add(org)

    def store_acq(self, item):
        with self.session_scope() as session:
            try:
                focal_org = session.query(db.Organization).filter(
                    db.Organization.url.like('%{}%'.format(item['focal_company_url']))
                ).one()
                acq = db.Acquisition(acquired_organization_url=item['acquired_url'])
                if item.get('date'):
                    focal_org.date = self.parse_date(item['date'])
                focal_org.acquisitions.append(acq)

            except (orm.exc.MultipleResultsFound, orm.exc.NoResultFound) as e:
                logging.error('Supposed to find 1 result')
                raise e

    def store_employee(self, item):
        with self.session_scope() as session:
            try:
                org = session.query(db.Organization).filter(
                    db.Organization.url.like('%{}%'.format(item['company_url']))
                ).one()
                employee = db.Employee(title=item.get('title'), person_url=item['person_url'])
                org.employees.append(employee)

            except (orm.exc.MultipleResultsFound, orm.exc.NoResultFound) as e:
                logging.error('Supposed to find 1 result')
                raise e

    def store_competitor(self, item):
        with self.session_scope() as session:
            try:
                focal_org = session.query(db.Organization).filter(
                    db.Organization.url.like('%{}%'.format(item['focal_company_url']))
                ).one()
                competitor = db.Competitor(competitor_url=item['competitor_url'])
                focal_org.competitors.append(competitor)

            except (orm.exc.MultipleResultsFound, orm.exc.NoResultFound) as e:
                logging.error('Supposed to find 1 result')
                raise e

    def store_partner(self, item):
        with self.session_scope() as session:
            try:
                focal_org = session.query(db.Organization).filter(
                    db.Organization.url.like('%{}%'.format(item['focal_company_url']))
                ).one()
                partner = db.Partner(partner_url=item['partner_url'])
                focal_org.partners.append(partner)

            except (orm.exc.MultipleResultsFound, orm.exc.NoResultFound) as e:
                logging.error('Supposed to find 1 result')
                raise e

    def store_board_member(self, item):
        with self.session_scope() as session:
            try:
                org = session.query(db.Organization).filter(
                    db.Organization.url.like('%{}%'.format(item['company_url']))
                ).one()
                board_member = db.BoardMember(title=item.get('title'), person_url=item['person_url'])
                org.board_members.append(board_member)

            except (orm.exc.MultipleResultsFound, orm.exc.NoResultFound) as e:
                logging.error('Supposed to find 1 result')
                raise e

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except (err.IntegrityError, exc.IntegrityError):
            session.rollback()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    """
    Parses dates with the possible date formats in Crunchbase.
    """
    def parse_date(self, date_string):
        date_formats = [
            '%B %d, %Y',
            '%b, %Y',
            '%b %d, %Y',
            '%b, %Y',
            '%B, %Y',
            '%Y',
        ]
        for date_format in date_formats:
            try:
                dt = datetime.strptime(date_string, date_format)
            except ValueError:
                # Try another date_format
                continue
            else:
                return dt.date()
        # If loop exits and we still haven't returned, that means date_formats
        # need to be expanded with the uncaught date_string date format
        raise ValueError('No formats fits the date string {}'.format(date_string))
