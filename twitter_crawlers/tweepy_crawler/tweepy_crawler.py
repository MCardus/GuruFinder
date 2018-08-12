"""Twitter client for python"""

import tweepy
import argparse
import os
import logging
from logging_setup import setup_logging


class TweepyCrawler(object):
    """Twitter client for python"""

    def __init__(self):
        # Creation of the actual interface, using authentication
        self.auth = self._load_auth()
        self.api = tweepy.API(self.auth)
        setup_logging(default_path="logging_setup/logging_properties.yml", severity_level=logging.INFO)

    def download_user_timeline(self, user):
        """
        Using api instance to download an entire timeline given a user
        :param user: Twitter user. i.e @ThePSF
        :return:
        """
        for event in tweepy.Cursor(self.api.user_timeline, screen_name=user).items():
            # Generating tweets though logging
            logging.info(event._json)

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
