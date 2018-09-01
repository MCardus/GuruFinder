"""GuruRecommender class tests"""

import unittest
from gururecommender import GuruRecommender

class TestGuruRecommender(unittest.TestCase):

    def setUp(self):
        config = {'elastic_host': 'localhost', 'port': 9200}
        self.guru_recommender = \
            GuruRecommender(config=config,
                            default_doc2vec_pickle_filepath="models/d2v.model",
                            default_lda_pickle_filepath="models/lda.pkl",
                            default_vectorizer_pickle_filepath="models/vectorizer.pkl",
                            default_word2vec_pickle_filepath="models/w2v.pkl")

    def test_lda_fit(self):
        # assert void method, and no exception is raised
        self.assertEqual(self.guru_recommender.fit(model_type=self.guru_recommender.LDA_MODEL,
                                                   words_min_freq=0.0001,
                                                   words_max_freq=0.7), None)

    def test_lda_predict(self):
        # assert void method, and no exception is raised
        self.assertEqual(self.guru_recommender.predict(model_type=self.guru_recommender.LDA_MODEL),None)

    def test_top_n_gurus_lda(self):
        input_text = "I made these this morning, first time. Followed recipe exactly and they were Perfect! All ingredients pulsed in a food processor. My batter was thick enough in about 4 minutes. I used a non stick griddle, buttered. The heat setting is medium low to low. Make sure griddle is hot before cooking. 4 minutes first side, 3 minutes second side. Low and slow is the correct way to cook these. No sticking whatsoever. As an aside, my psyllium was orange flavored Metamucil, so I sprinkled in about a teaspoon of unsweetened coconut flakes and called them Tropical pancakes with the hint of orange undertone!"
        output = self.guru_recommender.top_n_gurus(input_text=input_text, model_type=self.guru_recommender.LDA_MODEL, n=3)
        assert isinstance(output,list)

    def test_doc2vec_fit(self):
        # assert void method, and no exception is raised
        self.assertEqual(self.guru_recommender.fit(model_type=self.guru_recommender.DOC2VEC_MODEL), None)

    def test_doc2vec_predict(self):
        # assert void method, and no exception is raised
        self.guru_recommender.predict(model_type=self.guru_recommender.DOC2VEC_MODEL)

    def test_top_n_gurus_doc2vec(self):
        input_text = "I made these this morning, first time. Followed recipe exactly and they were Perfect! All ingredients pulsed in a food processor. My batter was thick enough in about 4 minutes. I used a non stick griddle, buttered. The heat setting is medium low to low. Make sure griddle is hot before cooking. 4 minutes first side, 3 minutes second side. Low and slow is the correct way to cook these. No sticking whatsoever. As an aside, my psyllium was orange flavored Metamucil, so I sprinkled in about a teaspoon of unsweetened coconut flakes and called them Tropical pancakes with the hint of orange undertone!"
        output = self.guru_recommender.top_n_gurus(input_text=input_text, model_type=self.guru_recommender.DOC2VEC_MODEL, n=3)
        assert isinstance(output, list)

    def test_top_n_gurus_doc2vec_no_elastic_filter(self):
        input_text = "I made these this morning, first time. Followed recipe exactly and they were Perfect! All ingredients pulsed in a food processor. My batter was thick enough in about 4 minutes. I used a non stick griddle, buttered. The heat setting is medium low to low. Make sure griddle is hot before cooking. 4 minutes first side, 3 minutes second side. Low and slow is the correct way to cook these. No sticking whatsoever. As an aside, my psyllium was orange flavored Metamucil, so I sprinkled in about a teaspoon of unsweetened coconut flakes and called them Tropical pancakes with the hint of orange undertone!"
        output = self.guru_recommender.top_n_gurus(input_text=input_text, model_type=self.guru_recommender.DOC2VEC_MODEL, n=3, elastic_filter=False)
        assert isinstance(output, list)

    def test_word2vec_fit(self):
        # assert void method, and no exception is raised
        self.assertEqual(self.guru_recommender.fit(model_type=self.guru_recommender.WORD2VEC_MODEL), None)

    def test_word2vec_predict(self):
        # assert void method, and no exception is raised
        self.assertEqual(self.guru_recommender.predict(model_type=self.guru_recommender.WORD2VEC_MODEL), None)

    def test_top_n_gurus_word2vec(self):
        input_text = "I made these this morning, first time. Followed recipe exactly and they were Perfect! All ingredients pulsed in a food processor. My batter was thick enough in about 4 minutes. I used a non stick griddle, buttered. The heat setting is medium low to low. Make sure griddle is hot before cooking. 4 minutes first side, 3 minutes second side. Low and slow is the correct way to cook these. No sticking whatsoever. As an aside, my psyllium was orange flavored Metamucil, so I sprinkled in about a teaspoon of unsweetened coconut flakes and called them Tropical pancakes with the hint of orange undertone!"
        output = self.guru_recommender.top_n_gurus(input_text=input_text, model_type=self.guru_recommender.WORD2VEC_MODEL, n=3)
        assert isinstance(output, list)

    def test_top_n_gurus_wordvec_no_elastic_filter(self):
        input_text = "I made these this morning, first time. Followed recipe exactly and they were Perfect! All ingredients pulsed in a food processor. My batter was thick enough in about 4 minutes. I used a non stick griddle, buttered. The heat setting is medium low to low. Make sure griddle is hot before cooking. 4 minutes first side, 3 minutes second side. Low and slow is the correct way to cook these. No sticking whatsoever. As an aside, my psyllium was orange flavored Metamucil, so I sprinkled in about a teaspoon of unsweetened coconut flakes and called them Tropical pancakes with the hint of orange undertone!"
        output = self.guru_recommender.top_n_gurus(input_text=input_text, model_type=self.guru_recommender.WORD2VEC_MODEL, n=1, elastic_filter=False)
        assert isinstance(output, list)



if __name__ == '__main__':
    unittest.main()
