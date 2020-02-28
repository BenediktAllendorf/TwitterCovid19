# TwitterCovid19

Load Tweets from Search API into a PostgreSQL database as JSONB.

Check `docs` folder.

TODO:

* merge with Tweet streaming component, or use separate repository / running on cronjob
* use proper logging
* think about triggering (systemd service, cronjob)
* how to identify tweet location (store it / analyze tweet if possible)