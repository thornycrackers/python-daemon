#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example on how to create a daemon.

If you are confused on how the daemon library works you can get some ideas
from the tests.

https://pagure.io/python-daemon/blob/master/f/test/test_runner.py
"""
from logging import FileHandler, Formatter, getLogger, info
from os import fork, setsid, getpid
from sys import exit
from time import sleep


class MyDaemon(object):
    """Daemon class. Not for production use, example only."""

    def __init__(self):
        """Initialize the paths and the pidfile of the daemon."""
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/python_daemon.pid'

    def create_pidfile(self):
        with open(self.pidfile_path, mode='w', encoding='utf-8') as a_file:
            a_file.write(str('{}\n'.format(self.pid)))

    def detach_process(self):
        """Simple method for daemonizing process."""
        newpid = fork()
        if newpid > 0:
            exit()
        else:
            setsid()
            newpid = fork()
            if newpid > 0:
                exit()
            else:
                self.pid = getpid()
                self.create_pidfile()
                return

    def run(self):
        """Entrypoint for the daemon."""
        self.detach_process()
        # Setup logging
        log = getLogger()
        handler = FileHandler('/var/log/python_daemon.log')
        formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel('INFO')
        while True:
            info('I am alive')
            sleep(1)


# run the daemon
if __name__ == '__main__':
    daemon = MyDaemon()
    daemon.run()
