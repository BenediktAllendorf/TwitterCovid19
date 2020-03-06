# TwitterCovid19

Load Tweets from Search API to JSON files and load them into a PostgreSQL database as JSONB.

TODO:

* merge with Tweet streaming component, or use separate repository / running on cronjob
* use proper logging
* think about triggering (systemd service, cronjob)
* how to identify tweet location (store it / analyze tweet if possible) -> tagging to a db field based on the search query location

## Setup the database
See [docs/os_provision.md](docs/os_provision.md)


## Parsing tweets from Twitter Search API to JSON
* copy `settings.dist.json` to `settings.json`and insert twitter credentials
* all regions to scrape should be in `regions.json` (and be commited to git)
* run `load_tweets.py $regionName` to start scraping backward from the current time (this will detect if tweets are reached that have been scraped. Then the script stops)
* run `load_tweets.py $regionName --resume` to start scraping backward from the oldest tweet
* add `--no_output` to prevent any logs being printed to the console

## Loading JSON into database

* run `load_to_database.py $regionName` to load the respective files into the database

## Annotating tweets

* run `annotate.py $regionName` to annotate tweets in the database with DBPedia Spotlight