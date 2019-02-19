#!/usr/bin/env bash

DUMP_DATE=$1

if [ -z "$DUMP_DATE" ]; then
  echo "No DUMP_DATE given as first argument!"
  exit 1
fi

cat gh_maria_scripts/init-db.sql | mysql -uroot || true

echo "#################### HOW TO RESTORE ######################"
echo "Type the following to the mysql prompt:"
echo "source gh_maria_dumps/$DUMP_DATE/mysql-$DUMP_DATE.sql;"
echo "##########################################################"

mysql -u github-user -pgithub-pass github
