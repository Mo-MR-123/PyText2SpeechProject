#!/bin/bash

# Set the PYTHONPATH variable to this project root folder so that python can search for modules from 
# root folder (current folder) where this script is executed.
# This makes sure that the experiment scripts can see and use other modules (e.g. shared folder)
# and use it without import errors.
export PYTHONPATH="$PWD"
export IS_DEV_LOGGING=1 # log to stdout if we are in dev. otherwise log in files.
export ENABLE_LOGGING=0

python src/main.py