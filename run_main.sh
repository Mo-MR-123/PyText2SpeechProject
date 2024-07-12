#!/bin/bash

# Set the PYTHONPATH variable to this project root folder so that python can search for modules from 
# root folder (current folder) where this script is executed.
# This makes sure that the experiment scripts can see and use other modules (e.g. shared folder)
# and use it without import errors.
export PYTHONPATH="$PWD"

python src/main.py