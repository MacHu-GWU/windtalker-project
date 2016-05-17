#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


default_surfix = "-encrypted"  # windtalker secret


def get_encrypted_file_path(original_path, surfix=default_surfix):
    """Find the output encrypted file path(by adding a surfix).

    Example: ``test.txt -> test-wtscrt.txt``
    """
    abspath = os.path.abspath(original_path)
    fname, ext = os.path.splitext(abspath)
    fname = fname + surfix
    return fname + ext


def get_encrypted_dir_path(original_path, surfix=default_surfix):
    """Find the output encrypted dir path(by adding a surfix).

    Example: ``test -> test-wtscrt``
    """
    abspath = os.path.abspath(original_path)
    return abspath + surfix


def recover_path(encrypted_path, surfix=default_surfix):
    """Find the original path of encrypted file or dir.

    Example: ``test-wtscrt.txt -> test.txt``
    """
    return encrypted_path.replace(surfix, "")


def transform(src, dst, converter,
              overwrite=False, stream=True, chunksize=1024**2, **kwargs):
    """A file stream transform IO utility function.

    :param src: original file path
    :param dst: destination file path
    :param converter: binary content converter function
    :param overwrite: default False,
    :param stream: default True, if True, use stream IO mode, chunksize has to
      be specified.
    :param chunksize: default 1MB
    """
    if not overwrite:
        if os.path.exists(dst):
            raise FileExistsError("'%s' already exists!" % dst)

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
            else:
                f_output.write(converter(f_input.read(), **kwargs))


#--- Unittest ---
if __name__ == "__main__":
    org = __file__
    dst = get_encrypted_file_path(org)
    print(recover_path(dst))

    org = os.getcwd()
    dst = get_encrypted_dir_path(org)
    print(recover_path(dst))

    src = "__init__.py"
    dst = "__init__-Backup.py"

    def converter(content):
        return content

    transform(src, dst, converter, overwrite=True, stream=False)