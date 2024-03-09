#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
export EXCITED="true"
echo "setup.sh script executed successfully!"
echo $DATABASE_URL
echo $EXCITED
export FLASK_APP=myapp
export FLASK_ENV=development
