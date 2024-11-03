import requests
import re
from os import remove
from pwn import *

class CrtPassiveScan:

    def __init__(self, domain):

        self.crt = "https://crt.sh/?q="
        self.domain = domain
        self.pattern = "\S.*" + self.domain # pattern where string does not contain white space character
        self.clean = "<BR>|>|<|\*"
        self.temp1 = f"{domain}-temp1.txt"
        self.temp2 = f"{domain}-temp2.txt"
        self.p1 = log.progress("Scanning " + domain + " with crt.sh")


    def query(self):

        url = self.crt + self.domain
        
        try:
            r = requests.get(url)

            with open(self.temp1, "w") as f:
                f.write(r.text)
            
            subdomains = self.extract()
            self.p1.success("Done!")
            return subdomains

        except TimeoutError:
            self.p1.failure("crt.sh does not respond")
            return

    @staticmethod
    def eliminate_duplicates(duplicates):

        unique = list(dict.fromkeys(duplicates)) # eliminate duplicates

        for elem in range(len(unique)): # get rid off intial annoying dot
            if unique[elem][0] == '.':
                unique[elem] = unique[elem][1:]
        
        return unique
    
    def cleanup(self):
        with open(self.temp1, "r") as f:
            with open(self.temp2, "w") as w:
                w.write(re.sub(self.clean, '\n', f.read()))


    def find_match(self):
        with open(self.temp2, "r") as z:   
            return re.findall(self.pattern, z.read())[9:] # first 9 positions in list are rubbish
        
    
    def delete_temp_files(self):
        remove(self.temp1)
        remove(self.temp2)

    def extract(self):

        # make some modifications to file with crt.sh response for easier regex pattern matching
        self.cleanup()    

        # extract matches
        subdomains_duplicates = self.find_match()
        
        # remove duplicates
        subdomains = self.eliminate_duplicates(subdomains_duplicates)

        # delete temp files
        self.delete_temp_files()

        return subdomains
