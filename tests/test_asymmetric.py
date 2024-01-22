# -*- coding: utf-8 -*-

from windtalker.asymmetric import AsymmetricCipher


class TestAsymmetricCipher:
    def test_encrypt_decrypt_data(self):
        data = "Turn right at blue tree".encode("utf-8")
        A_pubkey, A_privkey = AsymmetricCipher.new_keys()
        B_pubkey, B_privkey = AsymmetricCipher.new_keys()

        cipherA = AsymmetricCipher(A_pubkey, A_privkey, B_pubkey)
        cipherB = AsymmetricCipher(B_pubkey, B_privkey, A_pubkey)

        token = cipherA.encrypt(data)
        sign = cipherA.sign

        data_new = cipherB.decrypt(token, signature=sign)
        assert data == data_new
        assert data != token


if __name__ == "__main__":
    from windtalker.tests import run_cov_test

    run_cov_test(__file__, "windtalker.asymmetric", preview=False)
