#!/bin/bash

#update and upgrade system
sudo apt-get update && sudo apt-get upgrade -y

#install scipy and its dependencies
sudo apt-get install python-scipy libatlas-base-dev -y

#create python3 venv to be able to easily install jupyter 
#and other packages used in the project
python3 -m venv ~/PPT-env

#activate virtualenv and install required packages via pip
source ~/PPT-env/bin/activate
pip install -r requirements.txt

