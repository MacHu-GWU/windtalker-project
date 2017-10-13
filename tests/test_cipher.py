#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from pytest import raises, approx

from windtalker.cipher import BaseCipher
from base import BaseTestCipher


class MyCipher(BaseCipher):
    def decrypt(self, binary, *args, **kwargs):
        return binary

    def encrypt(self, binary, *args, **kwargs):
        return binary


c = MyCipher()


def test_base64():
    s = "hello"
    assert c.b64decode_str(c.b64encode_str(s)) == s


class TestBaseCipher(BaseTestCipher):
    cipher = c


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
