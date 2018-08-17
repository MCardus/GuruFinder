"""Guru recommender system"""
from gururecommender.elasticsearch_cli import Elasticsearc_cli
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
from lda_topic_modelling.LDAModelling import LDAModelling


class GuruRecommender(object):

    def __init__(self):
        self.elasticsearch = Elasticsearc_cli()
        self.lda = LDAModelling()

    def top_n_similar_gurus(self, input_text, n=20):
        return self.elasticsearch.search_similar_top_n(input_text=input_text, n=n)


    def train_lda(self):
        all_tweets = self.elasticsearch.retrieve_gurus_tweets()
        self.lda.train_gridsearch(all_tweets)

    def codify_gurus(self):
        gurus_dict = self.elasticsearch.retrieve_gurus_tweets()
        for guru in gurus_dict.keys()
        self.lda.train_gridsearch(gurus_dict)
        return gurus_dict

if __name__ == "__main__":
    guruRecomender = GuruRecommender()
    #print(guruRecomender.top_n_similar_gurus(input_text="Apache Sqoop has been used primarily for transfer of data between relational databases and HDFS, leveraging the Hadoop Mapreduce engine"))
    print(guruRecomender.codify_gurus())
