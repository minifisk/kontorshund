# Kontorshund (Office Dog)

www.kontorshund.se


## For examination purposes
Distinctiveness and Complexity:
Please find below the description of the project, I believe you will find that it meets your standards for a final project.

## Short description of the project
Kontorshund.se is a Django powered application, offering people a marketplace for creating advertisements either offering or requesting an "Office dog" - i.e.
If you have a dog and need/want a few days off during the weekdays, you can create an ad, finding someone who are willing to take care of your dog one/a few weekdays
every week. At the opposite end, if you work in an office/are retired/just want to take care of a dog but maybe don't have the ability or want to buy your own
dog, you can create an ad to find a dog owner willing to lend out their dog to you!


## How to run the application

### Postgres database
The application need a postgres database, so start a local postgres, go into the file "dev.env.example" and change it's name to "dev.env". Then fill out the following
lines with the connection details to your database:

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

### Rest of fields in env file
You can disregard of the rest of the lines in the dev.env, MERCHANT_SWISH_NUMBER is related to setting up the payment solution for the Swedish payment system.
reCAPTCHA_SITE_KEY and reCAPTCHA_SECRET_KEY is for handling the implemented reCAPCHA check for giving out clients emails.

### Start the application
Start a development version of the application (production version of application require additional certificate files and has other settings not needed for just
testing the application) by running (make sure you have downloaded and run the Desktop Docker application first)

docker-compose up --build

## Design considerations for the application

### Django vs separate front-end
In the beginning of this project I was contemplating if it would be best to create two separate applications - one React front-end and hosting the backend with Django
and django-rest-framework. However, I landed in the decision to do the application fully in Django, as I at the time felt that there was some areas within
Django that I wanted to get more accustomed to, such as working with Django build in tools for forms. 

Hindsight I'm happy to have made this decision, sure doing everything in Django is a bit limiting when implementing more complex javascript solutions, which I
for example was forced to do for the search function for ads on the index page (see javascript section of list_ads.html). By using a front-end framework such
as React this code could have been made more consise and modular, as well as designing reusable components for different front-end sections.

However, using the built in template engine in Django offers a lot of simplifications in working with forms, which I use quiet a lot in this application, so
I didn't suffer to much from my design decision. It was also valuable to stick to the borders of the Django framework and learn to develop solutions, and 
I must say that I have come to greatly appreciate its design, especially the "loose coupling" philosophy, making it easier to create modular soltuions.

### Error handling
I have tried implement logical logger.debug and logger.info messages for overlooking the application, but also for debugging purposes. Furthermore I've connected
Sentry to the production application to get notified when there is an error on the live application.

### Testing
I have done tests for majority of the models and views in the application, if you run a newer Mac with the M1 chip, you may run into errors when running tests, see
fix for this below:

To run tests, start the docker application:

docker-compose up --build

Then open a shell for the application, either trough VSCode's built-in Docker extension, or by running:

docker exec -it web /bin/bash

Then run

python manage.py test
 
If you run into issues when running test containing "SCRAM AUTHENTICATION", stop the docker-compose runtime, and execute:

export DOCKER_DEFAULT_PLATFORM=linux/amd64

Then rerun:

docker-compose up --build

### Docker
I have designed the application using Docker as I highly enjoy the way working with dockerized application and become accustomed to it. It makes it very easy to set up the development environment, and combine for example the main web application with an scheduler instance running CRON-jobs, which I have also implemented.
This also make it easier to set up a test-postgres database, instead of having an external postgres (which I however use for production as it is easier to
manage an external database in production than to have to go through the abstraction in Docker).

### NGINX
I have set up the application to run with Gunicorn + NGINX in production, where NGINX handles the static and media files, and Gunicorn serve the actual application, according to branch standards.

### Backup
I've set up a backup-script which do daily backups on my external Postgres instance, this run directly on the Ubuntu machine where I host the production application, but can be found in the repository under scripts/backup.

### Templates
I have tried to modularize the templates, saving sections that are repeated in separate files and including them when needed.

### Authentication
I'm using Django allauth for authentication as it make it much easier to work with for example social authentication (I'm using Google and Facebook in production). 

### Fixtures
I'm using fixtures for importing essential database posts for making the application work - for example geographies and dog breeds.

### Storage
I'm using Linode's storage solution, which is a S3 type of storage solution, which enable using Boto3 for handling static and media files, which works very well with Django.

### Payment solution
The production application is integrated with the Swedish payment solution Swish, which make it possible for customers to do payments via their phone when posting an ad. This is build with certificates obtained by my bank and integrated in the application. The process can be seen in payment_views, where I've implemented the solution both for customers visiting the site via desktop to create a QR code, which they then take a photo of with their mobile and obtain the call for payment with, or for customers who visit the site via mobile and directly can open their Swish application when making their payment. This was a challenging part of building the application, but I got help from another Swedish developer I got contact with in a forum online. Together we set up the open repository for aiding developers in the same situation: https://github.com/johano99/swishsimple

## Final remarks
This was my last project in the two course series of Harvards CS50 and CS50Web courses (this project being the final project for the latter course). I started my journey toward becoming a developer in 2020, and have now, in march 2022, obtained a position as a back-end developer, which I enjoy very much. Harvards courses made this possible, and I have discovered my passion for coding and web development. 

This was a challenging application to build and it took quiet some time, I've estimated that the total time from the first commit until launch was around 200-220 hours. A lot of the time has gone into designing the application, but also familiarizing myself with how to set up a production ready infrastructure, powered on a Linux machine. I'm very happy to have done it "the right way", and not settling for abstracted services such as Heroku. 

Doing it from the bottom up has been very challenging at times, but I've also found a fascination and love for Linux and the way the system is designed. Finding wonderful packages such as Watchlist, which handle the automatic deployment with Docker has been a life-saver. I'm happy to have entered web development at this point in time, where development don't have to be to cumbersome, but where a single person can build a pretty complex application.

My final thanks goes out to Harvard and the staff at CS50 and CS50W for making this material available for free. It has truly changed the course of my life, for the better.




