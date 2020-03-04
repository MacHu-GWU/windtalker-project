#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._version import __version__

__short_description__ = "Super easy-to-use encryption and decryption tool"
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .cipher import BaseCipher
except ImportError:
    pass

try:
    from .symmetric import SymmetricCipher
except ImportError:
    pass

try:
    from .asymmetric import AsymmetricCipher
except ImportError:  # pragma: no cover
    pass
