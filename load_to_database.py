import os
import time

from twittersql.database import init_db
from twittersql.utils import find_json_files, load_json
from twittersql.database import write_tweet

JSON_FOLDER = os.path.join('tweets', 'unprocessed')

def main():
    print("Starting")

    # Set up database
    init_db()

    iterator = find_json_files(folder=JSON_FOLDER)

    amount = len(list(iterator))
    print("{} JSON files loaded".format(amount))
    time.sleep(2)

    for index, file in enumerate(find_json_files(folder=JSON_FOLDER)):
        data = load_json(file)
        write_tweet(data)
        print("{}/{} - imported tweet into db: {}".format(index, amount, file))

if __name__ == '__main__':
    main()