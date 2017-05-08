from sqlalchemy import create_engine
from scraper.db import Base, CONN_URL

if __name__ == '__main__':
    engine = create_engine(CONN_URL, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
