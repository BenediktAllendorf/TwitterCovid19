import json
import argparse
import pickle
import os
import time
import logging
from spotlight import SpotlightException
from requests import RequestException

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

    # set of tweet id where resources were not found
    try:
        with open('no_resources_found.pickle', 'rb') as f:
            no_resources_found = pickle.load(f)
    except (FileNotFoundError, OSError):
        no_resources_found = set()

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

            if tweet_id not in no_resources_found:
                text = tweet.tweet_body.get('text')
                clean = clean_tweet(text)
                try:
                    r = get_annotation(language=language, text=clean)
                except SpotlightException as e:
                    logger.warning(e)
                    no_resources_found.add(tweet_id)
                except RequestException as e:
                    logger.error(e)
                else:
                    update_tweet_concepts(tweet_id, r)
                    forms = ', '.join([t['surfaceForm'] for t in r])
                    logger.info("{}/{} - tweet_id: {} - forms: {}".format(index, amount, tweet_id, forms))
        else:
            with open('no_resources_found.pickle', 'wb') as f:
                pickle.dump(no_resources_found, f)


if __name__ == '__main__':
    main()