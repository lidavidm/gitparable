#!/usr/bin/env python

import os


def init():
    os.mkdir("working/")
    with open("branches", "w") as branches:
        pass


if __name__ == "__main__":
    init()
