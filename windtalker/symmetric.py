#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import io
import os
import time
import base64

from cryptography.fernet import Fernet

from windtalker.cipher import BaseCipher
from windtalker.exc import PasswordError
from windtalker import hashes
from windtalker import files
from windtalker import py23


if py23.is_py2:
    input = raw_input


class SymmtricCipher(Fernet, BaseCipher):
    """A symmtric encryption algorithm utility class helps you easily 
    encrypt/decrypt text, files and even a directory.

    :param password: The secret password you use to encrypt all your message.
      If you feel uncomfortable to put that in your code, you can leave it 
      empty. The system will ask you manually enter that later.

    **中文文档**

    对称加密算法
    """
    _encrypt_chunk_size = 1024 * 1024  # 1 MB
    _decrypt_chunk_size = 1398200  # 1.398 MB

    def __init__(self, password=None):
        if password:
            fernet_key = self.any_text_to_fernet_key(password)
            super(SymmtricCipher, self).__init__(fernet_key)
        else:
            self.input_password()

    def any_text_to_fernet_key(self, text):
        md5 = hashes.fingerprint.of_text(text)
        fernet_key = base64.b64encode(md5.encode("utf-8"))
        return fernet_key

    def input_password(self):
        self.set_password(input(
            "Please enter your secret key (case sensitive): "))

    def set_password(self, password):
        self.__init__(password)

    def set_encrypt_chunk_size(self, size):
        if 1024 * 1024 < size < 100 * 1024 * 1024:
            self._encrypt_chunk_size = size
            self._decrypt_chunk_size = len(self.encrypt(b"x" * size))
        else:
            print("encrypt chunk size has to be between 1MB and 100MB")

    @property
    def metadata(self):
        return {"_encrypt_chunk_size": self._encrypt_chunk_size,
                "_decrypt_chunk_size": self._decrypt_chunk_size, }

    def encrypt(self, content):
        return super(SymmtricCipher, self).encrypt(content)

    def decrypt(self, content):
        try:
            return super(SymmtricCipher, self).decrypt(content)
        except:
            raise PasswordError("Opps, wrong magic word!")