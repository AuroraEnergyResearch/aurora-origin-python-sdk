# Installation

1. Install the package from the Git repository.

```bash
# Use pip:
pip install git+https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk

# Or uv:
uv add git+https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk
```

2. Add your Aurora API key to `$HOME/.aurora-api-key`, for example `C:\\Users\\Joe Bloggs\\.aurora-api-key`, or set the `AURORA_API_KEY` environment variable.

3. Import `OriginSession` and initialise it.

```python
from origin_sdk.OriginSession import OriginSession

session = OriginSession()
result = session.get_projects()
print(result[0])
```
