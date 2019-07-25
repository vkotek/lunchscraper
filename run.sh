#!/usr/bin/env bash

cp $HOME/web.kotek.co/myapp/subscribers.json $PWD/data/subscribers.json

$HOME/virtualenv/bin/python $PWD/lunchscraper
