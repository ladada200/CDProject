# Retrievr
### What is this project?
Welcome to the Retrievr; produced and created by Retrievr Labs.

### Who is Retrievr Labs?
1. Christopher Rupert

Checkout the wiki here! [https://github.com/ladada200/Retrievr/wiki](https://github.com/ladada200/Retrievr/wiki)

### Who is Retrievr Labs?
1. Christopher Rupert.

### Version:
1.0.0.20.9.4.a



### Setup / Configuration
When cloning this inside of the config folder will be a template.cfg file;  This file will need to be copied, modified (with your parameters) and renamed to local.cfg to work.

If for some reason this template does not exist; here is the structure.

```
[HOST]
HOST_PORT="8080"                              # change if different
HOST_HTTPS=False                            # set to True to use HTTPS
HOST_NAME=localhost                         # by default is localhost
HOST_FS=localhost                           # change if using S3
HOST_RDP_PORT=8069                          # change if different; used for RDP/RPC Communication


[DB]
DB_HOST=localhost                           # change if not localhost
DB_PORT=5432                                # change if different
DB_USERNAME=dbadmin                         # change if different
DB_PASSWORD=pass                            # change if different
DB_NAME=Retrievr                           # name of database to use once connected to DB.

[SONG_FORMAT]
SONG_STORE="AUDIO/{artist}/{album}/{song}"
SONG_DISPLAY_FORMAT="{song} - {artist} - {album} - {year}/{month}/{day} - {length}"
SONG_RATING="{score} out of 5"
SONG_TAGS="{tags}"

[ADMIN]
ADMIN_USER="administrator@Retrievr.com"    # admin user
ADMIN_PASS="changeme1234"                   # admin password

[DEBUG]
DEBUG=True                                  # Debug mode enabled
```

### DB Scripts:
These scripts are contained under Postgresql and should be used to setup the postgres DB once.  Revisions may occur in the future; please be aware that this is a work in progress only.
