import os
import time
import json

from twittersql.database import init_db
from twittersql.utils import find_json_files, load_json
from twittersql.database import write_tweet

JSON_FOLDER = os.path.join('tweets', 'unprocessed')

def read_regions(path=os.path.join('regions.json')):
    """Load regions JSON file"""
    with open(path, 'r') as f:
        regions = json.load(f)
    return regions

def main():
    regions = read_regions()
    print("Files folder: '{}' Region: '{}'".format(JSON_FOLDER, regions))
    time.sleep(4)

    # Set up database
    init_db()

    for region in regions:
        geocode = regions[region]['geocode']

        iterator = find_json_files(JSON_FOLDER, region)

        amount = len(list(iterator))
        print("Region: {} - {} JSON files found".format(region, amount))
        time.sleep(2)

        for index, file in enumerate(find_json_files(JSON_FOLDER, region)):
            data = load_json(file)
            unique = write_tweet(data, region, geocode)
            if unique:
                print("{}/{} - imported tweet into db: {}".format(index, amount, file))
            #else:
            #print("{}/{} - Duplicate tweet: {}".format(index, amount, file))

if __name__ == '__main__':
    main()