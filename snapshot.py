#!/usr/bin/env python3

import datetime
import os
import shutil
import sys

def warn(message):
    print(message, file=sys.stderr)


def parse_snapshot(filename):
    if filename.startswith("snapshot-"):
        try:
            snapshot_number = int(filename[9:])
            return snapshot_number
        except ValueError:
            warn(f"Found directory that looks like snapshot but isn't: {filename}")
            return None
    else:
        return None


def unparse_snapshot(number):
    return "snapshot-" + str(number)


def exists(number):
    return os.path.exists(unparse_snapshot(number))


def current_snapshot():
    """
    Returns the ID of the latest snapshot, or None if no snapshots exist.
    """

    greatest_snapshot = None
    for filename in os.listdir("."):
        if os.path.isdir(os.path.join(".", filename)):
            snapshot_number = parse_snapshot(filename)
            if snapshot_number is None:
                continue
            elif greatest_snapshot is None or snapshot_number > greatest_snapshot:
                greatest_snapshot = snapshot_number

    if greatest_snapshot is None:
        return None
    else:
        return greatest_snapshot


def get_next_snapshot():
    current = current_snapshot()

    if current is None:
        return 0
    else:
        return current + 1


def create_snapshot(number, message, parent_snapshot):
    target = unparse_snapshot(number)
    source = "./working"

    if os.path.exists(os.path.join(source, "message")):
        raise RuntimeError("'message' file exists in 'working/'!")

    shutil.copytree(src=source, dst=target)
    creation_time = datetime.datetime.now().isoformat()
    message = message + "\n"
    message = message + creation_time + "\n"
    message = message + "Parent: " + str(parent_snapshot) + "\n"
    with open(os.path.join(target, "message"), "w") as f:
        f.write(message)

    return message


if __name__ == "__main__":
    target = get_next_snapshot()
    print("Enter snapshot message: ", end="")
    message = input()

    if target != 0:
        print("Enter parent snapshot: ", end="")
        parent = input()
        try:
            parent = int(parent)
        except ValueError:
            print("Invalid parent snapshot number.")
            sys.exit(1)

        if not exists(parent):
            print("Parent snapshot does not exist.")
            sys.exit(1)
    else:
        # The root commit is its own parent
        parent = 0

    message = create_snapshot(target, message, parent)
    print(f"Created snapshot {target}:")
    print(message, end="")
