"""GuruRecommender class tests"""

import unittest
from gururecommender import ElasticsearcCli
import logging
import numpy as np


class TestElasticSearchCli(unittest.TestCase):

    def setUp(self):
        self.elasticsearch_cli = ElasticsearcCli()
        logging.basicConfig(level=logging.INFO)

    def test_retrieve_gurus_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_gurus_tweets(), dict)

    def test_retrieve_keywords_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_keywords_tweets(), dict)

    def test_retrieve_all_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_all_tweets(), dict)

    def test_search_similar_top_n(self):
        input_text = "I love Art Buckwald’s quote: Dinner is not what you do in the evening before something else. Dinner is the evening. That is what makes Savor the Summit held in Park City each June so much fun.  It is an entire evening of great food, fabulous company and making new friends. Cuisine Unlimited is the only caterer invited. It is one of our favorite events of the year and so happy we have many guests who return year after year."
        output = self.elasticsearch_cli.search_similar_top_n(input_text=input_text, n=4)
        print(output)
        assert isinstance(output, list)

    def test_retrieve_gurus_codes(self):
        input_text = "I love Art Buckwald’s quote: Dinner is not what you do in the evening before something else. Dinner is the evening. That is what makes Savor the Summit held in Park City each June so much fun.  It is an entire evening of great food, fabulous company and making new friends. Cuisine Unlimited is the only caterer invited. It is one of our favorite events of the year and so happy we have many guests who return year after year."
        assert isinstance(self.elasticsearch_cli.retrieve_gurus_codes(
            self.elasticsearch_cli.search_similar_top_n(input_text=input_text, n=5), model_type='lda'), dict)

    def test_retrieve_gurus_names(self):
        gurus_names = self.elasticsearch_cli.retrieve_gurus_names()
        logging.info(gurus_names)
        assert isinstance(gurus_names, np.ndarray)


if __name__ == '__main__':
    unittest.main()
