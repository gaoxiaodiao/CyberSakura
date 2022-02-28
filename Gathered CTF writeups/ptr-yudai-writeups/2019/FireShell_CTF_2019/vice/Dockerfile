FROM ubuntu:14.04

VOLUME ["/var/www"]

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    apt-get install -y \
      apache2 \
      curl \
      libcurl3 \
      libcurl3-dev \
      php5 \
      php5-cli \
      libapache2-mod-php5 \
      php5-gd \
      php5-json \
      php5-ldap \
      php5-mysql \
      php5-pgsql \
      php5-curl

ADD index.php /var/www/html/index.php

EXPOSE 80
