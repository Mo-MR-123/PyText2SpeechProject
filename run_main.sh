#!/bin/bash

# Set the PYTHONPATH variable to this project root folder so that python can search for modules from 
# root folder (current folder) where this script is executed.
# This tells Python to treat the root directory (where this script is run) 
# as the starting point for imports
export PYTHONPATH="$PWD"
export IS_DEV_LOGGING=1 # log to stdout if we are in dev. otherwise log in files.
export ENABLE_LOGGING=0

# Set DEBUG_FLAG for debugging (1 for debugging, unset or 0 for normal execution)
export DEBUG_FLAG=1  # Change to 0 or comment out to run without debugging

python src/main.py