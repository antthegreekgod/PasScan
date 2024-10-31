# PasScan

PasScan is a tool under development to passively scan any target.

3 different datasets are used to gather Open Source Information:
- crt.sh
- shodan.io
- hunter.io

## Usage

```python
python3 ./main.py -d/--domain <single domain scan> -f/--file <read set of domains from file> -e/--email <path to file with hunter.io API_KEY>
```
