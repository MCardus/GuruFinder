"""Guru recommender system"""

import logging
import json
import numpy as np
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
import argparse
from text_models.topic_modelling import LDA
from loggingsetup import setup_logging
from gururecommender.elasticsearch_cli import ElasticsearcCli


class GuruRecommender(object):

    def __init__(self):
        with open('gururecommender/conf/config.json', 'r') as f:
            config = json.load(f)
        print(config["elastic_host"])
        self.elasticsearch = ElasticsearcCli(host=config["elastic_host"])
        self.lda = LDA(default_lda_pickle_filepath="gururecommender/models/lda.pkl",
                       default_vectorizer_pickle_filepath="gururecommender/models/vectorizer.pkl")
        self.LDA_MODEL = "lda"
        self.WORD2VEC_MODEL = "word2vec"
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)
        self.predict_logger = logging.getLogger('guru_predict')

    def elasticsearch_top_n_gurus(self, input_text, n=20):
        return self.elasticsearch.search_similar_top_n(input_text=input_text, n=n)

    def top_n_gurus(self, input_text, model_type, n=20):
        first_selection = self.elasticsearch_top_n_gurus(input_text=input_text,
                                                         n=n)

    def fit(self, model_type):
        """
        Collect all tweets in elastic and trains a new model which is serialized in disk
        :param model_type: Model type
        """
        tweets_list = list(self.elasticsearch.retrieve_all_tweets().values())
        tweets_list_processed = [". ".join(tweet) for tweet in tweets_list]
        if model_type == self.LDA_MODEL:
            logging.info(f"""LDA fit in proces""")
            self.lda.fit(tweets_list_processed)
        elif model_type == self.WORD2VEC_MODEL:
            pass
        else:
            raise ValueError(f"""Model {model_type} does not exists""")

    def predict(self, model_type):
        gurus_dict = self.elasticsearch.retrieve_gurus_tweets()
        gurus_text = {k: '. '.join(v) for k, v in gurus_dict.items()}
        if model_type.lower() == self.LDA_MODEL:
            prediction = {k: self.lda.predict(np.array([v])) for k, v in gurus_text.items()}
        elif model_type == self.WORD2VEC_MODEL:
            pass
        else:
            raise ValueError(f"""Model {model_type} does not exists""")
        for k,v in prediction.items():
            self.predict_logger.info(json.dumps({"user": k, "code": json.dumps(v[0].tolist())}))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Python Twitter API client')
    ap.add_argument("-a",
                    "--action",
                    required=True,
                    help="action. options: fit, predict")
    ap.add_argument("-m",
                    "--model",
                    required=True,
                    help="model type, options: lda")
    args = vars(ap.parse_args())
    action = args['action']
    model = args['model']
    gurufinder = GuruRecommender()

    if not model in ["lda"]:
        raise ValueError(f"""model {model} not known""")
    if action == "fit":
            gurufinder.fit(model_type=model)
    elif action == "predict":
            gurufinder.predict(model_type=model)
    else:
        raise ValueError(f"""action {action} not known""")
    # while True:
    #     pass


