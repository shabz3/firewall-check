# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2023 Vinay Sajip.
# Licensed to the Python Software Foundation under a contributor agreement.
# See LICENSE.txt and CONTRIBUTORS.txt.
#
"""
Parser for the environment markers micro-language defined in PEP 508.
"""

# Note: In PEP 345, the micro-language was Python compatible, so the ast
# module could be used to parse it. However, PEP 508 introduced operators such
# as ~= and === which aren't in Python, necessitating a different approach.

import os
import re
import sys
import platform

from .compat import string_types
from .util import in_venv, parse_marker
from .version import LegacyVersion as LV

__all__ = ['interpret']

_VERSION_PATTERN = re.compile(r'((\d+(\.\d+)*\w*)|\'(\d+(\.\d+)*\w*)\'|\"(\d+(\.\d+)*\w*)\")')
_VERSION_MARKERS = {'python_version', 'python_full_version'}


def _is_version_marker(s):
    return isinstance(s, string_types) and s in _VERSION_MARKERS


def _is_literal(o):
    if not isinstance(o, string_types) or not o:
        return False
    return o[0] in '\'"'


def _get_versions(s):
    return {LV(m.groups()[0]) for m in _VERSION_PATTERN.finditer(s)}
