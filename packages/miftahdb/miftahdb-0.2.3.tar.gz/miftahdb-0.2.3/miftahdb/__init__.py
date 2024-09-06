__version__ = "0.2.3"
__copyright__ = (
    "Copyright (c) 2024 miftahDB ~ https://github.com/miftahDB/miftahdb-python"
)
__license__ = "MIT License"

VERSION = __version__

__all__ = ["Client", "PickleEncoder", "StringEncoder", "sync"]

from .client import Client
from .encoders import PickleEncoder, StringEncoder
from . import sync
