#!/usr/bin/env bash

DB=oos.sqlite
FILE=schema.sql

if [[ -e "$DB" ]]; then
    echo "db '$DB' already exists, deleting"
    rm -rf "$DB"
fi

echo "creating database '$DB'"
sqlite3 "$DB" < "$FILE"

echo "success"

