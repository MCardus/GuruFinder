"""Twitter client for python"""

import tweepy
import argparse
import os
import logging
import json
from loggingsetup import setup_logging
import time


class TweepyCrawler(object):
    """Twitter client for python"""

    def __init__(self):
        # Creation of the actual interface, using authentication
        self.auth = self._load_auth()
        self.api = tweepy.API(self.auth)
        #TODO - Read using confreader
        setup_logging(default_path="loggingsetup/logging_properties.yml", severity_level=logging.INFO)
        self.twitter_logger = logging.getLogger('twiter_crawler')

    def download_user_timeline(self, users):
        """
        Using api instance to download an entire timeline given a list of coma separated users
        :param users: Twitter coma separated users. i.e @ThePSF,@montypython ‏
        :return:
        """
        for user in users.split(","):
            try:
                # @todo find a more suitable way to avoi twitter api limitations
                for event in tweepy.Cursor(self.api.user_timeline, screen_name=user).items():
                    # Generating tweets though logging
                    if event._json['lang'] == "en":
                        user_info = {k: event._json['user'][k] for k in ('id', 'id_str', 'name', 'screen_name', 'location',
                                                                      'description','followers_count','lang','created_at')}
                        tweet_info = {k: event._json[k] for k in ('created_at', 'id', 'id_str', 'text', 'geo', 'lang',
                                                                  'favorite_count', 'favorited', 'retweet_count')}
                        tweet_info['user'] = user_info
                        self.twitter_logger.info(json.dumps(tweet_info))
            except tweepy.TweepError:
                time.sleep(60 * 15)

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
    ap = argparse.ArgumentParser(description='Python Twitter API client')
    ap.add_argument("-u",
                    "--user",
                    required=True,
                    help="username to download its timeline. i.e @ThePSF‏")
    args = vars(ap.parse_args())
    tweepy_cli = TweepyCrawler()
    tweepy_cli.download_user_timeline(args["user"])
