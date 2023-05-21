FROM python:3.10

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apt update && apt install ntp -y
RUN cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN pip install -r requirements.txt