from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql.json import JSONB


Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(String(100), primary_key=True)
    tweet_body = Column(JSONB)
    inserted = Column(DateTime, default=datetime.now)
    location_id = Column(String(100))
    location_query = Column(String(100))
