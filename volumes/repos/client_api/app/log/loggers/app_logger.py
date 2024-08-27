from datetime import datetime
import logging


def get_app_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./app/log/logs/app.log',
        filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger('Main App Logger')

    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

def get_service_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./app/log/logs/service_layer.log',
        filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger('Service Layer Logger')

    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

def get_repo_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./app/log/logs/data_layer.log',
        filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger('Data Layer Logger')

    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

def log_exception(log, e: Exception):
    log.debug("Exception name is %s", e.__class__.__name__)
    log.debug("e.args =")
    log.debug(e.args)
    log.debug("e.__cause__ =")
    log.debug(e.__cause__)
    log.debug("e.__context__ =")

def get_test_logger():
    # during testing, use a transient handler instead of a persistent handler
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./app/log/logs/tests.log',
        filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger('Test Logger')

    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

def get_monitor_logger():
    logging.basicConfig(
        level=logging.MONITOR, # Custom Level
        filename='./app/log/logs/monitoring.log',
        filemode='a',
        format='%(asctime)s - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger('Monitoring Logger')

    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger
