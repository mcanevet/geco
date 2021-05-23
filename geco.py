#!/usr/bin/env python3

import argparse
import logging
import geco.profile as profile

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-p", "--profile", required=True, help="Profile to use")
    return parser.parse_args()

def main():
    logging.debug("In main().")
    prof = profile.Profile(args.profile)
    logging.debug(prof)
    logging.debug(prof.path)
    pass

if __name__ == "__main__":
    args = parse_arguments()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
