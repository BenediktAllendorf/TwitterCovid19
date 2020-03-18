# Installation

## PostgreSQL 11

Install PostgreSQL-11 for Ubuntu 18.04 LTS https://www.postgresql.org/download/linux/ubuntu/

```bash
sudo apt install postgresql-11

# save password you enter:
sudo -u postgres createuser -SDRP ubuntu

# create db `tweets` for user admin
sudo -u postgres createdb -O ubuntu tweets
```

### Remote read-only connection

```bash
sudo -u postgres psql -d tweets
```

```sql
CREATE ROLE group11 WITH LOGIN PASSWORD 'tsw2020' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION VALID UNTIL 'infinity';
GRANT CONNECT ON DATABASE tweets TO group11;
GRANT USAGE ON SCHEMA public TO group11;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO group11;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO group11;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO group11;
```

In `/etc/postgresql/11/main/postgresql.conf` allow remote connections:

```bash
listen_addresses = '*'
```

and in `/etc/postgresql/11/main/pg_hba.conf` make to allow any IP address to connect:

```bash
# IPv4 local connections:
host    all             all             0.0.0.0/0            md5
```

finally: `sudo service postgresql restart`

## Firewall

To lock down the server and allow only SSH and DB connections:
```bash
sudo ufw allow ssh
sudo ufw allow 5432/tcp
sudo ufw enable
```

Now the DB should be open for the read-only user `group11` via IP connections.

## Deploy

Clone repo to server and install Python 3 requirements
```bash
sudo apt install python3-pip python3-dev libpq-dev
pip3 install --upgrade pip
pip3 install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## DBpedia
```bash
sudo apt install docker.io
(sudo) docker pull dbpedia/spotlight-english
(sudo) docker run -d -p 80:80 dbpedia/spotlight-english spotlight.sh
```
Replace `english` with e.g. `dutch` for other languages (see https://github.com/dbpedia-spotlight/spotlight-docker)
