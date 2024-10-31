#!/usr/bin/env python3

from crt import CrtPassiveScan
from hunter import EmailHunter
from shodan import Shodan
import json
import parse
import threading
import argparse
import sys
from os import path, mkdir
from pwn import *

global subdomainDB
subdomainDB = {}

def get_options():

    parser = argparse.ArgumentParser(prog="PasScan",
                                     description="Passively scan a set of domains",
                                     epilog="Author: @antthegreekgod"
                                     )

    parser.add_argument("-f", "--file", default="apex.lst", help="File containing apex domains, if no file is provided it will try to scan the current directory for a file named \"apex.lst\"")
    parser.add_argument("-d", "--domain", help="Scan a single domain")
    parser.add_argument("-e", "--email", help="File with API KEY for hunter.io, by default it'll will try to read from \".hunterio\" in current directory")
    
    return parser.parse_args()

def query(domain):

    CrtPassiveScan(domain).query() # make and save crt.sh petition
    subdomains = parse.ParseCrtSh("out.txt", domain).extract() # crawl file and extract subdomains
    for subdomain in subdomains:
        if subdomain not in subdomainDB:
            subdomainDB[subdomain] = {"IP":"","ports":""}

def call_hunter(api_file, domains):
    try:

        with open(api_file, "r") as f:                
            api_key = f.read()

            for domain in domains:
                return EmailHunter(domain, api_key).call_hunterio() # passing target and API Key for hunter
                
    except FileNotFoundError:            
        
        print(f"File {api_file} not found, skipping hunter.io enum")
        return

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

    # start subdomain enumeration using crt.sh on background
    for domain in domains:
        thread = threading.Thread(target=query, args=(domain,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    # if email param is set, hunt emails using hunter.io api_key
    emails = []
    if args.email:
        emails = call_hunter(args.email, domains)

    elif path.isfile('.hunterio'):
        emails = call_hunter('.hunterio', domains)

    if emails:
        try:
            os.mkdir("results")
        except FileExistsError:
            pass
            
        with open("results/emails.lst", "w") as f:
            for email in emails:
                f.write(email + "\n")

        
    
    # wait for crt.sh to finish to start port scanning on every IP using shodan
    for thread in threads:
        thread.join()

    for sub in subdomainDB:
        ip, ports = Shodan(sub).lookup()

        subdomainDB[sub]["IP"] = ip
        subdomainDB[sub]["ports"] = ports
    
    try:
        os.mkdir("results")
    except FileExistsError:
        pass

    with open("results/domains.lst", "w") as f:
        json.dump(subdomainDB, f)

    
        
if __name__ == '__main__':
    main()