# Primitive i/o functions referenced elsewhere, useful for test patching (a
# sort of dependency injection

import sys

import readchar


ISATTY = sys.stdin.isatty()


def isatty():
    return ISATTY


def stream():
    return '' if ISATTY else sys.stdin.read()


def ttyin():
    return readchar.readkey()
