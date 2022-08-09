#!/bin/bash

VENV=${1:-~/PPT-env}

echo "venv:" $VENV

source $VENV/bin/activate
#jupyter-lab --ip 0.0.0.0 --no-browser --port 9999
jupyter-lab #--ip 0.0.0.0 --no-browser --port 9999

deactivate
