# Aurora Origin SDK

This is under development

# Installation

1. Install the package from the git repository

```bash
# Use pip:
pip install git+https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk
# Or uv:
uv add git+https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk
```

2. Add your Aurora API key to the file $home/.aurora-api-key. for example `C:\Users\Joe Bloggs\.aurora-api-key` or set as the environment variable `AURORA_API_KEY`.

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
