import argparse
import os
import sys
import time

from falcon_logger.lib.logger import FalconLogger
from normal_logger import NormalLogger
from rsyslog_logger import RsyslogLogger
from stdout_logger import StdoutLogger


# -------------------
class App:
    # -------------------
    def __init__(self):
        self._system = None
        self._num_lines = 100
        self._log = None

    # -------------------
    def init(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('system')
        parser.add_argument('--numlines', default=100, type=int, required=False)
        args = parser.parse_args()
        # print(args)

        self._system = args.system
        self._num_lines = args.numlines

        self._log = None
        if self._system == 'stdout':
            self._log = StdoutLogger()
        elif self._system == 'falcon':
            self._log = FalconLogger(os.path.join('out', 'sample_falcon.log'))
        elif self._system == 'falcon2':
            self._log = FalconLogger(None)
        elif self._system == 'normal':
            self._log = NormalLogger()
        elif self._system == 'rsyslog':
            self._log = RsyslogLogger()
        else:
            print(f'unknown system: {self._system}, choose stdout, falcon, normal, rsyslog')
            sys.exit(1)

    # -------------------
    def term(self):
        pass

    # -------------------
    def run(self):
        start_time = time.time()
        for i in range(self._num_lines):
            self._log.debug(f'{i}: test')

        if self._log is not None:
            self._log.term()

        end_time = time.time()
        elapsed = round((end_time - start_time) * 1_000, 1)
        print(f'{self._system}: total time: {elapsed} ms')


# -------------------
def main():
    app = App()
    app.init()
    app.run()
    app.term()


main()
