import os

pytest_plugins = ["input_tests.utils_for_testing"]


for key, value in os.environ.items():
    print(f"{key}: {value}")

# Disable tests in code build due to lack of internet access
collect_ignore = ["setup.py"]
if os.getenv("CODEBUILD_BUILD_ID"):
    collect_ignore.append("tests/*")
    collect_ignore_glob = ["*.py"]
