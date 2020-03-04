#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import base64
import os
import time

from . import files

try:
    import typing
except:
    pass


class BaseCipher(object):
    """
    Base cipher class.

    Any cipher utility class that using any encryption algorithm can be
    inherited from this base class. The only method you need to implement is
    :meth:`BaseCipher.encrypt` and :meth:`BaseCipher.decrypt`. Because once you
    can encrypt binary data, then you can encrypt text, file, and directory.
    """
    _encrypt_chunk_size = 1024
    _decrypt_chunk_size = 1024

    def b64encode_str(self, text):
        """
        base64 encode a text, return string also.

        :type text: str

        :rtype: str
        """
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def b64decode_str(self, text):
        """
        base64 decode a text, return string also.

        :type text: str

        :rtype: str
        """
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")

    def encrypt(self, binary, *args, **kwargs):
        """
        Overwrite this method using your encrypt algorithm.

        :type binary: bytes
        :param binary: binary data you need to encrypt

        :rtype: bytes
        :return: encrypted_binary, encrypted binary data
        """
        raise NotImplementedError

    def decrypt(self, binary, *args, **kwargs):
        """
        Overwrite this method using your decrypt algorithm.

        :type binary: bytes
        :param binary: binary data you need to decrypt

        :rtype: bytes
        :return: decrypted_binary, decrypted binary data
        """
        raise NotImplementedError

    def encrypt_binary(self, binary, *args, **kwargs):
        """
        :type binary: bytes
        :rtype: bytes
        """
        return self.encrypt(binary, *args, **kwargs)

    def decrypt_binary(self, binary, *args, **kwargs):
        """
        :type binary: bytes
        :rtype: bytes
        """
        return self.decrypt(binary, *args, **kwargs)

    def encrypt_text(self, text, *args, **kwargs):
        """
        Encrypt a string.

        :type text: str
        :rtype: str
        """
        b = text.encode("utf-8")
        token = self.encrypt(b, *args, **kwargs)
        return base64.b64encode(token).decode("utf-8")

    def decrypt_text(self, text, *args, **kwargs):
        """
        Decrypt a string.

        :type text: str
        :rtype: str
        """
        b = text.encode("utf-8")
        token = base64.b64decode(b)
        return self.decrypt(token, *args, **kwargs).decode("utf-8")

    def _show(self, message, indent=0, enable_verbose=True):  # pragma: no cover
        """Message printer.
        """
        if enable_verbose:
            print("    " * indent + message)

    def encrypt_file(self,
                     path,
                     output_path=None,
                     overwrite=False,
                     stream=True,
                     enable_verbose=True,
                     **kwargs):
        """
        Encrypt a file. If output_path are not given, then try to use the
        path with a surfix appended. The default automatical file path handling
        is defined here :meth:`windtalker.files.get_encrypted_file_path`

        :type path: str
        :param path: path of the file you need to encrypt

        :type output_path: str
        :param output_path: encrypted file output path

        :type overwrite: bool
        :param overwrite: if True, then silently overwrite output file if exists

        :type stream: bool
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory

        :type enable_verbose: bool
        :param enable_verbose: trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_encrpyted_path,
        )

        self._show("Encrypt '%s' ..." % path, enable_verbose=enable_verbose)
        st = time.clock()
        files.transform(path, output_path, converter=self.encrypt,
                        overwrite=overwrite, stream=stream,
                        chunksize=self._encrypt_chunk_size)
        self._show("    Finished! Elapse %.6f seconds" % (time.clock() - st,),
                   enable_verbose=enable_verbose)

        return output_path

    def decrypt_file(self,
                     path,
                     output_path=None,
                     overwrite=False,
                     stream=True,
                     enable_verbose=True,
                     **kwargs):
        """
        Decrypt a file. If output_path are not given, then try to use the
        path with a surfix appended. The default automatical file path handling
        is defined here :meth:`windtalker.files.recover_path`

        :type path: str
        :param path: path of the file you need to decrypt

        :type output_path: str
        :param output_path: decrypted file output path

        :type overwrite: bool
        :param overwrite: if True, then silently overwrite output file if exists

        :type stream: bool
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory

        :type enable_verbose: bool
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_decrpyted_path,
        )

        self._show("Decrypt '%s' ..." % path, enable_verbose=enable_verbose)
        st = time.clock()
        files.transform(path, output_path, converter=self.decrypt,
                        overwrite=overwrite, stream=stream,
                        chunksize=self._decrypt_chunk_size)
        self._show("    Finished! Elapse %.6f seconds" % (time.clock() - st,),
                   enable_verbose=enable_verbose)

        return output_path

    def encrypt_dir(self,
                    path,
                    output_path=None,
                    overwrite=False,
                    stream=True,
                    enable_verbose=True):
        """
        Encrypt everything in a directory.

        :type path: str
        :param path: path of the dir you need to encrypt

        :type output_path: str
        :param output_path: encrypted dir output path

        :type overwrite: bool
        :param overwrite: if True, then silently overwrite output file if exists

        :type stream: bool
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory

        :type enable_verbose: bool
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_encrpyted_path,
        )

        self._show("--- Encrypt directory '%s' ---" % path,
                   enable_verbose=enable_verbose)
        st = time.clock()
        for current_dir, _, file_list in os.walk(path):
            new_dir = current_dir.replace(path, output_path)
            if not os.path.exists(new_dir):  # pragma: no cover
                os.mkdir(new_dir)
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = os.path.join(new_dir, basename)
                self.encrypt_file(old_path, new_path,
                                  overwrite=overwrite,
                                  stream=stream,
                                  enable_verbose=enable_verbose)
        self._show("Complete! Elapse %.6f seconds" % (time.clock() - st,),
                   enable_verbose=enable_verbose)
        return output_path

    def decrypt_dir(self,
                    path,
                    output_path=None,
                    overwrite=False,
                    stream=True,
                    enable_verbose=True):
        """
        Decrypt everything in a directory.

        :type path: str
        :param path: path of the dir you need to decrypt

        :type output_path: str
        :param output_path: decrypted dir output path

        :type overwrite: bool
        :param overwrite: if True, then silently overwrite output file if exists

        :type stream: bool
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory

        :type enable_verbose: bool
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_decrpyted_path,
        )

        self._show("--- Decrypt directory '%s' ---" % path,
                   enable_verbose=enable_verbose)
        st = time.clock()
        for current_dir, _, file_list in os.walk(path):
            new_dir = current_dir.replace(path, output_path)
            if not os.path.exists(new_dir):  # pragma: no cover
                os.mkdir(new_dir)
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = os.path.join(new_dir, basename)
                self.decrypt_file(old_path, new_path,
                                  overwrite=overwrite,
                                  stream=stream,
                                  enable_verbose=enable_verbose)
        self._show("Complete! Elapse %.6f seconds" % (time.clock() - st,),
                   enable_verbose=enable_verbose)

        return output_path
