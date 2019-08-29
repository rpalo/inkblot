import pathlib
import sys

from inkblot import generate


def main():
    generate(pathlib.Path(sys.argv[1]))
