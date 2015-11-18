#!/usr/bin/env sh

set -e

DB=oos.sqlite
FILE=schema.sql

echo "opening database '$DB'"
sqlite3 "$DB"


