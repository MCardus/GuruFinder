"""GuruRecommender class tests"""

import unittest
from gururecommender import GuruRecommender

class TestGuruRecommender(unittest.TestCase):

    def setUp(self):
        self.guru_recommender = GuruRecommender()

    def test_lda_fit(self):
        # @TODO, mcck up need it
        self.guru_recommender.fit(model_type=self.guru_recommender.LDA_MODEL)

    def test_lda_predict(self):
        # @TODO, mcck up need it
        self.guru_recommender.predict(model_type=self.guru_recommender.LDA_MODEL)


if __name__ == '__main__':
    unittest.main()
