# On Ubuntu 18.04 LTS

- Install Postgres11 https://www.postgresql.org/download/linux/ubuntu/

```bash
sudo -u postgres createuser -SDRP admin
# then create pw

# create db for user admin
sudo -u postgres createdb -O admin tweets

# create read-only user for remote access
sudo -u postgres psql --file read_only_user.sql

```