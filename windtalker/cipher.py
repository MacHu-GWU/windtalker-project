# -*- coding: utf-8 -*-

import typing as T
import os
import time
import base64

from pathlib_mate import Path, T_PATH_ARG

from . import files


class BaseCipher:
    """
    Base cipher class.

    Any cipher utility class that using any encryption algorithm can be
    inherited from this base class. The only method you need to implement is
    :meth:`BaseCipher.encrypt` and :meth:`BaseCipher.decrypt`. Because once you
    can encrypt binary data, then you can encrypt text, file, and directory.
    """

    _encrypt_chunk_size = 1024
    _decrypt_chunk_size = 1024

    def b64encode_str(self, text: str) -> str:
        """
        base64 encode a text, return string also.
        """
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def b64decode_str(self, text: str) -> str:
        """
        base64 decode a text, return string also.
        """
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")

    def encrypt(self, binary: bytes, *args, **kwargs) -> bytes:
        """
        Overwrite this method using your encrypt algorithm.

        :param binary: binary data you need to encrypt

        :return: encrypted_binary, encrypted binary data
        """
        raise NotImplementedError

    def decrypt(self, binary: bytes, *args, **kwargs) -> bytes:
        """
        Overwrite this method using your decrypt algorithm.

        :param binary: binary data you need to decrypt

        :return: decrypted_binary, decrypted binary data
        """
        raise NotImplementedError

    def encrypt_binary(self, binary: bytes, *args, **kwargs) -> bytes:
        """ """
        return self.encrypt(binary, *args, **kwargs)

    def decrypt_binary(self, binary: bytes, *args, **kwargs) -> bytes:
        """ """
        return self.decrypt(binary, *args, **kwargs)

    def encrypt_text(self, text: str, *args, **kwargs) -> str:
        """
        Encrypt a string.
        """
        b = text.encode("utf-8")
        token = self.encrypt(b, *args, **kwargs)
        return base64.b64encode(token).decode("utf-8")

    def decrypt_text(self, text: str, *args, **kwargs) -> str:
        """
        Decrypt a string.
        """
        b = text.encode("utf-8")
        token = base64.b64decode(b)
        return self.decrypt(token, *args, **kwargs).decode("utf-8")

    def _show(
        self,
        message: str,
        indent: int = 0,
        enable_verbose: bool = True,
    ):  # pragma: no cover
        """Message printer."""
        if enable_verbose:
            print("    " * indent + message)

    def encrypt_file(
        self,
        path: T_PATH_ARG,
        output_path: T.Optional[T_PATH_ARG] = None,
        overwrite: bool = False,
        stream: bool = True,
        enable_verbose: bool = True,
        **kwargs,
    ):
        """
        Encrypt a file. If output_path are not given, then try to use the
        path with a surfix appended. The default automatical file path handling
        is defined here :meth:`windtalker.files.get_encrypted_file_path`

        :param path: path of the file you need to encrypt
        :param output_path: encrypted file output path
        :param overwrite: if True, then silently overwrite output file if exists
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory
        :param enable_verbose: trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path,
            dst=output_path,
            overwrite=overwrite,
            src_to_dst_func=files.get_encrypted_path,
        )

        self._show("Encrypt '%s' ..." % path, enable_verbose=enable_verbose)
        st = time.process_time()
        files.transform(
            path,
            output_path,
            converter=self.encrypt,
            overwrite=overwrite,
            stream=stream,
            chunksize=self._encrypt_chunk_size,
        )
        self._show(
            "    Finished! Elapse %.6f seconds" % (time.process_time() - st,),
            enable_verbose=enable_verbose,
        )

        return output_path

    def decrypt_file(
        self,
        path: T_PATH_ARG,
        output_path: T_PATH_ARG = None,
        overwrite: bool = False,
        stream: bool = True,
        enable_verbose: bool = True,
        **kwargs,
    ):
        """
        Decrypt a file. If output_path are not given, then try to use the
        path with a surfix appended. The default automatical file path handling
        is defined here :meth:`windtalker.files.recover_path`

        :param path: path of the file you need to decrypt
        :param output_path: decrypted file output path
        :param overwrite: if True, then silently overwrite output file if exists
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path,
            dst=output_path,
            overwrite=overwrite,
            src_to_dst_func=files.get_decrypted_path,
        )

        self._show("Decrypt '%s' ..." % path, enable_verbose=enable_verbose)
        st = time.process_time()
        files.transform(
            path,
            output_path,
            converter=self.decrypt,
            overwrite=overwrite,
            stream=stream,
            chunksize=self._decrypt_chunk_size,
        )
        self._show(
            "    Finished! Elapse %.6f seconds" % (time.process_time() - st,),
            enable_verbose=enable_verbose,
        )

        return output_path

    def encrypt_dir(
        self,
        path: T_PATH_ARG,
        output_path: T.Optional[T_PATH_ARG] = None,
        overwrite: bool = False,
        stream: bool = True,
        enable_verbose: bool = True,
    ):
        """
        Encrypt everything in a directory.

        :param path: path of the dir you need to encrypt
        :param output_path: encrypted dir output path
        :param overwrite: if True, then silently overwrite output file if exists
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path,
            dst=output_path,
            overwrite=overwrite,
            src_to_dst_func=files.get_encrypted_path,
        )

        self._show(
            "--- Encrypt directory '%s' ---" % path, enable_verbose=enable_verbose
        )
        st = time.process_time()
        for current_dir, _, file_list in os.walk(path.abspath):
            new_dir = output_path.joinpath(Path(current_dir).relative_to(path))
            new_dir.mkdir_if_not_exists()
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = new_dir.joinpath(basename)
                self.encrypt_file(
                    old_path,
                    new_path,
                    overwrite=overwrite,
                    stream=stream,
                    enable_verbose=enable_verbose,
                )
        self._show(
            "Complete! Elapse %.6f seconds" % (time.process_time() - st,),
            enable_verbose=enable_verbose,
        )
        return output_path

    def decrypt_dir(
        self,
        path: T_PATH_ARG,
        output_path: T.Optional[T_PATH_ARG] = None,
        overwrite: bool = False,
        stream: bool = True,
        enable_verbose: bool = True,
    ):
        """
        Decrypt everything in a directory.

        :param path: path of the dir you need to decrypt
        :param output_path: decrypted dir output path
        :param overwrite: if True, then silently overwrite output file if exists
        :param stream: if it is a very big file, stream mode can avoid using
          too much memory
        :param enable_verbose: boolean, trigger on/off the help information
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path,
            dst=output_path,
            overwrite=overwrite,
            src_to_dst_func=files.get_decrypted_path,
        )

        self._show(
            "--- Decrypt directory '%s' ---" % path, enable_verbose=enable_verbose
        )
        st = time.process_time()
        for current_dir, _, file_list in os.walk(path):
            new_dir = output_path.joinpath(Path(current_dir).relative_to(path))
            new_dir.mkdir_if_not_exists()
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = new_dir.joinpath(basename)
                self.decrypt_file(
                    old_path,
                    new_path,
                    overwrite=overwrite,
                    stream=stream,
                    enable_verbose=enable_verbose,
                )
        self._show(
            "Complete! Elapse %.6f seconds" % (time.process_time() - st,),
            enable_verbose=enable_verbose,
        )

        return output_path
