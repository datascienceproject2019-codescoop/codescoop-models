#!/usr/bin/env bash

DUMP_DATE=$1

if [ -z "$DUMP_DATE" ]; then
  echo "No DUMP_DATE given as first argument!"
  exit 1
fi

echo "#################### HOW TO RESTORE ######################"
echo "Provide sufficient CPU and RAM to your Docker Engine."
echo "What is sufficient? Well.. maybe at least 2 CPUs and 4 GBs RAM"
echo "Type the following to the mysql prompt:"
echo "source /gh_maria_dumps/$DUMP_DATE/mysql-$DUMP_DATE.sql;"
echo "##########################################################"

mysql -u github-user -pgithub-pass github
