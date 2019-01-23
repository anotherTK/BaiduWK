#!/usr/bin/env bash

# flask run configuration
export FLASK_APP=services
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 3764
