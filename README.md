# What is a daemon?
- A computer program that runs as a background process, rather than being under the direct control of an interactive user.
- Generally end with a 'd' (e.g. 'sshd', 'syslogd')

# Easiest Example
- nohup  python simple server & 

# Why do the double fork?
Fork then exit, process becomes child of init.

Session (SID) → Process Group (PGID) → Process (PID)

a process group denotes a collection of one or more processes.
a session denotes a collection of one or more process groups.

The first process in the process group becomes the process group leader and the
first process in the session becomes the session leader. Every session can have
one TTY associated with it. Only a session leader can take control of a TTY.
For a process to be truly daemonized (ran in the background) we should ensure
that the session leader is killed so that there is no possibility of the
session ever taking control of the TTY.

http://stackoverflow.com/questions/881388/what-is-the-reason-for-performing-a-double-fork-when-creating-a-daemon

# What does setsid do?
creates a new session if the calling process is not a process group leader.
The calling process is the leader of the new session, the process group leader
of the new process group, and has no controlling terminal.
http://unix.stackexchange.com/questions/240646/why-we-use-setsid-while-daemonizing-a-process

# Pop quiz, why can't we do just a single fork?
Disallowing a process group leader from calling setsid()
prevents the possibility that a process group leader places itself in
a new session while other processes in the process group remain in
the original session; such a scenario would break the strict two-
level hierarchy of sessions and process groups.
http://man7.org/linux/man-pages/man2/setsid.2.html

# What does nohup do?
Ignores the hangup signal.

# How to create a daemon.
http://web.archive.org/web/20120914180018/http://www.steve.org.uk/Reference/Unix/faq_2.html#SEC16
1. fork() so the parent can exit, this returns control to the command line or shell invoking your program. This step is required so that the new process is guaranteed not to be a process group leader. The next step, setsid(), fails if you're a process group leader.
2. setsid() to become a process group and session group leader. Since a controlling terminal is associated with a session, and this new session has not yet acquired a controlling terminal our process now has no controlling terminal, which is a Good Thing for daemons.
3. fork() again so the parent, (the session group leader), can exit. This means that we, as a non-session group leader, can never regain a controlling terminal.
4. chdir("/") to ensure that our process doesn't keep any directory in use. Failure to do this could make it so that an administrator couldn't unmount a filesystem, because it was our current directory. [Equivalently, we could change to any directory containing files important to the daemon's operation.]
5. umask(0) so that we have complete control over the permissions of anything we write. We don't know what umask we may have inherited. [This step is optional]
6. close() fds 0, 1, and 2. This releases the standard in, out, and error we inherited from our parent process. We have no way of knowing where these fds might have been redirected to. Note that many daemons use sysconf() to determine the limit _SC_OPEN_MAX. _SC_OPEN_MAX tells you the maximun open files/process. Then in a loop, the daemon can close all possible file descriptors. You have to decide if you need to do this or not. If you think that there might be file-descriptors open you should close them, since there's a limit on number of concurrent file descriptors.
7. Establish new open descriptors for stdin, stdout and stderr. Even if you don't plan to use them, it is still a good idea to have them open. The precise handling of these is a matter of taste; if you have a logfile, for example, you might wish to open it as stdout or stderr, and open `/dev/null' as stdin; alternatively, you could open `/dev/console' as stderr and/or stdout, and `/dev/null' as stdin, or any other combination that makes sense for your particular daemon.

