#!/usr/bin/env bash

COMMAND=$1
DUMP_DATE=$2

if [ -z "$DUMP_DATE" ]; then
  DUMP_DATE="2015-12-02" # Default MongoDB dump
  # DUMP_DATE="2014-01-02" # Default MySQL dump
fi

case "$1" in
  all:start)
    docker-compose up
    ;;
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
  mongo:unzip:all)
    # Not used since uncompressing everything will generate ~26 GBs of files
    cd gh_mongo_dumps/$DUMP_DATE
    tar -xzvf mongo-dump-$DUMP_DATE.tar.gz
    cd ../..
    ;;
  mongo:unzip)
    # Untars only collection metadatas since they are small and *can't* be otherwise restored with the
    # mongorestore command. Yes, this is crazy messy. But I don't make the rules. :DD
    cd gh_mongo_dumps/$DUMP_DATE
    tar xzvf mongo-dump-$DUMP_DATE.tar.gz *.json
    cd ../..

    echo "Now extracts the filepaths from the tarball"
    # After extracting the metadata, view the files inside the tarball and grep the BSON file paths
    # since they are required for tar to stream the single files to the mongorestore.
    # 1. List all the files inside the tarball
    # 2. Grep all the bson files 
    # 3. Print out their filepaths
    # 4. Save the results into files.txt
    tar ztvf gh_mongo_dumps/$DUMP_DATE/mongo-dump-$DUMP_DATE.tar.gz \
      | grep bson \
      | awk '{print $9}' \
      > gh_mongo_dumps/$DUMP_DATE/files.txt
    ;;
  mongo:restore)
    # Restores first the metadatas
    docker-compose exec ghmongo mongorestore /gh_mongo_dumps/$DUMP_DATE/dump/github -d github -u github-user -p github-pass

    # Then the really messy part of streaming single BSON files directly into the mongorestore command.
    # This way we are avoiding the extraction of the files which would result in temporarily duplication of
    # very large files. Sure maybe you could extract them one by one and then delete them as they restored, I don't know.
    # This is how it works now. :)

    # Execute the restore script inside the container as a separate script since piping to docker exec
    # doesn't really work as well as I'd like to.
    # It will read the file paths of the BSON files from the files.txt and then one by one:
    # 1. Extract the collection name
    # 2. Untar it and stream it to STDIN
    # 3. Pipe it to mongorestore
    docker-compose exec ghmongo bash ./gh_mongo_scripts/restore.sh $DUMP_DATE
    ;;
  mongo:bash)
    docker-compose exec ghmongo bash
    ;;
  mongo:shell)
    docker-compose exec ghmongo mongo github -u github-user -p github-pass
    ;;
  maria:start)
    docker-compose up ghmaria
    ;;
  maria:delete)
    docker-compose -f mariadb-stack.yml rm
    rm -r gh_maria_data
    ;;
  maria:getdump)
    mkdir -p gh_maria_dumps/$DUMP_DATE
    cd gh_maria_dumps/$DUMP_DATE
    echo "NOTE: use browser to download this if your download speed is very low, it might fail otherwise"
    curl -O http://ghtorrent-downloads.ewi.tudelft.nl/mysql/mysql-$DUMP_DATE.sql.gz
    cd ../..
    ;;
  maria:unzip)
    cd gh_maria_dumps/$DUMP_DATE
    tar -xzvf mysql-$DUMP_DATE.sql.gz
    cd ../..
    ;;
  maria:restore)
    docker-compose exec ghmaria bash ./gh_maria_scripts/restore.sh $DUMP_DATE
    ;;
  maria:restore:gz)
    docker-compose exec ghmaria zcat /gh_maria_dumps/$DUMP_DATE/mysql-$DUMP_DATE.sql.gz | mysql -u github-user -pgithub-pass github
    ;;
  maria:bash)
    docker-compose exec ghmaria bash
    ;;
  maria:shell)
    docker-compose exec ghmaria mysql -u github-user -pgithub-pass github
    ;;
  *)
    echo $"Command '$1' not found, usage: $0 [service:action] [?dump_date eg 2015-12-02]"
    exit 1
esac
