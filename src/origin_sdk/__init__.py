from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("aurora_origin_sdk")
except PackageNotFoundError:
    __version__ = "unknown"
