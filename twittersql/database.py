from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import SQLAlchemyError

from .config import DB_NAME, DB_USER, HOST
from .model import Tweet

engine = create_engine('postgresql://{}@{}/{}'.format(DB_USER, HOST, DB_NAME))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def init_db():
    """Create table if it doesn't exist"""
    if not engine.has_table('tweet'):
        print("Creating table `tweet`...")
        Tweet.__table__.create(bind=engine)

def write_tweet(tweet, region_name, geocode):
    """Write unique tweet into database, discard duplicates"""
    tweet_id = str(tweet['id'])
    # check if tweet_id already exists
    duplicate = session.query(Tweet).filter(Tweet.tweet_id == tweet_id).one_or_none()
    if not duplicate:
        t = Tweet(tweet_id=tweet_id, tweet_body=tweet, location_id=region_name, location_query=geocode)
        try:
            session.add(t)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print("Error: {}".format(e))
        finally:
            session.close()
    else:
        print("duplicate tweet")

def tweets_without_concepts(region):
    """Get tweets from region where tweet.concepts is null"""
    return session.query(Tweet).filter(Tweet.concepts == None).filter(Tweet.location_id == region).all()

def update_tweet_concepts(tweet_id, concepts):
    """Update tweet with concepts. Concepts should be JSON serializable."""
    session.query(Tweet).filter(Tweet.tweet_id == tweet_id).update({Tweet.concepts: concepts})
    session.commit()
    #session.close()