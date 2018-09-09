"""API services"""

import os
import json
import logging
import traceback
from flask import Blueprint, request
from loggingsetup.logging_setup import setup_logging
from gururecommender.guru_recommender import GuruRecommender

route = Blueprint('route', __name__)
setup_logging("loggingsetup/logging_properties.yml")

if 'ACCES_TOKEN' in os.environ:
    acess_token = os.getenv("ACCES_TOKEN")
    guruRecommender = GuruRecommender()

    @route.route("/recommend", methods=['POST'])
    def recommend():
        """
        Recommendations using guruFinder models
        """
        body = request.get_json()
        if 'token' in body and "token" in body and "input_text" in body and "num_recommendations" in body:
            token = body['token']
            input_text = body['input_text']
            n_recommendations = int(body["num_recommendations"])
            logging.info(f"""A: {token} B: {acess_token}""")
            if token == acess_token:
                if n_recommendations > 15:
                    code = "error"
                    ret = "max num of recommendations reached. Max num is 15"
                else:
                    code = "message"
                    ret = guruRecommender.top_n_gurus(input_text=input_text, model_type="lda", n=n_recommendations)
            else:
                code = "error"
                ret = f"""Authoritzation error"""

        else:
            code = "error"
            ret = f"""Incorrect access token"""

        return json.dumps({code: ret})

else:
    raise Exception("No token")


