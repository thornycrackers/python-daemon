#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example on how to create a daemon.

If you are confused on how the daemon library works you can get some ideas
from the tests.

https://pagure.io/python-daemon/blob/master/f/test/test_runner.py
"""
import os
import sys
from logging import FileHandler, Formatter, getLogger, info
from os.path import isfile
from signal import SIGINT, SIGTERM, signal
from time import sleep


class MyDaemon(object):
    """Daemon class. Not for production use, example only."""

    def __init__(self):
        """Initialize the paths and the pidfile of the daemon."""
        # Setup logging
        log = getLogger()
        handler = FileHandler('/var/log/python_daemon.log')
        formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel('INFO')
        self.pidfile_path = '/var/run/python_daemon.pid'
        # Register handlers to exit when we get a kill signal
        signal(SIGINT, self.exit_gracefully)
        signal(SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        """Exit Gracefully."""
        info('I died')
        self.remove_pidfile()
        exit()

    def create_pidfile(self):
        """Create a pidfile for the daemon."""
        info('Creating pid file')
        with open(self.pidfile_path, mode='w', encoding='utf-8') as a_file:
            a_file.write(str('{}\n'.format(self.pid)))

    def remove_pidfile(self):
        """Remove the pidfile."""
        info('Removing pidfile: {}'.format(self.pidfile_path))
        os.remove(self.pidfile_path)

    def detach_process(self):
        """Simple method for daemonizing process."""
        newpid = os.fork()
        if newpid > 0:
            exit()
        else:
            os.setsid()
            newpid = os.fork()
            if newpid > 0:
                exit()
            else:
                self.pid = os.getpid()
                return

    def run(self):
        """Entrypoint for the daemon."""
        if isfile(self.pidfile_path):
            print('Pidfile already exists, Daemon already running')
            exit()
        info('Starting up the python daemon.')
        self.detach_process()
        # redirect stdin, stdout and stderr to devnull
        f = open(os.devnull, 'w')
        sys.stdin = f
        sys.stdout = f
        sys.stderr = f
        # Create the pid file
        self.create_pidfile()
        while True:
            info('I am alive')
            sleep(1)

    def stop(self):
        """Stop a currently running process."""
        try:
            with open(self.pidfile_path, encoding='utf-8') as a_file:
                pid = a_file.readline()
                pid = pid.strip()  # Remove whitespace
                os.kill(int(pid), SIGTERM)
                exit()
        except FileNotFoundError:
            print('no pidfile found, is the daemon running?')
            exit()


# run the daemon
if __name__ == '__main__':
    daemon = MyDaemon()
    if len(sys.argv) <= 1:
        print('Usage: ./daemon_example.py \'start|stop\'')
        exit()
    if sys.argv[1] == 'start':
        daemon.run()
        exit()
    if sys.argv[1] == 'stop':
        daemon.stop()
        exit()
    print('Error: I dont know that command')
