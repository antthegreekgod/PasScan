#!/usr/bin/env python3

from crt import CrtPassiveScan
import parse
import threading


def query(domain):
    CrtPassiveScan(domain).query() # make and save crt.sh petition
    subdomains = parse.ParseCrtSh("out.txt", domain).extract() # crawl file and extract subdomains
    print(subdomains)


def main():

    with open ("apex.lst", "r") as f:        
        domains = f.read().split()
    
    threads = []
    for domain in domains:
        thread = threading.Thread(target=query, args=(domain,))
        threads.append(thread)

    for thread in threads:
        thread.start()

if __name__ == '__main__':
    main()

