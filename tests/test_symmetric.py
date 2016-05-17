#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from windtalker import files
from windtalker.symmetric import SymmtricCipher


class Unittest(unittest.TestCase):
    def test_input_password(self):
        cipher = SymmtricCipher()

        message = "Turn right at blue tree"
        encrypted = cipher.encrypt_text(message)

        decrypted = cipher.encrypt_text(message)
        self.assertNotEqual(message, decrypted)

    def test_encrypt_decrypt_text(self):
        cipher = SymmtricCipher(password="MyPassword")

        message = "Turn right at blue tree"
        encrypted = cipher.encrypt_text(message)

        decrypted = cipher.encrypt_text(encrypted)
        self.assertNotEqual(message, encrypted)

    def test_encrypt_decrypt_file(self):
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

        cipher = SymmtricCipher(password="MyPassword")
        cipher.encrypt_file(src, dst, overwrite=True)
        cipher.decrypt_file(dst, src_new, overwrite=True)

        # compare before after file
        with open(src_new, "rb") as f:
            self.assertEqual(f.read().decode("utf-8"), message)

        # clear test file
        for path in [src, dst, src_new]:
            try:
                os.remove(path)
            except Exception as e:
                print(e)
                pass

    def test_encrypt_decrypt_dir(self):
        dir_path = "MySecretFolder"
        dir_path_encrypted = "MySecretFolder-encrypted"
        dir_path_decrypted = "MySecretFolder-decrypted"
 
        cipher = SymmtricCipher(password="MyPassword")
        cipher.encrypt_dir(dir_path, dir_path_encrypted, overwrite=True)
        cipher.decrypt_dir(dir_path_encrypted,
                           dir_path_decrypted, overwrite=True)

unittest.main()