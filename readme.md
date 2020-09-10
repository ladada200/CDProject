# Retrievr
### What is this project?
Welcome to the Retrievr; produced and created by Retrievr Labs.

### Who is Retrievr Labs?
1. Christopher Rupert

### Version:
1.0.0.20.9.4.a

1. Major
2. Minor
3. Rev.
4. Year
5. Month
6. Day
7. Build-state

#### Goals
1. Collect CD / Song information
2. Upload songs either to Postgres DB or S3 Bucket
3. Stream music tto browser
4. Act as single-page application
5. Basic security for back-end
6. Basic data encryption
7. Basic data compression for faster streaming (Gzip)

#### Goals - reaching
1. Include Lambda and Lambda layer if necessary for file upload

#### What can I find here?
Here will be posted my solutions and ideas to a very simple project; a streamable CD Library.

#### Who is this for?
This is designed for those of us with an intermediate skill level in python, javascript, JQuery, Postgres, CSS and HTML.

#### Are there any packages in here?
1. Postgresql
2. sqlalchemy
3. urllib3
4. flask

#### Release schedule?
Sadly there is no planned release schedule; or maintenance procedures; this is a hobby project first.

#### Why?
In my limited free time, during the wee hours of the morning when I can breathe and relax I use the opportunity to stay sharp.

This project for me is a way to sharpen, hone, and refine my skills without affecting my day-to-day workload.

The intent is to create a workable Spotify-like clone starting from my limited experience.


### Setup / Configuration
When cloning this inside of the config folder will be a template.cfg file;  This file will need to be copied, modified (with your parameters) and renamed to local.cfg to work.

If for some reason this template does not exist; here is the structure.

```
# [ Server ]
HOST_PORT=8080                              # change if different
HOST_HTTPS=False                            # set to True to use HTTPS
HOST_NAME=localhost                         # by default is localhost
HOST_FS=localhost                           # change if using S3
HOST_RDP_POST=8069                          # change if different; used for RDP/RPC Communication

# [ Database ]
DB_HOST=localhost                           # change if not localhost
DB_PORT=5000                                # change if different
DB_USERNAME=dbadmin                         # change if different
DB_PASSWORD=pass                            # change if different
DB_NAME=cdproject                           # name of database to use once connected to DB.

# [ Administrative ]
ADMIN_USER="administrator@cdproject.com"    # admin user
ADMIN_PASS="changeme1234"                   # admin password

```

### DB Scripts:
These scripts are contained under Postgresql and should be used to setup the postgres DB once.  Revisions may occur in the future; please be aware that this is a work in progress only.
