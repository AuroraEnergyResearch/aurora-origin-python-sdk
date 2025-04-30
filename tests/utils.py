import os


def is_running_in_ci() -> bool:
    return "CI" in os.environ
