import requests
import json
from pwn import *

class Chaos:

    def __init__(self, domain, api_key):

        self.url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"
        self.headers = {"Authorization":api_key, "Connection":"close"}
        self.domain = domain
        self.p1 = log.progress("Scanning " + domain + " with chaos")

    def query_chaos(self):

        r = requests.get(self.url, headers=self.headers)
        sub = json.loads(r.text)["subdomains"]
        self.p1.success("Done!")
        return self.fqdn(sub) # this will return the full qualified domain name

    def fqdn(self, subdomains):
        if '*' in subdomains:
            subdomains.remove("*") # remove the annoying wildcards

        for item in range(len(subdomains)):
            subdomains[item] = str(subdomains[item]) + "." + self.domain
	
        return subdomains
        
        
