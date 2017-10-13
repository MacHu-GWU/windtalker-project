#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A portable version of ``six``, provide basic python2/3 compatible utilities.
"""

import sys

if sys.version_info[0] == 3:
    str_type = str
    int_type = (int,)
    pk_protocol = 3
    is_py2 = False
    is_py3 = True
else:
    str_type = basestring
    int_type = (int, long)
    pk_protocol = 2
    is_py2 = True
    is_py3 = False
