from datetime import datetime
import logging
from app.config import config


def get_app_logger():

    fh = logging.FileHandler('./app/log/logs/app/app-{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logging.basicConfig(
        level=config.APP_LOG_LEVEL.value,
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
