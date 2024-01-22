# -*- coding: utf-8 -*-

"""
File handling utility functions.
"""

import typing as T
from pathlib_mate import Path, T_PATH_ARG

DEFAULT_SUFFIX = "-encrypted"  # windtalker secret file or folder suffix


def get_encrypted_path(
    original_path: T_PATH_ARG,
    suffix: str = DEFAULT_SUFFIX,
) -> Path:
    """
    Find the output encrypted file /dir path (by adding a suffix).

    Example:

    - file: ``${home}/test.txt`` -> ``${home}/test-encrypted.txt``
    - dir: ``${home}/Documents`` -> ``${home}/Documents-encrypted``
    """
    p = Path(original_path).absolute()
    return p.change(new_fname=p.fname + suffix)


def get_decrypted_path(
    encrypted_path: T_PATH_ARG,
    suffix: str = DEFAULT_SUFFIX,
) -> Path:
    """
    Find the original path of encrypted file or dir.

    Example:

    - file: ``${home}/test-encrypted.txt`` -> ``${home}/test.txt``
    - dir: ``${home}/Documents-encrypted`` -> ``${home}/Documents``
    """
    p = Path(encrypted_path).absolute()
    if not p.fname.endswith(suffix):
        raise ValueError(
            f"'{p}' is not a encrypted file or dir path "
            f"(filename not ends with suffix {suffix}."
        )
    return p.change(new_fname=p.fname[: -len(suffix)])


def transform(
    src: T_PATH_ARG,
    dst: T_PATH_ARG,
    converter: T.Callable,
    overwrite: bool = False,
    stream: bool = True,
    chunksize: int = 1024**2,
    **kwargs,
):
    """
    A file stream transform IO utility function.

    :param src: original file path
    :param dst: destination file path
    :param converter: binary content converter function
    :param overwrite: default False,
    :param stream: default True, if True, use stream IO mode, chunksize has to
      be specified.
    :param chunksize: default 1MB
    """
    p_src = Path(src).absolute()
    p_dst = Path(dst).absolute()
    if not overwrite:  # pragma: no cover
        if p_dst.exists():
            raise EnvironmentError(f"'{p_dst}' already exists!")

    with p_src.open("rb") as f_input:
        with p_dst.open("wb") as f_output:
            if stream:
                # fix chunksize to a reasonable range
                if chunksize > 1024**2 * 10:
                    chunksize = 1024**2 * 10
                elif chunksize < 1024**2:
                    chunksize = 1024**2

                # write file
                while 1:
                    content = f_input.read(chunksize)
                    if content:
                        f_output.write(converter(content, **kwargs))
                    else:
                        break
            else:  # pragma: no cover
                f_output.write(converter(f_input.read(), **kwargs))


def process_dst_overwrite_args(
    src: T_PATH_ARG,
    dst: T.Optional[T_PATH_ARG] = None,
    overwrite: bool = True,
    src_to_dst_func: T.Optional[T.Callable] = None,
) -> T.Tuple[Path, Path]:
    """
    Check when overwrite is not allowed, whether the destination exists.
    """
    p_src = Path(src).absolute()

    if dst is None:
        p_dst = src_to_dst_func(p_src)
    else:
        p_dst = Path(dst).absolute()

    if not overwrite:
        if p_dst.exists():
            raise EnvironmentError(f"output path '{p_dst}' already exists..")

    return p_src, p_dst
