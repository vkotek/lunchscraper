#!/usr/bin/env bash

cp $HOME/web.kotek.co/myapp/subscribers.json $HOME/scripts/lunchScraper/data/subscribers.json

cd "${0%/*}"

$HOME/virtualenv/bin/python $HOME/scripts/lunchScraper/lunchscraper
