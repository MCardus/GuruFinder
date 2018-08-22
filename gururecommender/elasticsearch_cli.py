"""Elasticsearch client"""
import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import logging
from loggingsetup import setup_logging


class ElasticsearcCli(object):

    def __init__(self, host="localhost",
                 gurus_index="tweets-gurus",
                 keywords_index="tweets-keywords",
                 codified_gurus_index="tweets-codified-gurus"):
        self.HOST = host
        self.GURUS_INDEX = gurus_index
        self.KEYWORDS_INDEX = keywords_index
        self.CODIFIED_GURUS_INDEX = codified_gurus_index
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)
        logging.info(f"""Accesing elastic host: {[{"host": host, "port": 9200}]}""")
        self.client = Elasticsearch(hosts=[{"host": host, "port": 9200}])


    def retrieve_all_tweets(self):
        """
        Returns a dictionary containing all tweets in elasticsearch (keywords and gurus tweets)
        :return: dictionary containing all tweets in elasticsearch
        """
        gurus_tweets = self.retrieve_gurus_tweets()
        gurus_keywords = self.retrieve_keywords_tweets()
        gurus_tweets.update(gurus_keywords)
        return gurus_tweets

    def retrieve_keywords_tweets(self):
        """
        Returns a dictionary containing all keywords tweets in elasticsearch
        :return: dictionary containing all tweets for each guru in elasticsearch
        """
        keywords_dict = dict()
        keywords_entries = Search(using=self.client, index=self.KEYWORDS_INDEX).source(include=["text",
                                                                                                "user.screen_name"])
        for entry in keywords_entries[0:keywords_entries.count()].execute():
            user = entry["user"]["screen_name"]
            text = entry["text"]
            if user == 'JFGaleote':
                pass
            if user in keywords_dict:
                keywords_dict[user].append(text)
            else:
                keywords_dict[user] = [text]

        return keywords_dict

    def retrieve_gurus_tweets(self):
        """
        Returns a dictionary containing all tweets for each guru in elasticsearch
        :return: dictionary containing all tweets for each guru in elasticsearch
        """
        gurus_dict = dict()
        gurus_entries = Search(using=self.client, index=self.GURUS_INDEX).source(include=["body.text",
                                                                             "body.user.screen_name"])

        for entry in gurus_entries[0:gurus_entries.count()].execute():
            user = entry.body["user"]["screen_name"]
            text = entry.body["text"]
            if user in gurus_dict:
                gurus_dict[user].append(text)
            else:
                gurus_dict[user] = list()

        return gurus_dict

    def search_similar_top_n(self, input_text, n=20):
        """
        Elasticsearch computes top twenty similar results computing between a given text and gurus texts
        :param input_text:
        :param n:
        :return:
        """
        top_twenty = Search(using=self.client, index=self.GURUS_INDEX) \
            .source(include=["body.text", "body.user.id", "body.user.screen_name", "_score"]) \
            .query("multi_match", fields="body.text", query=input_text)[0:n*10] \

        top_twenty.aggs.bucket('genres', 'terms', field="body.user.id")\


        top_twenty_ids = top_twenty[0:n].execute().aggregations['genres']["buckets"]
        return top_twenty_ids

if __name__ == "__main__":
    cli = ElasticsearcCli()
    print(cli.retrieve_all_tweets())
