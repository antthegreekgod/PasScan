import re

class ParseCrtSh:

    def __init__(self, filenameme, domain):
        
        self.filename = filename
        self.domain = domain
        
    def extract(self):

        with open(self.filename, "r") as f:
            matches = re.findall(self.domain)

        print(matches)


def main():
    domain = "dentaid.com"
    ParseCrtSh("out.txt", domain).extract()

if __name__ == "__main__":
    main()