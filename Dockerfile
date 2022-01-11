# pull official base image
FROM python:3.9.6

# set work directory
WORKDIR /usr/src/kontorshund

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y locales && sed -i -e 's/# sv_SE.UTF-8 UTF-8/sv_SE.UTF-8 UTF-8/' /etc/locale.gen && dpkg-reconfigure --frontend=noninteractive locales

ENV LANG sv_SE.UTF-8
ENV LC_ALL sv_SE.UTF-8

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create the appropriate directories
RUN mkdir -p /home/kontorshund
ENV HOME=/home/kontorshund
ENV APP_HOME=/home/kontorshund/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY ./kontorshund/mediafiles $APP_HOME/mediafiles
COPY . $APP_HOME


