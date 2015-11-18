#!/usr/bin/env bash

./scripts/create.sh

./src/update_projects.py

DB=oos.sqlite
FILE=schema.sql

#echo "select * from project_stats order by project_id, month asc;" | sqlite3 "$DB"

./src/generate_data.py

chromium site/index.html

