import os

import pytest

for key, value in os.environ.items():
    print(f"{key}: {value}")

# Disable tests in code build due to lack of internet access
if os.getenv("CODEBUILD_BUILD_ID"):

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(config, items):
        items[:] = [item for item in items if "test_placeholder" in item.nodeid]
