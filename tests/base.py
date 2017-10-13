#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib_mate import Path


class BaseTestCipher(object):
    cipher = None

    @property
    def c(self):
        return self.cipher

    def test_binary_and_text(self):
        s = "Turn right at blue tree"
        assert self.c.decrypt_text(self.c.encrypt_text(s)) == s

        b = s.encode("utf-8")
        assert self.c.decrypt_binary(self.c.encrypt_binary(b)) == b

    def test_file(self):
        original = Path(__file__).change(
            new_basename="my-secret-file.txt").abspath
        encrypted = Path(__file__).change(
            new_basename="my-secret-file-encrypted.txt").abspath
        decrypted = Path(__file__).change(
            new_basename="my-secret-file-decrypted.txt").abspath

        original_text = Path(original).read_text()

        self.c.encrypt_file(original, encrypted,
                            overwrite=True, enable_verbose=False)
        encrypted_text = Path(encrypted).read_text()

        self.c.decrypt_file(encrypted, decrypted,
                            overwrite=True, enable_verbose=False)
        decrypted_text = Path(decrypted).read_text()

        assert original_text == decrypted_text

        for path in [encrypted, decrypted]:
            try:
                Path(path).remove()
            except:
                pass

    def test_dir(self):
        dir_path = Path(__file__).change(
            new_basename="MySecretFolder").abspath
        dir_path_encrypted = Path(__file__).change(
            new_basename="MySecretFolder-encrypted").abspath
        dir_path_decrypted = Path(__file__).change(
            new_basename="MySecretFolder-decrypted").abspath

        self.c.encrypt_dir(dir_path, dir_path_encrypted,
                           overwrite=True, enable_verbose=False)
        self.c.decrypt_dir(dir_path_encrypted, dir_path_decrypted,
                           overwrite=True, enable_verbose=False)
        for p1, p2 in zip(
                Path(dir_path).select_file(recursive=True),
                Path(dir_path_decrypted).select_file(recursive=True),
        ):
            assert p1.read_bytes() == p2.read_bytes()
