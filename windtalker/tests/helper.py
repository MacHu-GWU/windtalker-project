# -*- coding: utf-8 -*-

from ..paths import dir_project_root, dir_htmlcov, dir_tests_lib
from ..vendor.pytest_cov_helper import run_cov_test as _run_cov_test


def run_cov_test(
    script: str,
    module: str,
    preview: bool = False,
    is_folder: bool = False,
):
    _run_cov_test(
        script=script,
        module=module,
        root_dir=f"{dir_project_root}",
        htmlcov_dir=f"{dir_htmlcov}",
        preview=preview,
        is_folder=is_folder,
    )


p_original = dir_tests_lib / "my-secret-file.txt"
p_encrypted = dir_tests_lib / "my-secret-file-encrypted.txt"
p_decrypted = dir_tests_lib / "my-secret-file-decrypted.txt"

dir_original = dir_tests_lib / "MySecretFolder"
dir_encrypted = dir_tests_lib / "MySecretFolder-encrypted"
dir_decrypted = dir_tests_lib / "MySecretFolder-decrypted"


class BaseTestCipher:
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
        original_text = p_original.read_text()

        self.c.encrypt_file(
            p_original,
            p_encrypted,
            overwrite=True,
            enable_verbose=False,
        )
        encrypted_text = p_encrypted.read_text()

        self.c.decrypt_file(
            p_encrypted,
            p_decrypted,
            overwrite=True,
            enable_verbose=False,
        )
        decrypted_text = p_decrypted.read_text()

        assert original_text == decrypted_text
        assert original_text != encrypted_text

    def test_encrypt_and_decrypt_dir(self):
        self.c.encrypt_dir(
            dir_original,
            dir_encrypted,
            overwrite=True,
            enable_verbose=False,
        )
        self.c.decrypt_dir(
            dir_encrypted,
            dir_decrypted,
            overwrite=True,
            enable_verbose=False,
        )
        for p1, p2 in zip(
            dir_original.select_file(recursive=True),
            dir_decrypted.select_file(recursive=True),
        ):
            assert p1.read_bytes() == p2.read_bytes()
