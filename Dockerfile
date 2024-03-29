#########
# SET-UP
#########

FROM python:3.9.6

WORKDIR /usr/src/kontorshund

###############
# ENV VARIABLES
###############

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

############
# LOCALES/TZ
############

RUN apt-get update && apt-get install -y locales && sed -i -e 's/# sv_SE.UTF-8 UTF-8/sv_SE.UTF-8 UTF-8/' /etc/locale.gen && dpkg-reconfigure --frontend=noninteractive locales
ENV LANG sv_SE.UTF-8
ENV LC_ALL sv_SE.UTF-8

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Stockholm
RUN apt-get install -y tzdata

##############
# DEPENDENCIES
##############

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


############
#SUPERCRONIC
############

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=048b95b48b708983effb2e5c935a1ef8483d9e3e

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic


#############
# DIRECTORIES
#############

RUN mkdir -p /home/dockeruser
ENV HOME=/home/dockeruser
ENV APP_HOME=/home/dockeruser/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY . $APP_HOME

#############
# PERMISSIONS
#############

RUN ["chmod", "+x", "/home/dockeruser/web/hello.py"]
RUN ["chmod", "+x", "/home/dockeruser/web/cron_startup.sh"]



