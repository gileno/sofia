FROM python:3.3
ENV PYTHONUNBUFFERED 1

MAINTAINER Henrique Chehad <hchehad@gmail.com>

RUN apt-get update
RUN apt-get install libpq-dev
RUN pip install --upgrade pip

ADD . /sofia/
WORKDIR /sofia

RUN pip install -r /sofia/requirements.txt

EXPOSE 8000

RUN chmod +x /sofia/entrypoint.sh
ENTRYPOINT sh entrypoint.sh
