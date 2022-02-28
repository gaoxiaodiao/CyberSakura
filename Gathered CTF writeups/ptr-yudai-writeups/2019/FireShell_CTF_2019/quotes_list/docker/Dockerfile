FROM ubuntu:17.10

RUN apt-get update -y && apt-get install xinetd -y

RUN mkdir -p /app/quotes_list
RUN mkdir -p /opt/glibc

ADD quotes_list.sh /app/quotes_list
ADD quotes_list /app/quotes_list
ADD flag.txt /app/quotes_list
ADD init.sh /bin
ADD quotes_list.xinetd /etc/xinetd.d/quotes_list
ADD libc.so.6 /opt/glibc
ADD ld-linux-x86-64.so.2 /opt/glibc

RUN groupadd -r quotes_list && useradd -r -g quotes_list quotes_list && \
    chown -R root:quotes_list /app/quotes_list && \
    chmod 750 /app/quotes_list/quotes_list.sh && \
    chmod 750 /app/quotes_list/quotes_list && \
    chmod 440 /app/quotes_list/flag.txt && \
    chmod 700 /bin/init.sh

RUN service xinetd restart
