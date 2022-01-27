#!/bin/bash

set -e


###################
# Start supercronic 
###################
echo " Starting supercronic.... (cron_startup.sh)"
exec supercronic -passthrough-logs /crontab 