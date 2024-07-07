#!/bin/bash

VENV_DIR="./venv"

if [ ! -d "$VENV_DIR" ]; then
   echo "Creating Virtual Environment..."
   source $VENV_DIR/bin/activate
   echo "Installing Requirements..."
   pip install -r requirements.txt
else
   source $VENV_DIR/bin/activate
fi

export FLASK_APP=server.py
export FLASK_ENV=development
flask run
