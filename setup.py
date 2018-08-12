#!/usr/bin/env python

from distutils.core import setup

setup(
    name='gurufinder',
    packages=["logging_setup",
              "twitter_crawlers/tweepy_crawler"],
    version='0.1',
    license='MIT',
    long_description=open('README.md').read(),
)
