import re
import os

class ParseCrtSh:

    def __init__(self, filename, domain):
        
        self.filename = filename
        self.domain = domain
        self.pattern = "\S.*" + self.domain # pattern where string does not contain white space character
        self.clean = "<BR>|>|<|\*"

    @staticmethod
    def eliminate_duplicates(duplicates):

        unique = list(dict.fromkeys(duplicates)) # eliminate duplicates

        for elem in range(len(unique)): # get rid off intial annoying dot
            if unique[elem][0] == '.':
                unique[elem] = unique[elem][1:]
        
        return unique
    
    def cleanup(self):
        with open(self.filename, "r") as f:
            with open("temp.txt", "w") as w:
                w.write(re.sub(self.clean, '\n', f.read()))


    def find_match(self):
        with open("temp.txt", "r") as z:   
            return re.findall(self.pattern, z.read())[9:] # first 9 positions in list are rubbish
        
    
    @staticmethod
    def delete_temp_files():
        os.remove("temp.txt")
        os.remove("out.txt")

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
        

if __name__ == "__main__":
    ParseCrtSh("out.txt", "escriba.es").extract()