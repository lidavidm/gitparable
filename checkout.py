#!/usr/bin/env python

import os
import shutil
import sys

import branch
import snapshot

def checkout(number):
    source = snapshot.unparse_snapshot(number)
    target = "working/"

    shutil.rmtree(target)
    shutil.copytree(source, target)
    os.remove(os.path.join(target, "message"))

if __name__ == "__main__":
    print("Enter snapshot number or branch name: ", end="")
    number = input()

    try:
        number = int(number)
    except ValueError:
        try:
            number = branch.switch_branch(number)
        except ValueError:
            print("Invalid branch name.")
            sys.exit(1)

        print("Invalid snapshot number.")
        sys.exit(1)

    if not snapshot.exists(number):
        print("Snapshot does not exist.")
        sys.exit(1)

    checkout(number)
    print("Checked out snapshot", number)
