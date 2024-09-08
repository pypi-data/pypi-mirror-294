# Saldor

Saldor is a Python client library for interacting with the Saldor.com API. It
allows developers to easily integrate Saldor's services into their Python
applications.

## Installation

```
pip install saldor
```

Writing a basic app that uses the client:

```
import os

import saldor

client = saldor.SaldorClient(api_key=os.getenv("SALDOR_API_KEY"))

result = client.crawl(
    url="URL",
    params={},
    max_pages=3,
)
```



