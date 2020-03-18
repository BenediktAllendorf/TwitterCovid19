# TwitterCovid19

Project to analyze Twitter during the onset of the COVID-19 outbreak in the Netherlands.

This repository is to load Tweets from Search API to JSON files and load them into a PostgreSQL database as JSONB.
The accompanying repository for analysis is located at [davidhuser/TwitterCovid19-analysis](https://github.com/davidhuser/TwitterCovid19-analysis).


## Cloud server provision guide
See [docs/os_provision.md](docs/os_provision.md) to set up DBPedia instances and allow remote connections to the database.

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