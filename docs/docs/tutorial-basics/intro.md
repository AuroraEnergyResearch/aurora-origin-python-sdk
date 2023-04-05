---
sidebar_position: 1
sidebar_label: Installation
title: Installation
description: Getting the SDK installed and authenticated
---

# Installation

1. Install the package from the git repository

```bash
pip install git+https://github.com/AuroraEnergyResearch/aurora-origin-python-sdk
```

2. Add your Aurora API key to the file $home/.aurora-api-key

3. Import `OriginSession` and initialise. See
   [OriginSession](/docs/reference/OriginSession) for details on usage.

```python
from origin_sdk.OriginSession import OriginSession
session  = OriginSession()
result  = session.get_projects()
print(res[0])
```
