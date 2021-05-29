#!/usr/bin/env python3

import argparse
import logging
import pathlib
import sys
from geco import profile


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-p", "--profile", help="the geco profile to load",
                        type=pathlib.Path, required=True)
    return parser


def main(argv=sys.argv[1:]):
    args = create_parser().parse_args(argv)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("verbosity turned on")
    logging.debug("Profile = " + str(args.profile))
    p = profile.Profile(args.profile)
    p.load()
    p.create_efi_dir()
    p.download_opencore()
    p.checksum()
