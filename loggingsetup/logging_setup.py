"""Logging configuration"""

import os
import logging
import logging.config
import yaml


def setup_logging(
        default_path='logging_properties.yml',
        severity_level=logging.DEBUG,
        env_key='LOG_CFG'
):
    """Setup logging configuration"""

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    path = os.path.join(os.getcwd(), path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f)
        logging.config.dictConfig(config)
        logging.getLogger().setLevel(severity_level)
    else:
        logging.basicConfig(level=severity_level)


if __name__ == '__main__':
    logging.info("Hello World")
    logging.debug("Hello World")
    logging.error("Hello World")
