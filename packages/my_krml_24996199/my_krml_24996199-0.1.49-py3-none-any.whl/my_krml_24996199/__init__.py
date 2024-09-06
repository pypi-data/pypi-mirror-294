# read version from installed package
from importlib.metadata import version
__version__ = version("my_krml_24996199")

from my_krml_24996199.features.build_features import build_features