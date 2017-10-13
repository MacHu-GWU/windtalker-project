#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

import os
from windtalker import files
from pathlib_mate import Path


def test_files():
    before_file = __file__
    after_file = files.get_encrpyted_path(before_file)
    assert after_file.endswith(files.default_surfix + ".py")
    assert files.recover_path(after_file) == before_file

    before_dir = Path(__file__).parent.abspath
    after_dir = files.get_encrpyted_path(before_dir)
    assert after_dir.endswith(files.default_surfix)
    assert files.recover_path(after_dir) == before_dir

    files.transform(__file__, after_file,
                    converter=lambda x: x, overwrite=True, stream=True)
    try:
        os.remove(after_file)
    except:
        pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
