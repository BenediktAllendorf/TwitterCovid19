# TwitterCovid19

Load Tweets from Search API into a PostgreSQL database as JSONB.

Check `docs` folder.

TODO:

* merge with Tweet streaming component, or use separate repository / running on cronjob
* use proper logging
* think about triggering (systemd service, cronjob)

## Setup
* copy `settings.dist.json` to `settings.json`and insert twitter credentials
* all regions to scrape should be in `regions.json` (and be commited to git)
* run `scrape.py $regionName` to start scraping backward from the current time (this will detect if tweets are reached that have been scraped. Then the script stops)
* run `scrape.py $regionName --resume` to start scraping backward from the oldest tweet
