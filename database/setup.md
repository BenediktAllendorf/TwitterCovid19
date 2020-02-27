# Database installation

## PostgreSQL 11

Install PostgreSQL-11 for Ubuntu 18.04 LTS https://www.postgresql.org/download/linux/ubuntu/

```bash
sudo apt install postgresql-11

# save password you enter:
sudo -u postgres createuser -SDRP admin

# create db `tweets` for user admin
sudo -u postgres createdb -O admin tweets

# create read-only user for remote access
sudo -u postgres psql --file read_only_user.sql
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

Now the DB should be open for the read-only user via IP connections.