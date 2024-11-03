# PasScan

PasScan is a tool under development to passively scan any target (domain).

4 different datasets are used to gather Open Source Information:
- crt.sh
- shodan.io
- hunter.io
- chaos from ProjectDiscovery

## Installation

- Clone Git project, create a python virtual environment and install dependencies:
```bash
git clone https://github.com/antthegreekgod/PassiveEnum.git
python3 -m venv ./PassiveEnum
cd ./PassiveEnum
source bin/activate
pip3 install -r requirements.txt
```

## Usage
```python
python3 ./main.py -d/--domain <single domain scan> -f/--file <read set of domains from file>
```
### API Keys
To unleash the full potential of this tool, make sure to include in the following file all its corresponding API Keys:
- .hunterio
- .chaos
