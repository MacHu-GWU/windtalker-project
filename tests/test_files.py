# -*- coding: utf-8 -*-

import pytest
from pathlib_mate import Path
from windtalker import files


def test_get_encrypted_path_get_decrypted_path():
    p_before = Path(__file__)
    p_after = files.get_encrypted_path(p_before)
    assert p_after.abspath.endswith(files.DEFAULT_SUFFIX + ".py")
    assert files.get_decrypted_path(p_after) == p_before

    dir_before = p_before.parent
    dir_after = files.get_encrypted_path(dir_before)
    assert dir_after.abspath.endswith(files.DEFAULT_SUFFIX)
    assert files.get_decrypted_path(dir_after) == dir_before

    files.transform(
        p_before,
        p_after,
        converter=lambda x: x,
        overwrite=True,
        stream=True,
    )
    p_after.remove_if_exists()


def test_process_dst_overwrite_args():
    p_src = Path("test.txt")
    p_src, p_dst = files.process_dst_overwrite_args(
        p_src,
        dst=None,
        overwrite=False,
        src_to_dst_func=files.get_encrypted_path,
    )
    assert p_dst == files.get_encrypted_path(p_src)

    src = "test.txt"
    with pytest.raises(EnvironmentError):
        p_src, p_dst = files.process_dst_overwrite_args(
            src,
            dst=__file__,
            overwrite=False,
            src_to_dst_func=files.get_encrypted_path,
        )


if __name__ == "__main__":
    from windtalker.tests import run_cov_test

    run_cov_test(__file__, "windtalker.files", preview=False)
