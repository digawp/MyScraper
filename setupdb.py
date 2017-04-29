import urlparse

from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Date, NVARCHAR, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_name_or_b(a, b):
    return a.name if a is not None else b

class Person(Base):
    """Represent a Person in Crunchbase"""
    __tablename__ = 'tbl_Person'

    id = Column(Integer, primary_key=True)
    name = Column(NVARCHAR(128), nullable=False)
    url = Column(VARCHAR(255), nullable=False, unique=True)
    primary_role = Column(VARCHAR(64))
    born = Column(Date)
    gender = Column(VARCHAR(16))
    location = Column(VARCHAR(128))
    website = Column(VARCHAR(255))
    facebook = Column(VARCHAR(255))
    twitter = Column(VARCHAR(255))
    linkedin = Column(VARCHAR(255))
    description = Column(TEXT)

    jobs = relationship('Job', back_populates='person')
    board_advisors = relationship('BoardAdvisorRole', back_populates='person')
    investments = relationship('Investment', back_populates='person')
    education = relationship('Education', back_populates='person')

    def __repr__(self):
        return self.name

class Job(Base):
    """Represent a Job that a Person has"""
    __tablename__ = 'tbl_Job'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'))
    organization_url = Column(VARCHAR(255), nullable=False)
    title = Column(VARCHAR(64))
    start = Column(VARCHAR(16))
    end = Column(VARCHAR(16))
    appointment_period = Column(VARCHAR(64))

    person = relationship('Person', back_populates='jobs')
    organization = relationship('Organization')

    def __repr__(self):
        return '{}, {} of {}'.format(self.person.name, self.title,
            get_name_or_b(self.organization, self.organization_url))
                  
class BoardAdvisorRole(Base):
    """Represent a Board and Adivsor Role a Person has"""
    __tablename__ = 'tbl_BoardAdvisorRole'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'))
    organization_url = Column(VARCHAR(255), nullable=False)
    title = Column(VARCHAR(64))

    person = relationship('Person', back_populates='jobs')
    organization = relationship('Organization')

    def __repr__(self):
        return '{}, {} of {}'.format(self.person.name, self.title,
            get_name_or_b(self.organization, self.organization_url))
        
class Investment(Base):
    """Represent an Investment a Person has done"""
    __tablename__ = 'tbl_Investment'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'))
    organization_url = Column(VARCHAR(255), nullable=False)
    date = Column(Date)

    person = relationship('Person', back_populates='jobs')
    organization = relationship('Organization')

    def __repr__(self):
        return '{} invested in {} in {}'.format(self.person.name,
            get_name_or_b(self.organization, self.organization_url),
            self.date)
        
class Education(Base):
    """Represent an Educational experience a Person has"""
    __tablename__ = 'tbl_Education'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'))
    organization_url = Column(VARCHAR(255), nullable=False)
    period = Column(VARCHAR(64))
    
    person = relationship('Person', back_populates='jobs')
    organization = relationship('Organization')

    def __repr__(self):
        return '{} studied in {}'.format(self.person.name,
            get_name_or_b(self.organization, self.organization_url))
        
class Organization(Base):
    """Represent an Organization in Crunchbase"""
    __tablename__ = 'tbl_Organization'

    id = Column(Integer, primary_key=True)
    name = Column(NVARCHAR(255), nullable=False)
    url = Column(VARCHAR(255), nullable=False, unique=True)
    ipo_date = Column(Date)
    stock_code = Column(VARCHAR(10))
    headquarters = Column(VARCHAR(64))
    description = Column(TEXT)
    categories = Column(VARCHAR(64))
    website = Column(VARCHAR(255))
    facebook = Column(VARCHAR(255))
    twitter = Column(VARCHAR(255))
    linkedin = Column(VARCHAR(255))
    found_date = Column(Date)
    aliases = Column(VARCHAR(64))

    acquisitions = relationship('Acquisition', back_populates='organization')
    founders = relationship('Founder', back_populates='organization')
    employees = relationship('Employee', back_populates='organization')
    competitors = relationship('Competitor', back_populates='focal_company')
    partners = relationship('Partner', back_populates='focal_company')
    board_members = relationship('BoardMember', back_populates='company')

    def __repr__(self):
        return self.name

class Acquisition(Base):
    """Represent an Acquisition done by an Organization"""
    __tablename__ = 'tbl_Acquisition'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    acquired_organization_id = Column(Integer, ForeignKey('tbl_Organization.id'))
    acquired_organization_url = Column(VARCHAR(255), nullable=False)
    date = Column(Date)

    organization = relationship('Organization', back_populates='acquisitions')

    def __repr__(self):
        return '{} acquired by {} in {}'.format(self.acquired_organization_url,
            self.organization.name, self.date)
        
class Founder(Base):
    """Represent a founding relationship between a person and an organization"""
    __tablename__ = 'tbl_Founder'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'))
    person_url = Column(VARCHAR(255), nullable=False)

    person = relationship('Person')
    organization = relationship('Organization', back_populates='founders')

    def __repr__(self):
        return '{} founded {}'.format(
            get_name_or_b(self.person, self.person_url), self.organization.name)
        
class Employee(Base):
    """Represent a relationship of an organization and its employees"""
    __tablename__ = 'tbl_Employee'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'))
    person_url = Column(VARCHAR(255), nullable=False)
    title = Column(VARCHAR(64))

    person = relationship('Person')
    organization = relationship('Organization', back_populates='employees')

    def __repr__(self):
        return '{}, {} at {}'.format(
            get_name_or_b(self.person, self.person_url), self.title,
            self.organization.name)
        
class Competitor(Base):
    """Represent competition relationship between organizations"""
    __tablename__ = 'tbl_Competitor'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    competitor_organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    competitor_url = Column(VARCHAR(255), nullable=False)

    focal_company = relationship('Organization', back_populates='competitors')

    def __repr__(self):
        return '{} competes with {}'.format(self.focal_company.name, self.competitor_url)
        
class Partner(Base):
    """Represent partnership between organizations"""
    __tablename__ = 'tbl_Partner'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    partner_organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    partner_url = Column(VARCHAR(255), nullable=False)

    focal_company = relationship('Organization', back_populates='partners')

    def __repr__(self):
        return '{} and {} are partners'.format(self.focal_company.name, self.partner_url)
        
class BoardMember(Base):
    """Represent relationship between a Person and an Organization at which that
    Person is a board member"""
    __tablename__ = 'tbl_BoardMember'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('tbl_Organization.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('tbl_Person.id'))
    person_url = Column(VARCHAR(255), nullable=False)
    title = Column(VARCHAR(64))

    person = relationship('Person')
    organization = relationship('Organization', back_populates='employees')

    def __repr__(self):
        return '{} has {} as a board member'.format(self.organization.name,
            get_name_or_b(self.person, self.person_url))
        

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://crunchbase@localhost/crunchbase', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
