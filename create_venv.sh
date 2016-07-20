#!/usr/bin/env bash


if [ ! -d "./venv" ]; then
	virtualenv -p $(which python3) ./venv
else
	echo "Virtual env already created"
fi
./venv/bin/pip install requests
./venv/bin/pip install landslide