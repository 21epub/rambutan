FROM python:3.7.9-slim-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install supervisor
RUN pip install -U pip -i https://mirrors.aliyun.com/pypi/simple/

COPY . /opt/rambutan
WORKDIR		/opt/rambutan

RUN pip install -r requirement/prod.txt

COPY docker/conf/gunicorn /etc/default/gunicorn

EXPOSE		5000



#CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8000", "-k", "gevent", "-w", "2", "apps:create_app()"]
