# -*- coding: utf-8 -*-
"""Example of the Unix double fork for daemons."""
import os
import sys


def print_process_info(name):
    """Print information about the currently executing process."""
    pid = os.getpid()
    pgid = os.getpgid(pid)
    sid = os.getsid(pid)
    print('{} (PID:{}) (PGID:{}) (SID:{})'.format(name, pid, pgid, sid))


# First Fork
newpid = os.fork()
if newpid > 0:
    print_process_info('Parent')
    sys.exit()
else:
    print_process_info('Child')
    os.setsid()
    newpid = os.fork()
    # Second fork
    if newpid == 0:
        print_process_info('Grandchild')
    else:
        print_process_info('Child')
        sys.exit()

# # POP QUIZ!!!! Why won't this work
# print_process_info('Parent')
# os.setsid()
# print_process_info('Parent')
# newpid = os.fork()
# if newpid == 0:
#     print_process_info('Child')
