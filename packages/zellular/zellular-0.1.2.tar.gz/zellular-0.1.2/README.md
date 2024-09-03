# zellular.py

a python sdk for zellular

## Example

### Getting list of nodes

```python
>>> from pprint import pprint
>>> import zellular
>>> operators = zellular.get_operators()
>>> pprint(operators)
{'0x3eaa...078c': {
    'id': '0x3eaa...078c',
    'operatorId': '0xfd17...97fd',
    'pubkeyG1_X': '1313...2753',
    'pubkeyG1_Y': '1144...6864',
    'pubkeyG2_X': ['1051...8501', '1562...5720'],
    'pubkeyG2_Y': ['1601...1108', '1448...1899'],
    'public_key_g2': <eigensdk.crypto.bls.attestation.G2Point object at 0x7d8f31b167d0>,
    'socket': 'http://5.161.230.186:6001',
    'stake': 1
}, ... }
```

### Posting


### Fetching & Verifying

```python
>>> from pprint import pprint
>>> import zellular
>>> operators = zellular.get_operators()
