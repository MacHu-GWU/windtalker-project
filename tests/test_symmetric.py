#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from windtalker.symmetric import SymmetricCipher
from windtalker.exc import PasswordError
from base import BaseTestCipher


class TestSymmetricCipher(BaseTestCipher):
    cipher = SymmetricCipher(password="MyPassword")
    cipher.set_encrypt_chunk_size(0)
    cipher.set_encrypt_chunk_size(10 * 1024 * 1024)

    cipher.metadata

    def test_decrypt_with_password(self):
        encrypted_text = self.cipher.encrypt_text("Hello World")
        cipher = SymmetricCipher(password="MyPassword")
        cipher.set_password(password="AnotherPassword")
        with pytest.raises(PasswordError):
            cipher.decrypt_text(encrypted_text)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
