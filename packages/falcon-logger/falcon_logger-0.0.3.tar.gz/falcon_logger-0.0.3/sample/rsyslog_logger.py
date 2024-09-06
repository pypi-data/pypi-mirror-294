import logging
import logging.handlers

import sys


class RsyslogLogger:
    def __init__(self):
        # Gets or creates a logger
        self._logger = logging.getLogger(__name__)

        # set log level
        self._logger.setLevel(logging.DEBUG)

        # formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

        sh = logging.handlers.SysLogHandler(address='/dev/log')
        # sh.setFormatter(formatter)
        self._logger.addHandler(sh)

        stdout_handler = logging.StreamHandler(sys.stdout)
        # handler.setFormatter(formatter)
        self._logger.addHandler(stdout_handler)

    def term(self):
        pass

    def debug(self, msg=''):
        self._logger.debug(msg)


def create_logger(app_name, log_level=logging.DEBUG, stdout=True, syslog=False, file=False):
    # create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    # set log format to handlers
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')

    if file:
        # create file logger handler
        fh = logging.FileHandler('my-sample-app.log')
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if syslog:
        # create syslog logger handler
        sh = logging.handlers.SysLogHandler(address='/dev/log')
        sh.setLevel(log_level)
        sf = logging.Formatter('%(name)s: %(message)s')
        sh.setFormatter(sf)
        logger.addHandler(sh)

    if stdout:
        # create stream logger handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
