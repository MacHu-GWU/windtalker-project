# -*- coding: utf-8 -*-

import base64

from windtalker.cipher import BaseCipher
from windtalker.tests import BaseTestCipher


class MyCipher(BaseCipher):
    def encrypt(self, binary, *args, **kwargs):
        return (base64.b64encode(binary).decode("utf-8") + "X").encode("utf-8")

    def decrypt(self, binary, *args, **kwargs):
        return base64.b64decode(binary.decode("utf-8")[:-1].encode("utf-8"))


c = MyCipher()


def test_base64():
    s = "hello"
    assert c.b64decode_str(c.b64encode_str(s)) == s


class TestBaseCipher(BaseTestCipher):
    cipher = c


if __name__ == "__main__":
    from windtalker.tests import run_cov_test

    run_cov_test(__file__, "windtalker.cipher", preview=False)
