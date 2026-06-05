# Aurora Origin SDK

## This is under development and not for general use.

## PR Checks

GitHub Actions is set up to run the test suite against multiple versions of Python so that changes can be checked for compatibility.

The tests run against the production API using an API token associated with the `origin-python-sdk-tests@service.auroraer.com` user account. The API token is stored as a secret in GitHub and injected as an environment variable.

## Developing

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) to install dependencies and set up your virtual environment:

```sh
uv sync
```

### Building the documentation

The documentation requires node

```powershell
# If you haven't installed the documentation packages before
cd docsite; npm i;
```

```powershell
# Generate markdown from pydoc strings
uv run pydoc-markdown

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

The site will deploy automatically within a few minutes. The expected documentation can be found
[here](https://auroraenergyresearch.github.io/aurora-origin-python-sdk/).
