import json
import argparse
import os
import time

from twittersql.database import tweets_without_concepts, update_tweet_concepts
from twittersql.spotlight import clean_tweet, get_annotation

REGIONS = os.path.join('regions.json')


def parse_region(path):
    """Get the proper region and geocode and language from regions.json"""
    parser = argparse.ArgumentParser()
    parser.add_argument('region')
    args = parser.parse_args()

    with open(path, 'r') as f:
        regions = json.load(f)

    region_name = args.region
    if region_name not in regions.keys():
        raise ValueError("Not a valid region:  {}".format(region_name))
    else:
        geo_code = regions[region_name].get('geocode')
    language = regions[region_name].get('language')
    return region_name, geo_code, language

def main():
    region, geocode, language = parse_region(REGIONS)

    twc = tweets_without_concepts(region)
    amount = len(list(twc))
    print("{} Tweets to annotate".format(amount))
    time.sleep(2)

    # loop over tweets and annotate them and write back into the db with the JSON response
    for index, tweet in enumerate(twc):
        tweet_id = tweet.tweet_id
        text = tweet.tweet_body.get('text')
        clean = clean_tweet(text)
        r = get_annotation(language=language, text=clean)
        update_tweet_concepts(tweet_id, r)
        print("{}/{} - tweet_id: {} - annotated: {}".format(index, amount, tweet_id, json.dumps(r)))



if __name__ == '__main__':
    main()