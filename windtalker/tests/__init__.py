# -*- coding: utf-8 -*-

from pathlib_mate import Path

ORIGINAL_FILE = Path(__file__).change(new_basename="my-secret-file.txt").abspath
ENCRYPTED_FILE = Path(__file__).change(new_basename="my-secret-file-encrypted.txt").abspath
DECRYPTED_FILE = Path(__file__).change(new_basename="my-secret-file-decrypted.txt").abspath

ORIGINAL_DIR = Path(__file__).change(new_basename="MySecretFolder").abspath
ENCRYPTED_DIR = Path(__file__).change(new_basename="MySecretFolder-encrypted").abspath
DECRYPTED_DIR = Path(__file__).change(new_basename="MySecretFolder-decrypted").abspath


class BaseTestCipher(object):
    cipher = None

    @property
    def c(self):
        return self.cipher

    def test_encrypt_and_decrypt_binary_and_text(self):
        s = "Turn right at blue tree"
        assert self.c.decrypt_text(self.c.encrypt_text(s)) == s

        b = s.encode("utf-8")
        assert self.c.decrypt_binary(self.c.encrypt_binary(b)) == b

    def test_encrypt_and_decrypt_file(self):
        original_text = Path(ORIGINAL_FILE).read_text()

        self.c.encrypt_file(ORIGINAL_FILE, ENCRYPTED_FILE,
                            overwrite=True, enable_verbose=False)
        encrypted_text = Path(ENCRYPTED_FILE).read_text()

        self.c.decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE,
                            overwrite=True, enable_verbose=False)
        decrypted_text = Path(DECRYPTED_FILE).read_text()

        assert original_text == decrypted_text
        assert original_text != encrypted_text

    def test_encrypt_and_decrypt_dir(self):
        self.c.encrypt_dir(
            ORIGINAL_DIR, ENCRYPTED_DIR,
            overwrite=True, enable_verbose=False
        )
        self.c.decrypt_dir(
            ENCRYPTED_DIR, DECRYPTED_DIR,
            overwrite=True, enable_verbose=False
        )
        for p1, p2 in zip(
                Path(ORIGINAL_DIR).select_file(recursive=True),
                Path(DECRYPTED_DIR).select_file(recursive=True),
        ):
            assert p1.read_bytes() == p2.read_bytes()
