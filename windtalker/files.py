#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib_mate import Path


default_surfix = "-encrypted"  # windtalker secret


def get_encrpyted_path(original_path, surfix=default_surfix):
    r"""
    Find the output encrypted file /dir path (by adding a surfix).

    Example:

    - ``C:\test.txt`` -> ``C:\test-encrypted.txt``
    - ``C:\Users\admin\Documents`` -> ``C:\Users\admin\Documents-encrypted``
    """
    p = Path(original_path).absolute()
    encrypted_p = p.change(new_fname=p.fname + surfix)
    return encrypted_p.abspath


def recover_path(encrypted_path, surfix=default_surfix):
    r"""
    Find the original path of encrypted file or dir.

    Example:

    - ``C:\test-encrypted.txt`` -> ``C:\test.txt``
    - ``C:\Users\admin\Documents-encrypted`` -> ``C:\Users\admin\Documents``
    """
    surfix_reversed = surfix[::-1]

    p = Path(encrypted_path).absolute()
    fname = p.fname
    fname_reversed = fname[::-1]
    new_fname = fname_reversed.replace(surfix_reversed, "", 1)[::-1]
    decrypted_p = p.change(new_fname=new_fname)
    return decrypted_p.abspath


def transform(src, dst, converter,
              overwrite=False, stream=True, chunksize=1024**2, **kwargs):
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
