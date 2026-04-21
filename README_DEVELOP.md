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

Build the documentation locally with Sphinx:

```sh
uv run sphinx-build -M clean docs docs/_build
uv run sphinx-build -E -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html` to inspect the rendered site locally.

### Deploying the documentation

Documentation deployment is handled by GitHub Actions on pushes to `main`. The deploy workflow builds the Sphinx site and publishes the generated HTML to GitHub Pages.

The expected documentation can be found [here](https://ghp.auroraer.com/aurora-origin-python-sdk/).
