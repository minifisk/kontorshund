# pull official base image
FROM python:3.9.6

# set work directory
WORKDIR /usr/src/kontorshund

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create directory for the app user
RUN mkdir -p /home/kontorshund

# create the appropriate directories
ENV HOME=/home/kontorshund
ENV APP_HOME=/home/kontorshund/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME
