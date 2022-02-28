FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD flag        /home/pwn/flag
ADD chall       /home/pwn/chall
ADD pwn.xinetd  /etc/xinetd.d/pwn
ADD init.sh     /etc/init.sh
ADD redir.sh    /home/pwn/redir.sh

RUN chown -R pwn:pwn /home/pwn
RUN chown root:pwn /home/pwn
RUN chmod 440 /home/pwn/flag
RUN chmod 550 /home/pwn/chall
RUN chmod 550 /home/pwn/redir.sh

RUN ls /home/pwn -lh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN service xinetd restart
