# -*- coding: utf-8 -*-

import typing as T
import base64

from cryptography.fernet import Fernet
from .vendor.hashes import hashes

from .exc import PasswordError
from .paths import path_windtalker
from .cipher import BaseCipher


def read_windtalker_password():  # pragma: no cover
    return path_windtalker.read_text(encoding="utf-8").strip()


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

    def __init__(self, password: T.Optional[str] = None):
        if password:
            fernet_key = self.any_text_to_fernet_key(password)
            self.fernet = Fernet(fernet_key)  # type: Fernet
        else:  # pragma: no cover
            if path_windtalker.exists():
                self.set_password(read_windtalker_password())
            else:
                self.input_password()

    def any_text_to_fernet_key(self, text: str) -> bytes:
        """
        Convert any text to a fernet key for encryption.
        """
        md5 = hashes.of_str(text)
        fernet_key = base64.b64encode(md5.encode("utf-8"))
        return fernet_key

    def input_password(self):  # pragma: no cover
        """
        Manually enter a password for encryption on keyboard.
        """
        password = input("Please enter your secret key (case sensitive): ")
        self.set_password(password)

    def set_password(self, password: str):
        """
        Set a new password for encryption.
        """
        self.__init__(password=password)

    def set_encrypt_chunk_size(self, size: int):
        if 1024 * 1024 < size < 100 * 1024 * 1024:
            self._encrypt_chunk_size = size
            self._decrypt_chunk_size = len(self.encrypt(b"x" * size))
        else:
            raise ValueError(
                f"Cannot set encrypt chunk size = {size}, "
                f"encrypt chunk size has to be between 1MB and 100MB"
            )

    @property
    def metadata(self) -> dict:
        return {
            "_encrypt_chunk_size": self._encrypt_chunk_size,
            "_decrypt_chunk_size": self._decrypt_chunk_size,
        }

    def encrypt(self, binary: bytes, *args, **kwargs) -> bytes:
        """
        Encrypt binary data.
        """
        return self.fernet.encrypt(binary)

    def decrypt(self, binary: bytes, *args, **kwargs) -> bytes:
        """
        Decrypt binary data.
        """
        try:
            return self.fernet.decrypt(binary)
        except:
            raise PasswordError("Ops, wrong magic word!")
