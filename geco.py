#!/usr/bin/env python3

import argparse
import logging
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    return parser


def main():
    pass


if __name__ == "__main__":
    args = create_parser().parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("verbosity turned on")
    main()
