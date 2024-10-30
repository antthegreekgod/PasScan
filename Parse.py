import re
import os

class ParseCrtSh:

    def __init__(self, filename, domain):
        
        self.filename = filename
        self.domain = domain
        self.pattern = "\S.*" + self.domain # pattern where string does not contain white space character
        self.clean = "<BR>|>|<|\*"
        
    def extract(self):
        
        # initial cleanup
        with open(self.filename, "r") as f:
            matches = re.sub(self.clean, '\n', f.read())

        with open("temp.txt", "w") as w:
            w.write(matches)

        # extract matches
        with open("temp.txt", "r") as z:   
            subdomains = re.findall(self.pattern, z.read())

        # remove junk files
        os.remove("temp.txt")
        os.remove("out.txt")
        return subdomains
        