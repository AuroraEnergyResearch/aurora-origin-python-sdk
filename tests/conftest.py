import os

pytest_plugins = ["input_tests.utils_for_testing"]


# Disable tests in code build due to lack of internet access
if os.getenv("AWS_REGION"):
    collect_ignore_glob = ["*.py"]
