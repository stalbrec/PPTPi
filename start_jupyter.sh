#!/bin/bash

VENV=${1:-~/PPT-env}

echo "venv:" $VENV

source $VENV/bin/activate
jupyter-lab

deactivate
