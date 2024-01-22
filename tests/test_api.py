# -*- coding: utf-8 -*-

from windtalker import api


def test():
    _ = api
    _ = api.BaseCipher
    _ = api.AsymmetricCipher
    _ = api.SymmetricCipher


if __name__ == "__main__":
    from windtalker.tests import run_cov_test

    run_cov_test(__file__, "windtalker.api", preview=False)
