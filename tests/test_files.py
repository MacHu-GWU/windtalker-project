#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

import os
from windtalker import files
from pathlib_mate import Path


def test_get_encrpyted_path_get_decrpyted_path():
    before_file = __file__
    after_file = files.get_encrpyted_path(before_file)
    assert after_file.endswith(files.DEFAULT_SURFIX + ".py")
    assert files.get_decrpyted_path(after_file) == before_file

    before_dir = Path(__file__).parent.abspath
    after_dir = files.get_encrpyted_path(before_dir)
    assert after_dir.endswith(files.DEFAULT_SURFIX)
    assert files.get_decrpyted_path(after_dir) == before_dir

    files.transform(__file__, after_file,
                    converter=lambda x: x, overwrite=True, stream=True)
    try:
        os.remove(after_file)
    except:
        pass


def test_process_dst_overwrite_args():
    src = "test.txt"
    src, dst = files.process_dst_overwrite_args(
        src, dst=None, overwrite=False,
        src_to_dst_func=files.get_encrpyted_path,
    )
    assert dst == files.get_encrpyted_path(src)

    src = "test.txt"
    with raises(EnvironmentError):
        src, dst = files.process_dst_overwrite_args(
            src, dst=__file__, overwrite=False,
            src_to_dst_func=files.get_encrpyted_path,
        )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
