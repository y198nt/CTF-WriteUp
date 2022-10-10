FROM ubuntu:22.04

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update && apt-get install -y socat

WORKDIR /home/user/

USER user

COPY ./chall/ .

COPY ./info/flag.txt .


EXPOSE 13337

CMD socat \
      TCP-LISTEN:13337,reuseaddr,fork \
      EXEC:"/home/user/13+37"

