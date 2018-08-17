"""Elasticsearch client"""
import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class Elasticsearc_cli(object):

    def __init__(self, host="localhost", gurus_index="tweets-gurus"):
        self.HOST = host
        self.GURUS_INDEX = gurus_index
        self.client = Elasticsearch()


    def retrieve_all_tweets(self):
        """Retrieve all tweets"""

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
    cli = Elasticsearc_cli()
    print(cli.retrieve_gurus_tweets())
