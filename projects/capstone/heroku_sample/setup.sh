#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/capstone"
export TEST_DB_URL="postgresql://postgres@localhost:5432/capstone_test"
export EXCITED="true"
echo "setup.sh script executed successfully!"
echo $DATABASE_URL
echo $TEST_DB_URL
echo $EXCITED
export FLASK_APP=app.py
export FLASK_ENV=development
