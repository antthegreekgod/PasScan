#!/usr/bin/env python3

import requests

class PassiveScan:

    def __init__(self, domain):

        self.crt = "https://crt.sh/?q="
        self.domain = domain

    def query(self):

        url = self.crt + self.domain
        r = requests.get(url)

        with open("out.txt", "w") as f:
            f.write(r.text)

def main():

    with open ("apex.lst", "r") as f:        
        domains = f.read().split()
    
    for domain in domains:
        PassiveScan(domain).query()

if __name__ == '__main__':
    main()

