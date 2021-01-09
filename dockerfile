FROM ubuntu:latest
MAINTAINER changyoon "lkingkongl@naver.com"
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN apt-get install -y tzdata
RUN apt-get install -y git \
  && apt install git
RUN apt-get install -y cron

RUN (crontab -l 2>/dev/null; echo "*/30 * * * * /home/issuetracker/issuecrawl/run.py") | crontab -
WORKDIR /home
RUN mkdir issuetracker
COPY . /home/issuetracker
WORKDIR /home/issuetracker
RUN pip install -r requirements.txt

