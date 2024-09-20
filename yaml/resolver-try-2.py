
__all__ = ['BaseResolver', 'Resolver']

from .error import *
from .nodes import *

import re

class ResolverError(YAMLError):
    pass

class BaseResolver:

    DEFAULT_SCALAR_TAG = 'tag:yaml.org,2002:str'
    DEFAULT_SEQUENCE_TAG = 'tag:yaml.org,2002:seq'
    DEFAULT_MAPPING_TAG = 'tag:yaml.org,2002:map'

    yaml_implicit_resolvers = {}
    yaml_path_resolvers = {}
