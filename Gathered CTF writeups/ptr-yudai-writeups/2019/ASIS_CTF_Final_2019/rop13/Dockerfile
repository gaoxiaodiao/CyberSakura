FROM php:7.3-apache

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade

ADD challenge/flag.txt             /flag.txt
ADD challenge/server/rot13         /var/www/html/rot13
ADD challenge/server/index.php     /var/www/html/index.php
ADD challenge/server/recaptcha.php /var/www/html/recaptcha.php

RUN chown -R root:www-data /var/www/html
RUN chmod 550 /var/www/html
RUN chmod 550 /var/www/html/rot13
RUN chmod 550 /var/www/html/index.php
RUN chmod 550 /var/www/html/recaptcha.php
RUN chown -R root:root /flag.txt
RUN chmod 444 /flag.txt

RUN ls /var/www/html -lh
RUN chmod 1733 /tmp /var/tmp /dev/shm
