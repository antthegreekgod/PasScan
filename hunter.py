import json
import sys
import requests

class EmailHunter:
    def __init__(self, domain, api_key):

        self.url = "https://api.hunter.io/v2/domain-search?domain=" + domain + "&api_key=" + api_key

    def call_hunterio(self):

        
        r = requests.get(self.url)
        
        if "No user found for the API key supplied" in r.text:
            return "Hunter.io: No user found for the API key supplied"

        else:
            email_list = []
            try:
                emails = json.loads(r.text)["data"]["emails"]

                for email in emails:
                    email_list.append(email['value'])

                return email_list
            
            except:
                return "Something went wrong, no results came back"