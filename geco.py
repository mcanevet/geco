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
    p = profile.Profile(args.profile)
    p.load()
    p.create_efi_dir()
    p.download_opencore()
    p.patch_config_plist()
    p.compile_ssdts()
    p.download_kexts()
    p.download_ocbinarydata()

if __name__ == "__main__":
    args = parse_arguments()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
