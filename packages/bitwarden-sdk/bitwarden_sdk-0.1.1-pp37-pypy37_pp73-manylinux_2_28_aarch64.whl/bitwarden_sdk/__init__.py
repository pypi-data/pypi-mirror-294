"""The official Bitwarden client library for Python."""

__version__ = "0.1.1"

from .bitwarden_client import *
from .schemas import *

__doc__ = bitwarden_client.__doc__
if hasattr(bitwarden_client, "__all__"):
    __all__ = bitwarden_client.__all__

if hasattr(schemas, "__all__"):
    __all__ += schemas.__all__
