# Data Science Project 2019 Spring: Project Codescoop: Models

This repository contains the scripts and files used to download and run our models for our data science project.

# How to use

## Prerequisites

Download Docker, Docker Compose. Make sure your file sharing is on for this folder (so Docker can mount this directory for the containers). Also you'll need ~35 GBs free space for any of GHTorrent's database shenanigans.

If you're using Windows *and* Docker Toolbox I feel sorry for you.

# About the datasets

GHTorrent author's (and I) recommend using MySQL for the basic stuff. The MySQL version holds the basic structure of the Github's knowledge graph while the MongoDB includes the full JSON responses with commit texts(?) and whatnot. The full MySQL data is couple TBs(?) while the MongoDB is dozen TBs(?). To run the queries against the up-to-date data we could use already available Google Cloud's BigQuery GHTorrent dataset *BUT* it requires either a lot of free credits or big amount of money

LOL  
https://cloud.google.com/bigquery/pricing
>Queries (analysis)  
>$5.00 per TB  
>First 1 TB per month is free, see On-demand pricing for details. Flat-rate pricing is also available for high-volume customers.

## MySQL

This database contains GitHub event data from here http://ghtorrent-downloads.ewi.tudelft.nl/mysql/.

## MongoDB

This database contains GitHub event data from here http://ghtorrent.org/downloads.html. It's schema is described here http://ghtorrent.org/files/schema.pdf and the corresponding GitHub API URLs here http://ghtorrent.org/mongo.html (with examples if you click the "Documentation URL" eg https://developer.github.com/v3/repos/comments/#list-comments-for-a-single-commit).

1) Start up the database: `docker-compose up ghmongo` or `./commands mongo:start`
2) Download the second smallest dump (still 4.2 GB, uncompressed 26 GB :DD). Date is optional variable, we're using the second smallest dataset of 2015-12-02 as the default: `./commands.sh mongo:getdump [?date]`
3) We'll need to uncompress the downloaded tar.gz file BUT since it's sooper larger we'll only unzip the metadatas and then untar the BSON files as separate command piping the contents directly to mongorestore. This will avoid the temporal duplication of the data (to 60 GBs). Inspired by the scripts here https://gist.github.com/gousiosg/e16f4348d64fb907e5d8306401f36fa6 Unzip the metadata with: `./commands mongo:unzip [?date]`
5) Restore the dump from the metadatas and the BSON files: `./commands.sh mongo:restore [?date]`
6) Open up the shell to see if it worked: `./commands.sh mongo:shell`. Run `db.forks.count()` and if the number is non-zero hurray! You can now start getting lost into MongoDB documentation.

I ran this using my MacBookPro with SSD and stuff so with less powerful machine it might take longer. To view the size of the folders afterwards in macOS you can use: `du -hd1`.

To delete the database, run: `./commands.sh mongo:delete`. Otherwise the data will be persisted on disk even when the MongoDB instance is destroyed.

### Mongo shell

Is a Javascript based command line shell for directly running Mongo commands (like psql).

Open it with: `./commands.sh mongo:shell`

Some useful commands:
* `db.adminCommand('listDatabases')` will list all the databases, github is the restored data.
* `db.getCollectionNames()` will list all the collections in the database.
* `db.forks.count()` count items in collection `forks`.
* `db` shows the current database you're using.
* `var forks = db.forks.find()` fetches all documents from `forks` and stores them into a variable. `forks[0]` will display the first item.

