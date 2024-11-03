# PasScan

PasScan is a tool under development to passively scan any target.

3 different datasets are used to gather Open Source Information:
- crt.sh
- shodan.io
- hunter.io
- chaos from ProjectDiscovery

## Installation

- Clone Git project, create a python virtual environment and install dependencies:
```bash
git clone git@github.com:antthegreekgod/PassiveEnum.git
python3 -m venv ./PassiveEnum
cd ./PassiveEnum
source bin/activate
pip3 install -r requirements.txt
```

## Usage

```python
python3 ./main.py -d/--domain <single domain scan> -f/--file <read set of domains from file> -e/--email <path to file with hunter.io API_KEY>
```
