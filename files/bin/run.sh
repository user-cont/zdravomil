#!/bin/bash

set -e
source setup.sh

generate_passwd_file

if [ -z ${APP} ]; then
    echo "APP not defined or empty, exiting"
    exit 1
fi
if [ -z ${WORKER_QUEUES} ]; then
    echo "WORKER_QUEUES not defined or empty, exiting"
    exit 1

fi

if [ -z ${GITHUB_API_KEY} ]; then
    echo "GITHUB_API_KEY not defined or empty, exiting"
    exit 1

fi

echo "Queues: ${WORKER_QUEUES}"
exec celery worker --app=${APP} --queues="${WORKER_QUEUES}" --loglevel=info --pool=gevent --concurrency=100
