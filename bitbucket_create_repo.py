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
        print("Something went wrong!", file=sys.stderr)
        sys.exit(1)


def git_add_and_push_to_remote(username, reponame):
    addCommand = "git remote add origin git@bitbucket.org:{username}/{reponame}.git".format(
        username=username, reponame=reponame)
    subprocess.call(addCommand.split())
    subprocess.call("git push -u origin --all".split())
    subprocess.call("git push origin --tags".split())


def initialize_repo_if_nonexistent():
    if '.git' in os.listdir('.'):
        return True
    try:
        git_base_dir = subprocess.check_output('git rev-parse --show-toplevel'.split())
        if git_base_dir.strip():
            return True
    except subprocess.CalledProcessError as err:  # It's not a git repo
        c1 = subprocess.call('git init'.split())
        if c1 != 0: return False  # noqa
        c2 = subprocess.call('git add .'.split())
        if c2 != 0: return False  # noqa
        c3 = subprocess.call('git commit -m "Initial commit"'.split())
        if c3 != 0: return False  # noqa
        return True


if __name__ == '__main__':
    username = "AllanLRH"
    private = True
    if len(sys.argv) == 1:
        reponame = os.getcwd().split(os.path.sep)[-1]
        initialize_repo_if_nonexistent()
    else:
        reponame = sys.argv[1]
        if len(sys.argv) == 3:
                private = False if sys.argv[2] == "public" else True

    create_repo(username, reponame, private=private)
    git_add_and_push_to_remote(username, reponame)
