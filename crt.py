import requests

class CrtPassiveScan:

    def __init__(self, domain):

        self.crt = "https://crt.sh/?q="
        self.domain = domain

    def query(self):

        url = self.crt + self.domain
        
        try:
            r = requests.get(url)

            with open("out.txt", "w") as f:
                f.write(r.text)

        except TimeoutError:
            print("[!] crt.sh does not respond")