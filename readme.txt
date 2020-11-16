===========================================================================
Deployment on vlab
Deployment on vlab is easy. Just run the following command below, which will install virtualenv, create and activate a virtual environment on /var/tmp (that is a directory that won’t affecting your disk quota, because the libraries size of our app exceed normal disk quota provided by CSE), installing all the requirement libraries, initialize the database and run the application.

./execute.sh

After that, open your browser and type http://localhost:6969/ to access the LeetTrader web application. Have fun!

===========================================================================
General deployment
Using the general approach to deploy the application, you need to make sure you have installed all the required libraries in your environment. Using a virtual environment is recommended.

Run the following command to install virtualenv.
pip3 install virtualenv
In the base directory, run the following command to create a virtual environment.
virtualenv venv
In the base directory, run the following command to activate the virtual environment.
source venv/bin/activate
In the base directory, run the following command to install all the required libraries.
pip install -r requirements.txt
In the base directory, run the following command to initialize the database.
python utils.py
In the base directory, run the following command to run the application.
python run.py

After that, open your browser and type http://localhost:6969/ to access LeetTrader. Have fun!
===========================================================================