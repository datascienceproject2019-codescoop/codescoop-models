#!/usr/bin/env bash

COMMAND=$1
DUMP_DATE=$2

if [ -z "$DUMP_DATE" ]; then
  DUMP_DATE="2015-12-02" # Default dump
fi

case "$1" in
  mongo:start)
    docker-compose up ghmongo
    ;;
  mongo:delete)
    docker-compose down && rm -r ./gh_mongo_data
    ;;
  mongo:getdump)
    mkdir -p gh_mongo_dumps/$DUMP_DATE
    cd gh_mongo_dumps/$DUMP_DATE
    curl -O http://ghtorrent-downloads.ewi.tudelft.nl/mongo-daily/mongo-dump-$DUMP_DATE.tar.gz
    cd ../..
    ;;
  mongo:unzip)
    cd gh_mongo_dumps/$DUMP_DATE
    tar -xzvf mongo-dump-$DUMP_DATE.tar.gz
    cd ../..
    ;;
  mongo:restore)
    docker-compose exec ghmongo mongorestore /gh_mongo_dumps/$DUMP_DATE/dump/github/ -d github -u github-user -p github-pass
    ;;
  mongo:load)
    # zcat gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz | docker-compose exec ghmongo mongorestore -u mongo-admin -p mongo-pass -
    # zcat < gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz | docker-compose exec ghmongo mongorestore -u mongo-admin -p mongo-pass -
    # docker-compose exec ghmongo echo "gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz" > gh_mongo_dumps/asdf.txt
    # docker-compose exec ghmongo zcat "gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz" > gh_mongo_dumps/asdf.txt
    docker-compose exec ghmongo zcat "gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz" > ghmongo mongorestore -u mongo-admin -p mongo-pass -
    # tar xvzf gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz | docker-compose exec ghmongo mongorestore -u mongo-admin -p mongo-pass -    
    ;;
  mongo:shell)
    docker-compose exec ghmongo mongo github -u github-user -p github-pass
    ;;
  *)
    echo $"Command '$1' not found, usage: $0 [service:action] [?dump_date eg 2015-12-02]"
    exit 1
esac
