#!/usr/bin/env python

from distutils.core import setup

setup(
    name='gurufinder',
    packages=["loggingsetup",
              "twitter_crawlers/tweepy_crawler",
              "gururecommender",
              "api"],
    version='0.1',
    license='MIT',
    long_description=open('README.md').read(),
)
