# Aurora Origin SDK

## This is under development and not for general use.

## Developing

### Create a venv and activate if required

```powershell
python -m venv .venv
#enable python virtual environment
.\.venv\Scripts\activate
```

### Install dependencies

```powershell
# This install this module as symlinks to and all dependencies including the ones needed locally.
# It uses setup.py to find dependancies.
pip install -e  .[development] # This install this module as symlinks to and all dependencies including the ones needed locally.

# If you haven't installed the documentation packages before
cd docsite; npm i;
```

### Building the documentation

```powershell
.\.venv\Scripts\Activate.ps1

# Generate markdown from pydoc strings
pydoc-markdown

# Also update any of the markdown inside docsite/docs
cd docsite
npm run build
```

### Deploying the documentation

```powershell
cd docsite
npm run deploy_ghpages
```

Then check the result into `main`.

The site will deploy automatically within a few minutes. This expected the
documentation can be found
[here](https://auroraenergyresearch.github.io/aurora-origin-python-sdk/).
