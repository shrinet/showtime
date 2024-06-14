#!/bin/bash

echo "======================="
echo "Running Celery"
echo "======================="
if [ -d "ticenv" ];
then
    echo "Enabling virtual env"
else
    echo "No Vertual env"
    exit N
fi

#Activate virtual env
source ./ticenv/bin/activate

celery -A app.celery worker -l info

deactivate