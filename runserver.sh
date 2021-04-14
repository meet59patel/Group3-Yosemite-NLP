#!/bin/bash

export FLASK_APP=main.py
export FLASK_ENV=development
export TOKENIZERS_PARALLELISM=true
flask run --host 0.0.0.0