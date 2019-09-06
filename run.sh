#!/usr/bin/env bash

cp $HOME/web.kotek.co/myapp/subscribers.json $HOME/scripts/lunchScraper/data/subscribers.json

cd "${0%/*}"

$HOME/scripts/lunchScraper/venv/bin/python $HOME/scripts/lunchScraper/lunchscraper
