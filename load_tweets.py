import argparse
import logging
import os
import sys
import time
from datetime import datetime
import json

import twitter
from twitter import TwitterHTTPError


def connect(settings):
    auth = twitter.oauth.OAuth(settings['oauth_token'], settings['oauth_token_secret'], settings['consumer_key'],
                               settings['consumer_secret'])
    return twitter.Twitter(auth=auth)


def scrape(twitter_api, query, region_name, min_id, max_id, resume=False, count=100):
    search_results = None
    while search_results is None or \
            (len(search_results['statuses']) > 0 and 'max_id' in search_results['search_metadata']):

        done = False
        while not done:
            try:
                search_results = twitter_api.search.tweets(q=query, count=count,
                                                           geocode=regions[region_name]['geocode'],
                                                           max_id=min_id)
                time.sleep(1)
                done = True
            except TwitterHTTPError as error:
                if error.response_data['errors'][0]['message'] == 'Rate limit exceeded':
                    logging.getLogger().warning('Sleep ...')
                    time.sleep(60 * 5)
                else:
                    raise error

        if len(search_results['statuses']) == 0:
            logging.getLogger().info('Got no results')
            continue

        newest_tweet = search_results['statuses'][0]
        oldest_tweet = search_results['statuses'][-1]
        logging.getLogger().info(
            'Results between ' +
            convert_twitter_datetime_str(oldest_tweet['created_at']).strftime(
                '%Y-%m-%d %H:%M:%S') +
            ' (' + oldest_tweet['id_str'] + ')'
                                            ' and ' +
            convert_twitter_datetime_str(newest_tweet['created_at']).strftime(
                '%Y-%m-%d %H:%M:%S') +
            ' (' + newest_tweet['id_str'] + ')'
        )

        for tweet in search_results['statuses']:
            save_tweet(region_name, tweet)

        save_status(region_name, min_id=oldest_tweet['id'], max_id=newest_tweet['id'])

        if min_id == oldest_tweet['id']:
            logging.getLogger().info('Reached end of available data')
            search_results['statuses'] = []
            continue

        min_id = oldest_tweet['id']
        logging.getLogger().info('Saved')

        if not resume and max_id is not None and max_id > oldest_tweet['id']:
            logging.getLogger().info('Reached last scraping')
            search_results['statuses'] = []


def convert_twitter_datetime_str(twitter_datetime_str):
    return datetime.strptime(twitter_datetime_str, '%a %b %d %H:%M:%S %z %Y')


def save_tweet(region_name, tweet):
    created_at = convert_twitter_datetime_str(tweet['created_at'])
    path = os.path.join(sys.path[0], 'tweets/unprocessed/' + region_name + '/' + created_at.strftime('%Y/%m/%d/%H/%M'))
    os.makedirs(path, exist_ok=True)

    with open(path + '/' + tweet['id_str'] + '.json', 'w') as file:
        file.write(json.dumps(tweet))


def save_status(region_name, min_id, max_id):
    path = os.path.join(sys.path[0], 'tweets/unprocessed/' + region_name)
    os.makedirs(path, exist_ok=True)

    with open(path + '/status.json', 'r+') as file:
        data = json.load(file)

        data['max_id'] = max_id if data['max_id'] is None or data['max_id'] < max_id else data['max_id']
        data['min_id'] = min_id if data['min_id'] is None or data['min_id'] > min_id else data['min_id']

        file.seek(0, 0)
        file.write(json.dumps(data))


if __name__ == '__main__':

    with open(os.path.join(sys.path[0], 'settings.json')) as file:
        settings = json.load(file)

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--resume', action='store_true',
                        help="Resume with latest min_id")

    parser.add_argument('-noo', '--no_output', action='store_true',
                        help="If set, nothing will be printed to the terminal.")

    parser.add_argument('region')
    parser.add_argument('-q', '--query', default=settings['default_query'])

    args = parser.parse_args()

    region_name = args.region
    query = args.query

    with open(os.path.join(sys.path[0], 'regions.json')) as file:
        regions = json.load(file)

    if region_name not in regions:
        logging.error('Region not known!?')
        exit(1)

    path = os.path.join(sys.path[0], 'tweets/unprocessed/' + region_name + '/')
    os.makedirs(path, exist_ok=True)

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("{0}/{1}.log".format(path, 'scrape'))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    if not args.no_output:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    if os.path.exists(os.path.join(sys.path[0], 'tweets/unprocessed/' + region_name + '/status.json')):
        with open(os.path.join(sys.path[0], 'tweets/unprocessed/' + region_name + '/status.json')) as file:
            data = json.load(file)
            min_id = data['min_id']
            max_id = data['max_id']
    else:
        min_id = None
        max_id = None

        with open(path + '/status.json', 'w') as file:
            file.write(json.dumps({'max_id': max_id, 'min_id': min_id}))

    rootLogger.info(
        'Scraping ' + ('(resume) ' if args.resume else '') + 'query="' + query + '", min_id=' +
        str(min_id) + ', max_id=' + str(max_id))

    scrape(connect(settings), query, region_name, min_id=min_id if args.resume else None, max_id=max_id,
           resume=args.resume)
    rootLogger.info('Done scraping')
