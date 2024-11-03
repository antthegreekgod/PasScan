#!/usr/bin/env python3

from crt import CrtPassiveScan
from hunter import EmailHunter
from shodan import Shodan
from chaos import Chaos
import json
import threading
import argparse
import sys
from os import path

global subdomainDB
subdomainDB = {} # subdomainDB = {"apex1":{},"apex2":{}}

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

    parser.add_argument("-f", "--file", help="File containing apex domains")
    parser.add_argument("-d", "--domain", help="Scan a single domain")    
    
    return parser.parse_args()

def get_key(filename):

    with open(filename, "r") as f:
        return f.read()

def query_chaos(apex):

    api_key = get_key('.chaos')
    subdomains = Chaos(apex, api_key).query_chaos() # Chaos().query_chaos() returns a list, but i'll be turning its elements into dictionary keys
    
    for sub in subdomains:
        subdomainDB[apex]['subdomains'][sub] = {}
                
def query_crt(apex):

    subdomains = CrtPassiveScan(apex).query() # make and save crt.sh petition

    if subdomains: # check if something comes back because crt.sh is not very reliable
        for subdomain in subdomains:
            if subdomain not in subdomainDB[apex]["subdomains"]:

                subdomainDB[apex]["subdomains"][subdomain] = {}
            
    else:
        print("[!] either crt.sh is down or no subdomains were found for the target(s)")

def call_shodan(apex, sub):

    ips, ports = Shodan(sub).lookup()
    
    subdomainDB[apex]["subdomains"][sub]["IPs"] =ips
    subdomainDB[apex]["subdomains"][sub]["Ports"] = ports


def call_hunter(apex):

    api_key = get_key('.hunterio')
    
    
    emails = EmailHunter(apex, api_key).call_hunterio() # passing target and API Key for hunter
        
    if emails:
        subdomainDB[apex]["emails"] = emails

    else:
        subdomainDB[apex]["emails"] = []
        print(f"[!] No emails found for {apex}")


def add_apex(domain, file):
    if domain:
        subdomainDB[domain] = {"subdomains":{}}
    
    if file:
        try:    
            with open (file, "r") as f:        
                apexes = f.read().split()

                for apex in apexes:
                    if apex not in subdomainDB:
                        subdomainDB[apex] = {"subdomains":{}}

        except FileNotFoundError:
            pass


def main():

    args = get_options()


    if not args.domain and not args.file:
        sys.exit("[!] No file nor domain was provided to scan. Use -h or --help to view the help menu")
    
    add_apex(args.domain, args.file) # add apex domains as dictionary keys to subdomainDB

    # start with chaos subdomain enum
    if path.isfile('.chaos'):
        threadsChaos = []

        for apex in subdomainDB.keys():
            thread = threading.Thread(target=query_chaos, args=(apex,))
            threadsChaos.append(thread)
            thread.start()
        
        for thread in threadsChaos:
            thread.join()

    # start subdomain enumeration using crt.sh on background
    threads = []
    for apex in subdomainDB.keys():
        thread = threading.Thread(target=query_crt, args=(apex,))
        threads.append(thread)
        thread.start()


    # if .hunterio file is found, hunt emails using hunter.io api_key
    if path.isfile('.hunterio'):
        for apex in subdomainDB.keys():
            call_hunter(apex)


    # wait for crt.sh to finish to start port scanning on every IP using shodan
    for thread in threads:
        thread.join()

    for apex in subdomainDB:
        for sub in subdomainDB[apex]['subdomains']:
            call_shodan(apex, sub)

    with open("results.json", "w") as f:
        json.dump(subdomainDB, f)

    print("\n[+] Results saved as results.json")

if __name__ == '__main__':
    main()