""" Setting up Django to work as stand-alone for supercronic in container """

import sys, os, django, time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kontorshund.settings")
django.setup()

print('waiting 10 seconds for set-up to finish')
time.sleep(10)
print('Sleep finished!')
