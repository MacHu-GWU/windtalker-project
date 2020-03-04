#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from windtalker.asymmetric import AsymmetricCipher


class TestAsymmetricCipher(object):

    def test_encrypt_decrypt_data(self):
        data = "Turn right at blue tree".encode("utf-8")
        A_pubkey, A_privkey = AsymmetricCipher.newkeys()
        B_pubkey, B_privkey = AsymmetricCipher.newkeys()

        cipherA = AsymmetricCipher(A_pubkey, A_privkey, B_pubkey)
        cipherB = AsymmetricCipher(B_pubkey, B_privkey, A_pubkey)

        token = cipherA.encrypt(data)
        sign = cipherA.sign

        data_new = cipherB.decrypt(token, signature=sign)
        assert data == data_new
        assert data != token


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
