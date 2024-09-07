# Python Authentication for FIWARE Data Space (FDSAuth) ![example workflow](https://github.com/CitCom-VRAIN/fdsauth/actions/workflows/package.yml/badge.svg)
Welcome to the **Python Authentication for FIWARE Data Space** repository. This library, or **FDSAuth**, facilitates seamless FIWARE Data Space framework authentication. With built-in support for various authentication protocols and methods, FDSAuth helps developers implement secure and reliable authentication in their applications, ensuring compliance with FIWARE standards and best practices.

## Table of Contents 📚
- [Python Authentication for FIWARE Data Space (FDSAuth) ](#python-authentication-for-fiware-data-space-fdsauth-)
  - [Table of Contents 📚](#table-of-contents-)
  - [Installation 🛠️](#installation-️)
  - [Usage  💻](#usage--)
  - [Development 🚀](#development-)
  - [Contact 📫](#contact-)
  - [Acknowledgments 🙏](#acknowledgments-)

## Installation 🛠️
To install FDSAuth, simply use `pip`:

```bash
pip install fdsauth
```

## Usage  💻
First, define following environment variables in your `.env` file. Substitute example values for your own:
```bash
KEYCLOAK_PROTOCOL=http
KEYCLOAK_ENDPOINT=keycloak-consumer.127.0.0.1.nip.io:8080
KEYCLOAK_USERNAME=test-user
KEYCLOAK_PASSWORD=test
```

Usage example:
```python
from dotenv import load_dotenv
from fdsauth import Consumer

# Load environment variables from .env file
load_dotenv()

# Create a Consumer instance and retrieve the verifiable credential
consumer = Consumer()
jwt_credential = consumer.get_auth_token()
print(jwt_credential)
```

## Development 🚀
```bash
# Create virtual env
python3 -m venv ./venv && source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build
python setup.py sdist bdist_wheel

# Local testing
pip install dist/fdsauth-X.X.X-py3-none-any.whl
```

## Contact 📫
For any questions or support, please reach out to us via GitHub Issues or email us at [joamoteo@upv.es](mailto:joamoteo@upv.es).

## Acknowledgments 🙏
This work has been made by **VRAIN** for the **CitCom.ai** project, co-funded by the EU.

<img src="https://vrain.upv.es/wp-content/uploads/2022/01/vrain_1920_1185.jpg" alt="VRAIN" width="200"/>
<img src="https://www.fiware.org/wp-content/directories/research-development/images/citcom-ai.png" alt="CitCom.ai" width="200"/>
