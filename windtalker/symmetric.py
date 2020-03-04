#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import base64

from cryptography.fernet import Fernet
from pathlib_mate import Path

from . import fingerprint
from . import py23
from .cipher import BaseCipher
from .exc import PasswordError

if py23.is_py2:
    input = raw_input

HOME_DIR = Path.home()
WINDTALKER_CONFIG_FILE = Path(HOME_DIR, ".windtalker")


def read_windtalker_password():  # pragma: no cover
    return WINDTALKER_CONFIG_FILE.read_text(encoding="utf-8").strip()


class SymmetricCipher(BaseCipher):
    """
    A symmetric encryption algorithm utility class helps you easily
    encrypt/decrypt text, files and even a directory.

    :param password: The secret password you use to encrypt all your message.
      If you feel uncomfortable to put that in your code, you can leave it
      empty. The system will ask you manually enter that later.

    **中文文档**

    对称加密器。
    """

    _encrypt_chunk_size = 1024 * 1024  # 1 MB
    _decrypt_chunk_size = 1398200  # 1.398 MB
    """Symmtric algorithm needs to break big files in small chunk, and encrypt
    them one by one, and concatenate them at the end. Each chunk has a fixed 
    size. That's what these two attributes for.
    """

    def __init__(self, password=None):
        if password:
            fernet_key = self.any_text_to_fernet_key(password)
            self.fernet = Fernet(fernet_key)  # type: Fernet
        else:  # pragma: no cover
            if WINDTALKER_CONFIG_FILE.exists():
                self.set_password(read_windtalker_password())
            else:
                self.input_password()

    def any_text_to_fernet_key(self, text):
        """
        Convert any text to a fernet key for encryption.

        :type text: str
        :rtype: bytes
        """
        md5 = fingerprint.fingerprint.of_text(text)
        fernet_key = base64.b64encode(md5.encode("utf-8"))
        return fernet_key

    def input_password(self):  # pragma: no cover
        """
        Manually enter a password for encryption on keyboard.
        """
        password = input("Please enter your secret key (case sensitive): ")
        self.set_password(password)

    def set_password(self, password):
        """
        Set a new password for encryption.
        """
        self.__init__(password=password)

    def set_encrypt_chunk_size(self, size):
        if 1024 * 1024 < size < 100 * 1024 * 1024:
            self._encrypt_chunk_size = size
            self._decrypt_chunk_size = len(self.encrypt(b"x" * size))
        else:
            print("encrypt chunk size has to be between 1MB and 100MB")

    @property
    def metadata(self):
        return {
            "_encrypt_chunk_size": self._encrypt_chunk_size,
            "_decrypt_chunk_size": self._decrypt_chunk_size,
        }

    def encrypt(self, binary, *args, **kwargs):
        """
        Encrypt binary data.

        :type binary: bytes
        :rtype: bytes
        """
        return self.fernet.encrypt(binary)

    def decrypt(self, binary, *args, **kwargs):
        """
        Decrypt binary data.

        :type binary: bytes
        :rtype: bytes
        """
        try:
            return self.fernet.decrypt(binary)
        except:
            raise PasswordError("Opps, wrong magic word!")
