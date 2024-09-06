import logging
import os
import sys


class NormalLogger:
    def __init__(self):
        # Gets or creates a logger
        self._logger = logging.getLogger(__name__)

        # set log level
        self._logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(os.path.join('out', 'sample_normal.log'))
        self._logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        self._logger.addHandler(stdout_handler)

    def term(self):
        pass

    def debug(self, msg=''):
        self._logger.debug(msg)
