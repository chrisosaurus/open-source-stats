#!/usr/bin/env bash

set -e

./scripts/create.sh

./src/update_projects.py

DB=oos.sqlite
FILE=schema.sql

#echo "select * from project_stats order by project_id, month asc;" | sqlite3 "$DB"

./src/generate_data.py

echo 'output generated to `site/index.html`, attempting to open in browser';

chromium site/index.html

