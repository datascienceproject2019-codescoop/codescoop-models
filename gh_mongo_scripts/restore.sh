#!/usr/bin/env bash

DUMP_DATE=$1

if [ -z "$DUMP_DATE" ]; then
  echo "No DUMP_DATE given as first argument!"
  exit 1
fi

while read FILEPATH; do
  COLLECTION=$(basename $FILEPATH .bson)
  tar xOf /gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz $FILEPATH \
    | mongorestore -d github -c $COLLECTION -u github-user -p github-pass -
done </gh_mongo_dumps/$DUMP_DATE/files.txt
