FROM        ubuntu
MAINTAINER	jiaxin	<edison7500@gmail.com>
RUN         apt-get update && apt-get -y install python2.7 \
                    python2.7-dev python-pip libjpeg8-dev libpng12-dev \
                    zlib1g-dev gcc make libffi-dev supervisor
RUN         pip install -U flask requests pillow gunicorn cffi gevent -i http://pypi.douban.com/simple
COPY        supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR     /data/www/rambutan
EXPOSE 		5000
CMD         ["/usr/bin/supervisord"]