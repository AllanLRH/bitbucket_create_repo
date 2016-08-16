#!/usr/bin/env python

import subprocess
from bitbucket.bitbucket import Bitbucket
import sys
import os


def get_internet_password(user, webpage):
    pwdBytes = subprocess.check_output(
        "security find-internet-password -a {user} -s {webpage} -w".format(
            user=user, webpage=webpage).split())
    password = pwdBytes.decode('utf-8').strip()
    return password


def create_repo(username, reponame, scm="git", private=True):
    password = get_internet_password(username, "bitbucket.org")
    bb = Bitbucket(username, password)
    response = bb.repository.create(reponame, scm=scm, private=private)
    if response[0]:  # True or False
        rsp = response[1]
        repoUrl = "https://bitbucket.org/{username}/{reponame}".format(
            username=username, reponame=reponame)
        return repoUrl, rsp
    else:
        print("Something went wrong!", fie=sys.stderr)
        sys.exit(1)


def git_add_and_push_to_remote(username, reponame):
    addCommand = "git remote add origin git@bitbucket.org:{username}/{reponame}.git".format(
        username=username, reponame=reponame)
    subprocess.call(addCommand.split())
    subprocess.call("git push -u origin --all".split())
    subprocess.call("git push origin --tags".split())


if __name__ == '__main__':
    username = "AllanLRH"
    private = True
    if len(sys.argv) == 1:
        reponame = os.getcwd().split(os.path.sep)[-1]
        if ".git" not in os.listdir("."):
            print("Error! No dir provided, and current dir is not a git repository!",
                  file=sys.stderr)
            sys.exit(1)
    else:
        reponame = sys.argv[1]
        if len(sys.argv) == 3:
                private = False if sys.argv[2] == "public" else True

    create_repo(username, reponame, private=private)
    git_add_and_push_to_remote(username, reponame)
