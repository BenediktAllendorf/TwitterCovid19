import os
import time
import json
import argparse

from twittersql.database import init_db
from twittersql.utils import find_json_files, load_json
from twittersql.database import write_tweet

JSON_FOLDER = os.path.join('tweets', 'unprocessed')
#JSON_FOLDER = os.path.join('sample') # dev

def parse_region():
    """Get the proper region and geocode from regions.json"""
    parser = argparse.ArgumentParser()
    parser.add_argument('region')
    args = parser.parse_args()

    with open('regions.json', 'r') as f:
        regions = json.load(f)

    region_name = args.region
    if region_name not in regions.keys():
        raise ValueError("Not a valid region:  {}".format(region_name))
    else:
        geo_code = regions[region_name].get('geocode')
    return region_name, geo_code

def main():
    region_name, geocode = parse_region()
    print("Files folder: '{}' Region: '{}' Geocode: '{}'".format(JSON_FOLDER, region_name, geocode))
    time.sleep(4)

    # Set up database
    init_db()

    iterator = find_json_files(JSON_FOLDER, region_name)

    amount = len(list(iterator))
    print("{} JSON files loaded".format(amount))
    time.sleep(2)

    for index, file in enumerate(find_json_files(JSON_FOLDER, region_name)):
        data = load_json(file)
        write_tweet(data, region_name, geocode)
        print("{}/{} - imported tweet into db: {}".format(index, amount, file))

if __name__ == '__main__':
    main()