#!/usr/bin/env python

import snapshot


def parse_branches():
    branches = []
    with open("branches") as f:
        for line in f:
            current = False
            if line.startswith("*"):
                current = True
                line = line[1:]
            name, snapshot_id = line.strip().split(" ")
            snapshot_id = snapshot.unserialize_snapshot(snapshot_id)
            branches.append((name, snapshot_id, current))

    return branches


def unparse_branches(branches):
    with open("branches", "w") as f:
        for (name, snapshot_id, current) in branches:
            if current:
                f.write(f"* {name} {snapshot_id}\n")
            else:
                f.write(f"  {name} {snapshot_id}\n")


def current_branch():
    branches = parse_branches()
    for (name, snapshot_id, current) in branches:
        if current:
            return (name, snapshot_id, current)
    return None


def create_branch(name, snapshot_number):
    branches = parse_branches()

    for (existing, _, _) in branches:
        if name == existing:
            raise ValueError(f"Branch {name} already exists!")

    branches.append((name, snapshot_number, False))
    unparse_branches(branches)


def switch_branch(name):
    branches = parse_branches()
    new_branches = []
    found = False
    current_snapshot = None

    for (branch_name, snapshot_id, current) in branches:
        if branch_name == name:
            found = True
            current_snapshot = snapshot_id
            new_branches.append((branch_name, snapshot_id, True))
        else:
            new_branches.append((branch_name, snapshot_id, False))

    if not found:
        raise ValueError("Branch not found!")

    unparse_branches(new_branches)

    return current_snapshot


def update_branch(name, new_snapshot):
    branches = parse_branches()
    found = False
    for i, (branch_name, snapshot_id, current) in enumerate(branches):
        if branch_name == name:
            snapshot_id = new_snapshot
            found = True
        branches[i] = (branch_name, snapshot_id, current)

    if not found:
        raise ValueError("Branch not found!")

    unparse_branches(branches)
