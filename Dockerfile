# pull official base image
FROM python:3.9.6

# set work directory
WORKDIR /usr/src/kontorshund

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Locales (local language format for date and time)
RUN apt-get update && apt-get install -y locales && sed -i -e 's/# sv_SE.UTF-8 UTF-8/sv_SE.UTF-8 UTF-8/' /etc/locale.gen && dpkg-reconfigure --frontend=noninteractive locales
ENV LANG sv_SE.UTF-8
ENV LC_ALL sv_SE.UTF-8

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.6/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=c3b78d342e5413ad39092fd3cfc083a85f5e2b75

RUN curl -fsSLO "$SUPERCRONIC_URL" && \
    echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - && \
    chmod +x "$SUPERCRONIC" && \
    mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" && \
    ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic


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

RUN ["chmod", "+x", "/home/kontorshund/web/hello.py"]
RUN ["chmod", "+x", "/home/kontorshund/web/cron_startup.sh"]
RUN ["chmod", "+x", "/home/kontorshund/web/django_standalone_setup.py"]



