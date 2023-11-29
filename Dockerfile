FROM python:3.10.13-alpine3.18

RUN mkdir -p /usr/src/app && apk add ffmpeg
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8443

CMD python3 bot.py