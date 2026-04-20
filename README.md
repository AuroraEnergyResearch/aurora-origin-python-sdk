# Aurora Origin SDK

Python SDK for accessing data from Origin, Aurora's market model platform.

# Installation

We currently support running the SDK on all currently supported version of Python: 3.10 - 3.14.

1. Install the package from the git repository

```bash
# Use pip:
pip install aurora-origin-sdk
# Or uv:
uv add aurora-origin-sdk
```

2. Add your Aurora API key to the file `$home/.aurora-api-key`. for example `C:\Users\Joe Bloggs\.aurora-api-key` or set as the environment variable `AURORA_API_KEY`.

3. Import `OriginSession` and initialise.

```python
from origin_sdk.OriginSession import OriginSession
session  = OriginSession()
result  = session.get_projects()
print(res[0])
```

4. See
   [the documentation](https://auroraenergyresearch.github.io/aurora-origin-python-sdk)
   for further details on the SDK.
