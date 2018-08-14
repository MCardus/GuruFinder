"""Twitter client for python"""

import tweepy
import argparse
import os
import logging
import json
from loggingsetup import setup_logging


class TweepyCrawler(object):
    """Twitter client for python"""

    def __init__(self):
        # Creation of the actual interface, using authentication
        self.auth = self._load_auth()
        self.api = tweepy.API(self.auth)
        #TODO - Read using confreader
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)

    def download_user_timeline(self, user):
        """
        Using api instance to download an entire timeline given a user
        :param user: Twitter user. i.e @ThePSF
        :return:
        """
        for event in tweepy.Cursor(self.api.user_timeline, screen_name=user).items():
            # Generating tweets though logging
            #logging.info(json.dumps(event._json))
            """
            dict_keys(['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source', 'in_reply_to_status_id',
                       'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str',
                       'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors',
                       'retweeted_status', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited',
                       'retweeted', 'possibly_sensitive', 'lang'])
            """
            user_info = {k: event._json['user'][k] for k in ('id', 'id_str', 'name', 'screen_name', 'location',
                                                          'description','followers_count','lang','created_at')}
            tweet_info = {k: event._json[k] for k in ('created_at', 'id', 'id_str', 'text', 'geo', 'lang',
                                                      'favorite_count', 'favorited', 'retweet_count')}
            tweet_info['user'] = user_info
            logging.info(json.dumps(tweet_info))

    def _load_auth(self):
        """
        Read auth env vars and load an auth object
        :return:
        """
        # Consumer keys and access tokens, used for OAuth
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        access_token = os.getenv("TWITTER_OAUTH_SECRET")
        access_token_secret = os.getenv("TWITTER_OAUTH_TOKEN")

        # Validating env vars
        for var in [consumer_secret, access_token, access_token_secret]:
            if not var: raise ValueError("Empty env vars!")

        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description='Python Twitter API client')
    ap.add_argument("-u",
                    "--user",
                    required=True,
                    help="username to download its timeline. i.e @ThePSF‏")
    args = vars(ap.parse_args())
    tweepy_cli = TweepyCrawler()
    tweepy_cli.download_user_timeline(args["user"])
