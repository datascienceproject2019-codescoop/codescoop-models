# Data Science Project 2019 Spring: Project Codescoop: Models

This repository contains the scripts and files used to download and run our models for our data science project.

NOTE: some scripts might not work as they should. Please tell me (Teemu) about it.

**Table of Contents**

<!-- toc -->

- [Data Science Project 2019 Spring: Project Codescoop: Models](#data-science-project-2019-spring-project-codescoop-models)
- [How to use](#how-to-use)
  - [Prerequisites](#prerequisites)
  - [About the datasets](#about-the-datasets)
- [GHTorrent](#ghtorrent)
  - [MySQL/MariaDB](#mysqlmariadb)
  - [Local installation](#local-installation)
  - [Using Docker](#using-docker)
  - [MySQL shell](#mysql-shell)
  - [MongoDB](#mongodb)
  - [Mongo shell](#mongo-shell)
- [Jupyter](#jupyter)
  - [Requirements](#requirements)
  - [How to install](#how-to-install)
  - [How to use](#how-to-use-1)

<!-- tocstop -->

# How to use

## Prerequisites

Download Docker, Docker Compose. Make sure your file sharing is on for this folder (so Docker can mount this directory for the containers). Also you'll need ~20 GBs free space for any of GHTorrent's database shenanigans.

If you're using Windows *and* Docker Toolbox I feel sorry for you.

## About the datasets

GHTorrent author's (and I) recommend using MySQL for the basic stuff. The MySQL version holds the basic structure of the Github's knowledge graph while the MongoDB includes the full JSON responses with commit texts(?) and whatnot. The full MySQL data is couple TBs(?) while the MongoDB is dozen TBs(?). To run the queries against the up-to-date data we could use already available Google Cloud's BigQuery GHTorrent dataset *BUT* it requires either a lot of free credits or big amount of money

LOL  
https://cloud.google.com/bigquery/pricing
>Queries (analysis)  
>$5.00 per TB  
>First 1 TB per month is free, see On-demand pricing for details. Flat-rate pricing is also available for high-volume customers.

# GHTorrent

## MySQL/MariaDB

This database contains GitHub event data from here http://ghtorrent-downloads.ewi.tudelft.nl/mysql/.

This is ridiculously slow either way you do it; locally or with Docker. I think using either one is fine. Now I have written two versions just to confuse people. Idk.

## Local installation

1) Install MariaDB to your local machine, mine was 10.3 and it worked fine. If you're on macOS I recommend brew: `brew install mariadb`
2) Get the dump, probably you should download it using your browser since curl hangs up at times for some reason. I'm using dump of `2014-01-02` http://ghtorrent-downloads.ewi.tudelft.nl/mysql
3) I recommend unzipping the data to see the actual queries being run and also you can continue a stopped restoration. The unzipped data will be 24 GBs *and* the database once restored at least 12 GBs. Of course do it only if you can afford using extra 24 GBs: `./cmd.sh maria:unzip 2014-01-02`
4) Run the script: `./gh_maria_scripts/local-restore.sh 2014-01-02`.
5) Type in the command similar to `source gh_maria_dumps/2014-01-02/mysql-2014-01-02.sql;`. This will generate x amount of data. Without unzipping just run `DUMP_DATE=2014-01-02 cat gh_maria_scripts/init-db.sql | mysql -uroot || true && zcat gh_maria_dumps/$DUMP_DATE/mysql-$DUMP_DATE.sql.gz | mysql -u github-user -pgithub-pass github`.
6) See if it has worked: `mysql -u github-user -pgithub-pass github` and execute: `select language,count() from projects where forked_from is null group by language;`. If it returns something, great! You are now a MySQL expert.
7) When you no longer need the data run `./gh_maria_scripts/local-delete.sh` to delete it.

## Using Docker

1) Start up the database: `./cmd.sh maria:start`
2) Download the second smallest dump of `2014-01-02` (5.5 GB): `./cmd.sh maria:getdump 2014-01-02`
3) Either unzip (24 GBs) and restore the data so you can see the actual progress and continue a stopped restoration: `./cmd.sh maria:unzip 2014-01-02` and `./cmd.sh maria:restore 2014-01-02`. Or just stream the gzip directly to mysql: `./cmd.sh maria:restore:gz`.
4) See if it has worked: `./cmd.sh maria:shell` and execute: `select language,count() from projects where forked_from is null group by language;`. If it returns something, great! You are now a MySQL expert.

## MySQL shell

Open it with `mysql -u github-user -pgithub-pass github` if you have a local installation, with Docker `./cmd.sh maria:shell`.

Some useful commands:
* `\q` exits the shell.

## MongoDB

This database contains GitHub event data from here http://ghtorrent.org/downloads.html. It's schema is described here http://ghtorrent.org/files/schema.pdf and the corresponding GitHub API URLs here http://ghtorrent.org/mongo.html (with examples if you click the "Documentation URL" eg https://developer.github.com/v3/repos/comments/#list-comments-for-a-single-commit).

The restoring with direct piping took me 3 hours with my MacBook Pro. Total size of data was with default dump 4.2 GB tarball + 8.9 GB as MongoDB data. Also the MongoDB docker image is 400 MB. So you should have at least (preferably well over) 13.5 GB of free space.

1) Start up the database: `docker-compose up ghmongo` or `./cmd.sh mongo:start`
2) Download the second smallest dump (still 4.2 GB, uncompressed 26 GB :DD). Date is optional variable, we're using the second smallest dataset of 2015-12-02 as the default: `./cmd.sh mongo:getdump [?date]`

Well since I wanted to make things difficult I avoided the extraction of the data by directly uncompressing the tarball BSON files to mongorestore thus avoiding the 26 GB extra stuff on disk. BUT the problem is it takes a lot longer with streaming. But anyway.

3) To avoid extracting the large BSON files, extract only the metadatas. We however have to grep the filenames of those BSON files which is why this takes a while. Unzip the metadata with: `./cmd.sh mongo:unzip [?date]`
4) Restore the dump from the metadatas and the BSON files: `./cmd.sh mongo:restore [?date]`
5) Open up the shell to see if it worked: `./cmd.sh mongo:shell`. Run `db.commits.count()` and if the number is 932677 hurray! You can now start getting lost into MongoDB documentation.

I ran this using my MacBook Pro with SSD and stuff so with less powerful machine it might take longer. To view the size of the folders afterwards in macOS you can use: `du -hd1`.

To delete the database, run: `./cmd.sh mongo:delete`. Otherwise the data will be persisted on disk even when the MongoDB instance is destroyed.

## Mongo shell

Is a Javascript based command line shell for directly running Mongo commands (like psql).

Open it with: `./cmd.sh mongo:shell`

Some useful commands:
* `db.adminCommand('listDatabases')` will list all the databases, github is the restored data.
* `db.getCollectionNames()` will list all the collections in the database.
* `db.forks.count()` count items in collection `forks`.
* `db` shows the current database you're using.
* `var forks = db.forks.find()` fetches all documents from `forks` and stores them into a variable. `forks[0]` will display the first item.

# Jupyter

So we are using Jupyter to create and run our models.

## Requirements

Python 3, virtualenv installed. Also either the MongoDB or MySQL dump restored. TODO: Use Github API

## How to install

1) Generate a virtualenv environment: `./jupyter.sh venv:create`. Or you install without it, your call.
2) Activate it by pasting this script's output to terminal: `./jupyter.sh venv`
3) Install the requirements: `./jupyter.sh pip:install`
4) Start the notebook: `./jupyter.sh notebook`. It should appear at http://localhost:8888

## How to use

There's a GHTorrent sandbox notebook inside the `notebooks` folder. You can play with that.

When you add new libraries don't forget to save the updated dependencies: `./jupyter pip:save`