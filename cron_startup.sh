#!/bin/bash

set -e

###############
# Set-up Django
###############
echo " Setting up Django for stand-alone use.... (cron_startup.sh)"
python /home/kontorshund/web/django_standalone_setup.py

#python /home/kontorshund/web/manage.py runserver

###################
# Start supercronic 
###################
echo " Starting supercronic.... (cron_startup.sh)"
exec supercronic /crontab