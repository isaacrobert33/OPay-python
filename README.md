# Opay Python Library

[![pypi](https://img.shields.io/pypi/v/opay-python.svg)](https://pypi.python.org/pypi/opay-python)

The OPay Python library provides convenient access to the OPay merchant API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses which makes the OPay resources easily accessed and enhances 
transaction ease via the OPay API.

## Installation

You wouldn't need this source code unless you want to modify or contribute to the package. If you just
want to use the package, just run:

```sh
pip install --upgrade opay-python
```

Install from source with:

```sh
python setup.py install
```

### Requirements

-   Python 3.7+

## Usage
For every instance of the Library you would need your opay merchant credentials which are your 
`merchantId` & `public_key`. You can get both on your merchant dashboard.

```python
from opay_python import OpayTransfers

# Instantiate the class
opay = OpayTransfers(public_key=`<public_key>`, merchant_id=`<merchantId>`)

# Initialize a transfer to an Opay wallet
response = opay.to_opay_wallet(
        amount='12000', reason='API Test', phone_number="+2348123456789", wallet_type="USER"
        )

# print the API's response to view the transaction's status
print(response)
```

## License 

[MIT](./LICENSE)
