#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest

from windtalker.asymmetric import AsymmetricCipher


class TestAsymmetricCipher(object):
    def test_encrypt_decrypt_data(self):
        """
        """
        data = "Turn right at blue tree".encode("utf-8")
        A_pubkey, A_privkey = AsymmetricCipher.newkeys()
        B_pubkey, B_privkey = AsymmetricCipher.newkeys()

        cipherA = AsymmetricCipher(A_pubkey, A_privkey, B_pubkey)
        cipherB = AsymmetricCipher(B_pubkey, B_privkey, A_pubkey)

        token = cipherA.encrypt(data)
        sign = cipherA.sign

        data_new = cipherB.decrypt(token, signature=sign)
        assert data == data_new

    def test_encrypt_decrypt_file(self):
        """
        """
        src = "secret.txt"
        dst = "secret-encrypted.txt"
        src_new = "secret-decrypted.txt"

        # create a test file
        message = "Turn right at blue tree"
        try:
            with open(src, "wb") as f:
                f.write(message.encode("utf-8"))
        except:
            pass

        # A want send B a file
        A_pubkey, A_privkey = AsymmetricCipher.newkeys()
        B_pubkey, B_privkey = AsymmetricCipher.newkeys()

        # A use B_pubkey for encryption
        cipherA = AsymmetricCipher(A_pubkey, A_privkey, B_pubkey)
        cipherA.encrypt_file(src, dst, overwrite=True)

        # B use B_privkey for decryption
        cipherB = AsymmetricCipher(B_pubkey, B_privkey, A_pubkey)
        cipherB.decrypt_file(dst, src_new, overwrite=True)

        # compare before after file
        with open(src_new, "rb") as f:
            assert f.read().decode("utf-8") == message

        # clear test file
        for path in [src, dst, src_new]:
            try:
                os.remove(path)
            except Exception as e:
                print(e)
                pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
