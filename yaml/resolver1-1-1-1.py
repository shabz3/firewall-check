
__all__ = ['BaseResolver', 'Resolver']

from .error import *
from .nodes import *

import re

class ResolverError(YAMLError):
    pass