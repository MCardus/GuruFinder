"""GuruRecommender class tests"""

import unittest
from gururecommender import ElasticsearcCli


class TestElasticSearchCli(unittest.TestCase):

    def setUp(self):
        self.elasticsearch_cli = ElasticsearcCli()

    def test_retrieve_gurus_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_gurus_tweets(), dict)

    def test_retrieve_keywords_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_keywords_tweets(), dict)

    def test_retrieve_all_tweets(self):
        assert isinstance(self.elasticsearch_cli.retrieve_all_tweets(), dict)


if __name__ == '__main__':
    unittest.main()
