FROM ubuntu:latest
MAINTAINER changyoon "lkingkongl@naver.com"
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ='Asia/Seoul'

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  tzdata \
  git \
  cron \
  vim \
  fonts-nanum\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# time setting
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
  && echo Asia/Seoul > /etc/timezone

# Create the log file to be able to run tail and Setup cron job
RUN touch /var/log/cron.log \
  && (crontab -l 2>/dev/null; echo "*/30 * * * * /home/issuetracker/issuecrawl/run.py") | crontab - \
  && mkdir /home/issuetracker
COPY . /home/issuetracker
WORKDIR /home/issuetracker
RUN pip install -r requirements.txt

CMD ["cron", "-f"]
# Run the command on container startup


