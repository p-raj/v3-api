FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
    && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y \
        ca-certificates \
        nginx \
        gettext-base \
        python3-dev \
        python-psycopg2 \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements /usr/src/app/requirements
RUN pip install -r requirements/production.txt

# RUN echo 'daemon off;' >> /etc/nginx/nginx.conf
# RUN ln -s /dev/stdout /var/log/nginx/access.log && ln -s /dev/stderr /var/log/nginx/error.log
RUN rm /etc/nginx/conf.d/default.conf
COPY noapp.conf /etc/nginx/conf.d/noapp.conf
COPY noapp.ini noapp.ini
COPY noapp.sh noapp.sh
RUN chmod +x noapp.sh

COPY . /usr/src/app
EXPOSE 80 1337
