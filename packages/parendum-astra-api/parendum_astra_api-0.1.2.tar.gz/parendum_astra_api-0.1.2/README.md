# Parendum Astra API Library

**Parendum OÜ**  
Creation Date: September 2023  
Copyright © 2023 Parendum OÜ. All rights reserved.

## Description

The Parendum Astra API library provides a Python client for interacting with the Parendum Astra API. This library facilitates secure communication with the API, including HMAC signature generation, request header creation, and encrypted response decryption.

## Features

- HMAC signature generation for secure API requests.
- Encrypted response decryption using AES.
- Simple methods for fetching reports and company lists.

## Installation

To use this library in your project, simply install it with the next command.

```bash
pip install git+https://gitlab.com/parendumteam/parendum-astra-api/
```

## Usage

Initialize the API client with your API key and secret:

```python
from parendum_astra_api import ParendumAstraAPI

client = ParendumAstraAPI(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
```

Retrieve reports:

```python
reports = client.get_reports(summary=True)
print(reports)
```

Retrieve a list of companies:

```python
companies = client.get_companies()
print(companies)
```

## Contact

For any inquiries, feedback, or issues, please contact:

- Email: info@parendum.com
- Website: https://parendum.com


## License

Unauthorized use, reproduction, modification, or distribution without the express consent of Parendum OÜ is strictly prohibited.
