Local testing requires Docker and docker-compose
```
python3.14 -m venv .venv
source .venv/bin/activate
```

The Lambda functions and layer use Python 3.14 on Amazon Linux 2023.
Use a SAM CLI version that supports Python 3.14 when building locally.
Lambda responses containing non-ASCII characters are returned as Unicode
rather than escaped JSON sequences on this runtime.