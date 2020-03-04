#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from pathlib_mate import Path

DEFAULT_SURFIX = "-encrypted"  # windtalker secret file or folder surfix


def get_encrpyted_path(original_path, surfix=DEFAULT_SURFIX):
    """
    Find the output encrypted file /dir path (by adding a surfix).

    Example:

    - file: ``${home}/test.txt`` -> ``${home}/test-encrypted.txt``
    - dir: ``${home}/Documents`` -> ``${home}/Documents-encrypted``

    :type original_path: str
    :type surfix: str

    :rtype: str
    """
    p = Path(original_path).absolute()
    encrypted_p = p.change(new_fname=p.fname + surfix)
    return encrypted_p.abspath


def get_decrpyted_path(encrypted_path, surfix=DEFAULT_SURFIX):
    """
    Find the original path of encrypted file or dir.

    Example:

    - file: ``${home}/test-encrypted.txt`` -> ``${home}/test.txt``
    - dir: ``${home}/Documents-encrypted`` -> ``${home}/Documents``

    :type encrypted_path: str
    :type surfix: str

    :rtype: str
    """
    surfix_reversed = surfix[::-1]

    p = Path(encrypted_path).absolute()
    fname = p.fname
    fname_reversed = fname[::-1]
    new_fname = fname_reversed.replace(surfix_reversed, "", 1)[::-1]
    decrypted_p = p.change(new_fname=new_fname)
    return decrypted_p.abspath


def transform(src,
              dst,
              converter,
              overwrite=False,
              stream=True,
              chunksize=1024 ** 2,
              **kwargs):
    """
    A file stream transform IO utility function.

    :type src: str
    :param src: original file path

    :type dst: str
    :param dst: destination file path

    :type converter: typing.Callable
    :param converter: binary content converter function

    :type overwrite: bool
    :param overwrite: default False,

    :type stream: bool
    :param stream: default True, if True, use stream IO mode, chunksize has to
      be specified.

    :type chunksize: int
    :param chunksize: default 1MB
    """
    if not overwrite:  # pragma: no cover
        if Path(dst).exists():
            raise EnvironmentError("'%s' already exists!" % dst)

    with open(src, "rb") as f_input:
        with open(dst, "wb") as f_output:
            if stream:
                # fix chunksize to a reasonable range
                if chunksize > 1024 ** 2 * 10:
                    chunksize = 1024 ** 2 * 10
                elif chunksize < 1024 ** 2:
                    chunksize = 1024 ** 2

                # write file
                while 1:
                    content = f_input.read(chunksize)
                    if content:
                        f_output.write(converter(content, **kwargs))
                    else:
                        break
            else:  # pragma: no cover
                f_output.write(converter(f_input.read(), **kwargs))


def process_dst_overwrite_args(src,
                               dst=None,
                               overwrite=True,
                               src_to_dst_func=None):
    """
    Check when overwrite is not allowed, whether the destination exists.
    """
    src = os.path.abspath(src)

    if dst is None:
        dst = src_to_dst_func(src)

    if not overwrite:
        if os.path.exists(dst):
            raise EnvironmentError(
                "output path '%s' already exists.." % dst)

    return src, dst
