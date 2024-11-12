import os

pytest_plugins = ["input_tests.utils_for_testing"]


for key, value in os.environ.items():
    print(f"{key}: {value}")

# Disable tests in code build due to lack of internet access
if os.getenv("CODEBUILD_BUILD_ID"):
    collect_ignore_glob = ["*test_*.py"]
