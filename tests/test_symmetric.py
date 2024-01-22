# -*- coding: utf-8 -*-

import pytest

from windtalker.symmetric import SymmetricCipher
from windtalker.exc import PasswordError
from windtalker.tests import BaseTestCipher


class TestSymmetricCipher(BaseTestCipher):
    cipher = SymmetricCipher(password="MyPassword")
    with pytest.raises(ValueError):
        cipher.set_encrypt_chunk_size(0)
    cipher.set_encrypt_chunk_size(10 * 1024 * 1024)

    _ = cipher.metadata

    def test_decrypt_with_password(self):
        encrypted_text = self.cipher.encrypt_text("Hello World")
        cipher = SymmetricCipher(password="MyPassword")
        cipher.set_password(password="AnotherPassword")
        with pytest.raises(PasswordError):
            cipher.decrypt_text(encrypted_text)


if __name__ == "__main__":
    from windtalker.tests import run_cov_test

    run_cov_test(__file__, "windtalker.symmetric", preview=False)
