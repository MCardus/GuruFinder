"""Elasticsearch client"""
import datetime

from time import gmtime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import logging
from loggingsetup import setup_logging
from collections import Counter
import numpy as np


class ElasticsearcCli(object):

    def __init__(self, host="localhost",
                 gurus_index="tweets-gurus",
                 keywords_index="tweets-keywords",
                 gurus_codes_index="gurus-codes"):
        self.HOST = host
        self.GURUS_INDEX = gurus_index
        self.KEYWORDS_INDEX = keywords_index
        self.GURUS_CODES_INDEX = gurus_codes_index
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)
        logging.info(f"""Accesing elastic host: {[{"host": host, "port": 9200}]}""")
        self.client = Elasticsearch(hosts=[{"host": host, "port": 9200}])


    def retrieve_all_tweets(self, current_year=True):
        """
        Returns a dictionary containing all tweets in elasticsearch (keywords and gurus tweets) for a timewindow
        :param current_year: Time window
        :return: dictionary containing all tweets in elasticsearch
        """
        gurus_tweets = self.retrieve_gurus_tweets(current_year=current_year)
        gurus_keywords = self.retrieve_keywords_tweets()
        gurus_keywords.update(gurus_tweets)
        return gurus_keywords

    def retrieve_keywords_tweets(self):
        """
        Returns a dictionary containing all keywords tweets in elasticsearch
        :return: dictionary containing all tweets for each guru in elasticsearch
        """
        keywords_dict = dict()
        keywords_entries = Search(using=self.client, index=self.KEYWORDS_INDEX).source(include=["text",
                                                                                                "user.screen_name"])
        for entry in keywords_entries[0:keywords_entries.count()].scan():
            user = entry["user"]["screen_name"]
            text = entry["text"]
            if user in keywords_dict:
                keywords_dict[user].append(text)
            else:
                keywords_dict[user] = [text]

        return keywords_dict

    def retrieve_gurus_tweets(self, current_year=True):
        """
        Returns a dictionary containing all tweets for each guru in elasticsearch for a timewindow
        :return: dictionary containing all tweets for each guru in elasticsearch for a timewindow
        """
        gurus_dict = dict()
        gurus_entries = Search(using=self.client, index=self.GURUS_INDEX).source(include=["body.text",
                                                                             "body.user.screen_name",
                                                                                          "body.created_at"])
        if current_year:
            gurus_entries = gurus_entries.filter('bool', must={'query_string': {'default_field': 'body.created_at',
                                                                                "query": f"""*{gmtime().tm_year}"""}})

        for entry in gurus_entries[0:gurus_entries.count()].scan():
            user = entry.body["user"]["screen_name"]
            text = entry.body["text"]
            if user in gurus_dict:
                gurus_dict[user].append(text)
            else:
                gurus_dict[user] = list()

        return gurus_dict

    def retrieve_gurus_codes(self, gurus_to_filter, model_type):
        filtered_gurus = dict()
        for guru in gurus_to_filter:
            guru_dict = Search(using=self.client, index=self.GURUS_CODES_INDEX)\
                .source(include=["body.user","body.code"]) \
                .filter('bool', must={'match': {'body.model_type': model_type.lower()}}) \
                .filter('bool', must={'match': {'body.user': guru}})[0].execute()[0]
            user = guru_dict.body['user']
            code = guru_dict.body['code']
            filtered_gurus[user] = code
        return filtered_gurus

    def search_similar_top_n(self, input_text, n=20, current_year=True):
        """
        Elasticsearch computes top twenty similar results computing between a given text and gurus texts
        :param input_text:
        :param n:
        :param current_year: time window
        :return:
        """
        # Similar users query
        top_tweets = Search(using=self.client, index=self.GURUS_INDEX) \
            .source(include=["body.text", "body.user.id", "body.user.screen_name", "_score", "body.created_at"]) \
            .query("multi_match", fields="body.text", query=input_text)[0:n*10]

        if current_year:
            top_tweets = top_tweets.filter('bool', must={'query_string': {'default_field': 'body.created_at',
                                                                                "query": f"""*{gmtime().tm_year}"""}})

        top_users = [entry.body["user"]["screen_name"] for entry in list(top_tweets.execute())]
        gurus_names = Counter(top_users).most_common(n)
        return [guru[0] for guru in gurus_names]


    def retrieve_gurus_names(self, current_year=True):
        """
        Queryng all gurus screen names
        :param current_year: time window
        """

        gurus_names = set()
        gurus_names_query = Search(using=self.client, index=self.GURUS_INDEX) \
            .source(include=["body.user.screen_name", "body.created_at"])

        if current_year:
            gurus_names_query = gurus_names_query.filter('bool', must={'query_string': {'default_field': 'body.created_at',
                                                                                "query": f"""*{gmtime().tm_year}"""}})

        for entry in gurus_names_query.scan():
            gurus_names.add(entry.body["user"]["screen_name"])
        return np.array(list(gurus_names))

if __name__ == "__main__":
    cli = ElasticsearcCli()
    print(cli.retrieve_all_tweets())
