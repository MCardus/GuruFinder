"""API creation"""
import os
from flask import Flask


def create_app(name=__name__, config=None, environment=None):
    """
    App factory
    :param name: Flask app name
    :param config: Flask config
    :param environment: Env conf file
    :return:
    """
    app = Flask(name)
    app.config['ENVIRONMENT'] = environment
    app.config.update(config or {})
    return app
