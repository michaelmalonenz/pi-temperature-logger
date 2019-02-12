#!/bin/bash

if [ $(whoami) != 'root' ]; then
    echo "Please sudo this script (don't run it as root directly!)"
fi

sudo --user=postgres dropdb temperature
sudo --user=postgres createdb temperature
sudo --user=postgres psql --single-transaction --dbname=temperature --file=temperature_db.sql