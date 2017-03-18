#!/usr/bin/env python3

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


if __name__ == "__main__":
    target = unparse_snapshot(get_next_snapshot())
    source = "./working"

    print(f"Creating snapshot {target}")

    shutil.copytree(src=source, dst=target)
