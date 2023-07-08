#!/bin/bash
#Только для Linux и Pypy.

current_dir=$(dirname "$(realpath "$0")")

cd "$current_dir" && chmod ug+x start.sh && pypy3 -m venv ./ && source ./bin/activate && pip3 install -U -r requirements.txt && chmod ug+x bot.py && pypy3 bot.py> ./app.log 2>&1