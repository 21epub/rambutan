FROM python:3.7.9-slim-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install supervisor
RUN pip install -U pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirement/prod.txt

COPY . /opt/rambutan
WORKDIR		/opt/rambutan
EXPOSE		5000

