FROM python:3.6.6-alpine3.8

ENV twitter_users=$twitter_users

# Installing external dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installing internal dependencies
VOLUME "${pwd}/../../logging_setup"
#RUN pip install --no-cache-dir logging_setup/
CMD ["sleep", "300"]
#CMD [ "python", "twitter_crawlers/tweepy_crawler/tweepy_crawler.py", "-u", "${twitter_users}"]