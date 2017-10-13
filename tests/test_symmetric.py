#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from windtalker.symmetric import SymmtricCipher
from base import BaseTestCipher


class TestSymmetricCipher(BaseTestCipher):
    cipher = SymmtricCipher(password="MyPassword")
    cipher.set_encrypt_chunk_size(0)
    cipher.set_encrypt_chunk_size(10 * 1024 * 1024)

    cipher.metadata


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
