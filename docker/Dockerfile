FROM python:3.7

MAINTAINER Lasha Gogua <gogualasha@gmail.com>


RUN apt-get update -y && apt-get install firefox-esr -y
RUN apt-get install -y --no-install-recommends ca-certificates \
 && rm -fr /var/lib/apt/lists/* \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin

RUN mkdir /app
WORKDIR /app


ADD requirements.txt requirements.txt
ADD scrapy.cfg scrapy.cfg
ADD classifiers /app/classifiers
ADD uptodate_parser /app/uptodate_parser
ADD docker/scrapyd.conf scrapyd.conf

RUN pip install tqdm
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["scrapyd"]
