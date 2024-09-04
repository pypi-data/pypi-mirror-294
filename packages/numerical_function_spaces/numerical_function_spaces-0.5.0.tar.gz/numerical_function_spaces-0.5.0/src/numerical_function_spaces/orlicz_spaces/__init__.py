# read version from installed package
from importlib.metadata import version
__version__ = version("numerical_function_spaces")

from .norms import *
from .orlicz_functions import *
from .plots import *
from .conjugate import *
