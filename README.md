# Data Science Project 2019 Spring: Project Codescoop: Models

This repository contains the scripts and files used to download and run our models for our data science project.

# How to use

## Prerequisites

Download Docker, Docker Compose. Make sure your file sharing is on for this folder (so Docker can mount this directory for the containers). Also you'll need ~35 GBs free space for the MongoDB shenanigans. As of now I don't know how to restore the Mongo database without unzipping the dump (dump 4.2 GB and 26 GB unzipped).

If you're using Windows *and* Docker Toolbox I feel sorry for you.

## MongoDB

This database contains GitHub event data from here http://ghtorrent.org/downloads.html. It's schema is described here http://ghtorrent.org/files/schema.pdf and the corresponding GitHub API URLs here http://ghtorrent.org/mongo.html (with examples if you click the "Documentation URL" eg https://developer.github.com/v3/repos/comments/#list-comments-for-a-single-commit).

1) Start up the database: `docker-compose up ghmongo` or `./commands mongo:start`
2) Download the second smallest dump (still 4.2 GB, uncompressed 26 GB :DD): `./commands.sh mongo:getdump`
3) We'll need to uncompress the downloaded tar.gz file as I couldn't figure out a better way. Inspired by the scripts here https://gist.github.com/gousiosg/e16f4348d64fb907e5d8306401f36fa6 you'll need to run only `./commands mongo:unzip` to let the magic happen. NOTE: you need to have 26 GB free space for the files. Also I ran this with my Macbook Pro's SSD. If you have HDD I don't know how long it will take. =) To view the size of the dumps afterwards in macOS: `du -hd1`.
4) Restore the dump: `./commands.sh mongo:restore`
5) Open up the shell to see if it worked: `./commands.sh mongo:shell`. Run `db.forks.count()` and if the number is non-zero hurray! You can now start getting lost into MongoDB documentation.

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

