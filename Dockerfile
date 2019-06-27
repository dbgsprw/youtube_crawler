FROM python:3.7
MAINTAINER dbgsprw@gmail.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
