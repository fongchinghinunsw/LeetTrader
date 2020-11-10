#!/bin/bash
# IMPORTANT: This script is only for the tutor/student to run the application in the vlab.
virtualenv --seeder=pip /var/tmp/leettrader/venv
source /var/tmp/leettrader/venv/bin/activate
pip install -r requirements.txt
python utils.py
python leettrader/tutorial/train.py
python run.py