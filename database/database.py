from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = 'admin:admin'
HOST = '127.0.0.1'
DB_NAME = 'tweets'

engine = create_engine('postgresql://{}@{}/{}'.format(DB_USER, HOST, DB_NAME))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import database.model
    Base.metadata.create_all(bind=engine)