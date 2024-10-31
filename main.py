#!/usr/bin/env python3

from crt import CrtPassiveScan
import parse
import threading
import argparse
import sys
from pwn import *


def get_options():

    parser = argparse.ArgumentParser(prog="PasScan",
                                     description="Passively scan a set of domains",
                                     epilog="Author: @antthegreekgod"
                                     )

    parser.add_argument("-f", "--file", default="apex.lst", help="File containing apex domains, if no file is provided it will try to scan the current directory for a file named \"apex.lst\"")
    parser.add_argument("-d", "--domain", default=None, help="Scan a single domain")
    
    return parser.parse_args()

def query(domain):
    p = log.progress("Scanning" + domain)
    CrtPassiveScan(domain).query() # make and save crt.sh petition
    subdomains = parse.ParseCrtSh("out.txt", domain).extract() # crawl file and extract subdomains
    p.success("Scan completed!")
    print(subdomains)


def main():

    args = get_options()

    domains = []

    if args.domain:
        domains.append(args.domain)

    try:    
        with open (args.file, "r") as f:        
            domains = f.read().split()
    except FileNotFoundError:
        pass

    threads = []
    if not domains:
        sys.exit("[!] No file nor domain was provided to scan. Use -h or --help to view the help menu")

    for domain in domains:
        thread = threading.Thread(target=query, args=(domain,))
        threads.append(thread)

    for thread in threads:
        thread.start()

if __name__ == '__main__':
    main()

