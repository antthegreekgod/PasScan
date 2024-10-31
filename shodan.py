from dns import resolver
import requests
import json

class Shodan:

    def __init__(self, domain):

        self.url = 'https://internetdb.shodan.io/'
        self.domain = domain
        self.ips = []
        self.ports = []

        try:
            ips = resolver.query(domain, "A")

        except Exception:
            return

        for ip in ips:
            self.ips.append(ip.to_text())

    def lookup(self):
        
        for ip in self.ips:
            r = requests.get(self.url + ip)
            response = json.loads(r.text)
            try:
                self.ports.append(response["ports"])
            except KeyError:
                continue

        return self.ips, self.ports