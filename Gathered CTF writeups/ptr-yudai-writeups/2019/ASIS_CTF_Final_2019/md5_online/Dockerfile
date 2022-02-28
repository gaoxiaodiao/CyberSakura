FROM ubuntu:17.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN dpkg --add-architecture i386
RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd libssl-dev:i386
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/pwn.xinetd /etc/xinetd.d/pwn
ADD challenge/init.sh    /etc/init.sh
ADD challenge/redir.sh   /home/pwn/redir.sh
RUN chmod 550        /home/pwn/redir.sh
RUN chmod 700        /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD challenge/flag.txt     /home/pwn/flag.txt
ADD challenge/chall        /home/pwn/chall
ADD challenge/banner.txt   /home/pwn/banner.txt
RUN chmod 440 /home/pwn/flag.txt
RUN chmod 550 /home/pwn/chall
RUN chmod 440 /home/pwn/banner.txt
RUN chown -R root:pwn /home/pwn
RUN ls /home/pwn -lh
RUN service xinetd restart