# Aurora Origin SDK compatibility package

`aurora-origin-sdk` is the legacy distribution name for the Aurora Origin Python
SDK. Version 0.32.0 is a metadata-only compatibility package that installs the
replacement [`auroraer-origin-sdk` package from PyPI](https://pypi.org/project/auroraer-origin-sdk/).

New installations should depend on the replacement package directly:

```bash
pip install auroraer-origin-sdk
```

Existing `import origin_sdk` statements continue to work because the replacement
distribution provides the same Python package.

The legacy notebook extra is also forwarded to the replacement package:

```bash
pip install "aurora-origin-sdk[notebooks]"
```

New installations should reference the replacement extra directly:

```bash
pip install "auroraer-origin-sdk[notebooks]"
```
