import json
import requests

from pwn import *

class EmailHunter:
    def __init__(self, domain, api_key):

        self.url = "https://api.hunter.io/v2/domain-search?domain=" + domain + "&api_key=" + api_key
        self.p1 = log.progress("Scanning emails for " + domain)

    def call_hunterio(self):

        
        r = requests.get(self.url)
        
        if "No user found for the API key supplied" in r.text:
            self.p1.failure("Hunter.io: No user found for the API key supplied")
            return

        else:
            email_list = []
            try:
                emails = json.loads(r.text)["data"]["emails"]

                for email in emails:
                    email_list.append(email['value'])
                    
                self.p1.success("Done!")
                return email_list
            
            except:
                self.p1.failure("Something went wrong, no results came back")
                return
