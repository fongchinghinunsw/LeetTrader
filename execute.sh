#!/bin/bash

virtualenv --seeder=pip /var/tmp/leettrader/venv
source /var/tmp/leettrader/venv/bin/activate
pip install -r requirements.txt
python utils.py
python run.py