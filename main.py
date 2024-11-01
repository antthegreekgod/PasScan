#!/usr/bin/env python3

from crt import CrtPassiveScan
from hunter import EmailHunter
from shodan import Shodan
from chaos import Chaos
import json
import threading
import argparse
import sys
from os import path, mkdir
from pwn import *

global subdomainDB
subdomainDB = {}

def get_options():

    desc = """Passively scan a set of domains. This tool has been designed to query multiple datasets. Such are: crt.sh, hunter.io, chaos etc. 
    Please make sure to provide a valid API key for each service. 
    API KEY Files:
    .hunterio
    .chaos
"""

    parser = argparse.ArgumentParser(prog="PasScan",
                                     description=desc,
                                     epilog="Author: @antthegreekgod"
                                     )

    parser.add_argument("-f", "--file", default="apex.lst", help="File containing apex domains, if no file is provided it will try to scan the current directory for a file named \"apex.lst\"")
    parser.add_argument("-d", "--domain", help="Scan a single domain")    
    
    return parser.parse_args()

def get_key(filename):

    with open(filename, "r") as f:
        return f.read()

def query_chaos(domain):

    api_key = get_key('.chaos')
    subdomains = Chaos(domain, api_key).query_chaos()
    
    print(subdomains)

def query_crt(domain):

    subdomains = CrtPassiveScan(domain).query() # make and save crt.sh petition
    if subdomains:
        for subdomain in subdomains:
            if subdomain not in subdomainDB:
                subdomainDB[subdomain] = {"IP":"","ports":""}
    else:
        print("[!] either crt.sh is down or no subdomains were found for the target(s)")

def call_hunter(domains):

    api_key = get_key('.hunterio')
    
    for domain in domains:
        emails = EmailHunter(domain, api_key).call_hunterio() # passing target and API Key for hunter
        
        if emails:
            try:
                mkdir("results")
            except FileExistsError:
                pass
                    
            with open(f"results/{domain}-emails.lst", "w") as f:
                for email in emails:
                    f.write(email + "\n")

        else:
            print(f"[!] No emails found for {domain}")


def main():

    args = get_options()

    domains = []

    # if --domain
    if args.domain:
        domains.append(args.domain)

    # if --file
    if args.file:
        try:    
            with open (args.file, "r") as f:        
                domains = f.read().split()
        except FileNotFoundError:
            pass

    threads = []
    if not domains:
        sys.exit("[!] No file nor domain was provided to scan. Use -h or --help to view the help menu")

    # start with chaos subdomain enum
    if path.isfile('.chaos'):
        threadsChaos = []

        for domain in domains:
            thread = threading.Thread(target=query_chaos, args=(domain,))
            threadsChaos.append(thread)
            thread.start()

    # start subdomain enumeration using crt.sh on background
    for domain in domains:
        thread = threading.Thread(target=query_crt, args=(domain,))
        threads.append(thread)
        thread.start()

    # if .hunterio file is found, hunt emails using hunter.io api_key
    if path.isfile('.hunterio'):
        call_hunter(domains)


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