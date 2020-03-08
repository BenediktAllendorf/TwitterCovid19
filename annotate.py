import json
import argparse
import os
import time
import logging
from spotlight import SpotlightException

from twittersql.database import tweets_without_concepts, update_tweet_concepts
from twittersql.spotlight import clean_tweet, get_annotation


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', action='store_true')
    return parser.parse_args()

def read_regions(path=os.path.join('regions.json')):
    """Load regions JSON file"""
    with open(path, 'r') as f:
        regions = json.load(f)
    return regions

def main():

    args = parse_args()

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("annotate.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    if not args.quiet:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)

    regions = read_regions()

    for region in regions:
        logger.info(region)
        language = regions[region]['language']
        twc = tweets_without_concepts(region)
        amount = len(list(twc))
        logger.info("{} tweets to annotate".format(amount))
        time.sleep(1)

        # loop over tweets and annotate them and write back into the db with the JSON response
        for index, tweet in enumerate(twc):
            tweet_id = tweet.tweet_id
            text = tweet.tweet_body.get('text')
            clean = clean_tweet(text)
            try:
                r = get_annotation(language=language, text=clean)
            except SpotlightException as e:
                logger.warning(e)
            else:
                logger.info("{}/{} - Inserting concepts for tweet {} into db".format(index, amount, tweet_id,))
                update_tweet_concepts(tweet_id, r)
                forms = ', '.join([t['surfaceForm'] for t in r])
                logger.info("{}/{} - tweet_id: {} - forms: {}".format(index, amount, tweet_id, forms))



if __name__ == '__main__':
    main()