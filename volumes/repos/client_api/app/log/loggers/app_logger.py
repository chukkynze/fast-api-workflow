import logging
from datetime import datetime

from app.config import get_app_env_config

app_env_config = get_app_env_config()


def get_app_logger():

    fh = logging.FileHandler('./app/log/logs/app/app-{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logging.basicConfig(
        level=app_env_config.APP_LOG_LEVEL.value,
        #filename='./app/log/logs/app.log',
        #filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s',
        force=True,
        handlers=[fh],
    )

    logger = logging.getLogger(__name__)
    logger.propagate = False

def log_exception(log, e: Exception):
    log.debug("Exception name is %s", e.__class__.__name__)
    log.debug("e.args =")
    log.debug(e.args)
    log.debug("e.__cause__ =")
    log.debug(e.__cause__)
    log.debug("e.__context__ =")
