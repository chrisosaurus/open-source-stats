#!/usr/bin/env bash

./create.sh

./update_projects.py

DB=oos.sqlite
FILE=schema.sql

echo "select * from project_stats;" | sqlite3 "$DB"

