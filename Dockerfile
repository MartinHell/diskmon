FROM python:3.7.2-alpine3.8

MAINTAINER Martin Hellstrom <martin@hellstrom.it>

WORKDIR /usr/src/app

COPY diskmon/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt &&\
    apk add --update smartmontools &&\
    rm -rf /var/cache/apk/*

COPY diskmon/main.py ./

CMD [ "python", "./main.py" ]
