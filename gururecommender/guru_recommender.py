"""Guru recommender system"""

import logging
import json
import numpy as np
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
import argparse
from text_models.topic_modelling import LDA
from text_models.embeddeds import Doc2Vec
from loggingsetup import setup_logging
from gururecommender.elasticsearch_cli import ElasticsearcCli
from sklearn.neighbors import BallTree
import ast


class GuruRecommender(object):

    def __init__(self,
                 config=None,
                 default_lda_pickle_filepath="gururecommender/models/lda.pkl",
                 default_vectorizer_pickle_filepath="gururecommender/models/vectorizer.pkl",
                 default_doc2vec_pickle_filepath="gururecommender/models/d2v.model"):

        if not config:
            with open('gururecommender/conf/config.json', 'r') as f:
                config = json.load(f)

        self.elasticsearch = ElasticsearcCli(host=config["elastic_host"])
        self.lda = LDA(default_lda_pickle_filepath=default_lda_pickle_filepath,
                       default_vectorizer_pickle_filepath=default_vectorizer_pickle_filepath)
        self.doc2vec = Doc2Vec(default_doc2vec_pickle_filepath=default_doc2vec_pickle_filepath)
        self.LDA_MODEL = "lda"
        self.DOC2VEC_MODEL = "doc2vec"
        self.WORD2VEC_MODEL = "word2vec"
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)
        logging.info(f"""Elasticsearch host {config["elastic_host"]}""")
        self.predict_logger = logging.getLogger('guru_predict')

    def elasticsearch_top_n_gurus(self, input_text, n=20):
        elastic_top_n = self.elasticsearch.search_similar_top_n(input_text=input_text, n=n)
        logging.info(f"""Elastic top n: {elastic_top_n}""")
        return elastic_top_n

    def top_n_gurus(self, input_text, model_type, n=10, elastic_filter=True):
        logging.info(f"""Looking for top {n} gurus using model type {model_type}""")
        logging.info(f"""Elastic filter {elastic_filter}""")
        if elastic_filter:
            logging.info(f"""Elasticsearch is looking for similar documents to: {input_text}""")
            # Elasticsearch first layer recommendation
            first_selection_gurus = self.elasticsearch_top_n_gurus(input_text=input_text, n=n*2)
            if len(first_selection_gurus) == 0:
                raise ValueError("Zero Gurus retrieved on first recommendation layer")
            else:
                logging.info(f"""Retrieved {len(first_selection_gurus)} gurus on first recommendation layer""")
        else:
            # Obtaining all gurus since there is no prior filter
            logging.info("Reetrieving all gurus names")
            first_selection_gurus = self.elasticsearch.retrieve_gurus_names()

        # Retrieving text model codes
        seconds_selection_codes = self.elasticsearch.retrieve_gurus_codes(first_selection_gurus, model_type=model_type)
        clean_codes = np.array([ast.literal_eval(string_code)
                                for string_code in list(seconds_selection_codes.values())])

        # Creating input_text code
        input_text_code = self._predict_single(input_text=input_text, model_type=model_type)

        # Looking for nearest gurus
        tree = BallTree(clean_codes, leaf_size=len(clean_codes)*2)
        k=len(clean_codes) if n > len(clean_codes) else n
        dist, ind = tree.query(input_text_code, k=k)
        top_n_gurus = [list(seconds_selection_codes.keys())[index] for index in ind[0]]
        logging.info(f"""Top n gurus: {top_n_gurus}""")
        return top_n_gurus


    def fit(self, model_type,
            lda_topic_granurality=3,
            lda_max_topics=12,
            words_min_freq=0.01,
            words_max_freq=0.8,
            doc2vec_workers=10):
        """
        Collect all tweets in elastic and trains a new model which is serialized in disk
        :param model_type: Model type
        """
        logging.info(f"""Fit using model type {model_type}""")
        tweets_list = list(self.elasticsearch.retrieve_all_tweets().values())
        # Generating flat list
        tweets_list_processed = np.concatenate(tweets_list).ravel().tolist()
        if model_type.lower() == self.LDA_MODEL:
            logging.info(f"""LDA fit in proces""")
            self.lda.fit(tweets_list_processed,
                         topic_search_granurality=lda_topic_granurality,
                         max_topics=lda_max_topics,
                         words_min_freq=words_min_freq,
                         words_max_freq=words_max_freq)
        elif model_type.lower() == self.WORD2VEC_MODEL:
            pass
        elif model_type.lower() == self.DOC2VEC_MODEL:
            self.doc2vec.fit(tweets_list_processed)
        else:
            raise ValueError(f"""Model {model_type} does not exists""")

    def predict(self, model_type):
        logging.info(f"""Predict using model type {model_type}""")
        gurus_dict = self.elasticsearch.retrieve_gurus_tweets()
        gurus_text = {k: '. '.join(v) for k, v in gurus_dict.items()}
        if model_type.lower() == self.LDA_MODEL:
            prediction = {k: self.lda.predict(np.array([v]))[0] for k, v in gurus_text.items()}
        elif model_type.lower() == self.WORD2VEC_MODEL:
            pass
        elif model_type.lower() == self.DOC2VEC_MODEL:
            prediction = {k: self.doc2vec.predict(v) for k, v in gurus_text.items()}
        else:
            raise ValueError(f"""Model {model_type} does not exists""")
        for k,v in prediction.items():
            self.predict_logger.info(json.dumps({"user": k,
                                                 "code": json.dumps(v.tolist()),
                                                 "model_type": model_type.lower()}))

    def _predict_single(self, input_text, model_type):
        if model_type.lower() == self.LDA_MODEL:
            prediction = self.lda.predict(np.array([input_text]))
        elif model_type.lower() == self.DOC2VEC_MODEL:
            prediction = np.array([self.doc2vec.predict(input_text)])
        else:
            raise ValueError(f"""Model {model_type} does not exists""")
        return prediction

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Python Twitter API client')
    ap.add_argument("-a",
                    "--action",
                    required=True,
                    help="action. options: fit, predict, recommend")
    ap.add_argument("-m",
                    "--model",
                    required=True,
                    help="model type, options: lda")
    ap.add_argument("-i",
                    "--input",
                    required=False,
                    help="input recommendation text")
    ap.add_argument("-n",
                    "--num_recommendation",
                    required=False,
                    default=15,
                    help="num of recommended gurus")
    ap.add_argument("-e",
                    "--elastic_filter",
                    required=False,
                    default="y",
                    help="Elastic filter. Options: y,n")
    args = vars(ap.parse_args())
    action = args['action']
    model = args['model']
    input_text = str(args['input'])
    elastic_filter = args['elastic_filter']
    elastic_filter = False if elastic_filter == "n" else True
    try:
        num_recommendation = int(args['num_recommendation'])
    except:
        logging.warning(f"""Num of recomendations {args['num_recommendation']} should be an integer""")
        num_recommendation=0
    gurufinder = GuruRecommender()

    if not model in [gurufinder.DOC2VEC_MODEL, gurufinder.LDA_MODEL]:
        raise ValueError(f"""model {model} not known""")
    if action == "fit":
            gurufinder.fit(model_type=model)
    elif action == "predict":
            gurufinder.predict(model_type=model)
    elif action == "recommend":
            gurufinder.top_n_gurus(input_text=input_text, model_type=model, n=num_recommendation, elastic_filter=elastic_filter)
    else:
        raise ValueError(f"""action {action} not known""")
    # while True:
    #     pass


