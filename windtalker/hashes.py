#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
hash utility module.
"""

from __future__ import print_function

import os
import pickle
import hashlib

from windtalker import py23


class WrongHashAlgorithmError(Exception):
    pass


class FingerPrint(object):
    """A hashlib wrapper class allow you to use one line to do hash as you wish.

    Usage::

        >>> from weatherlab.lib.hashes.fingerprint import fingerprint
        >>> print(fingerprint.of_bytes(bytes(123)))
        b1fec41621e338896e2d26f232a6b006

        >>> print(fingerprint.of_text("message"))
        78e731027d8fd50ed642340b7c9a63b3

        >>> print(fingerprint.of_pyobj({"key": "value"}))
        4c502ab399c89c8758a2d8c37be98f69

        >>> print(fingerprint.of_file("fingerprint.py"))
        4cddcb5562cbff652b0e4c8a0300337a
    """
    _chunk_size = 2**20

    def __init__(self):
        self.default_hash_method = hashlib.md5
        self.return_int = False

    def digest_to_int(self, digest):
        """Convert hexdigest str to int.
        """
        return int(digest, 16)

    def use(self, algorithm):
        """Change the hash algorithm you gonna use.
        """
        algorithm = algorithm.lower()
        if algorithm == "md5":
            self.default_hash_method = hashlib.md5
        elif algorithm == "sha1":
            self.default_hash_method = hashlib.sha1
        elif algorithm == "sha224":
            self.default_hash_method = hashlib.sha224
        elif algorithm == "sha256":
            self.default_hash_method = hashlib.sha256
        elif algorithm == "sha384":
            self.default_hash_method = hashlib.sha384
        elif algorithm == "sha512":
            self.default_hash_method = hashlib.sha512
        else:
            raise WrongHashAlgorithmError("There's no algorithm names '%s'! "
                                          "use one of 'md5', 'sha1', 'sha224', "
                                          "'sha256', 'sha384', 'sha512'." % algorithm)

    def set_return_int(self, flag):
        """If flag = False, return hex string, if True, return integer.
        default = False.
        """
        self.return_int = bool(flag)

    def of_bytes(self, py_bytes):
        """Use default hash method to return hash value of bytes.
        """
        m = self.default_hash_method()
        m.update(py_bytes)
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_text(self, text, encoding="utf-8"):
        """Use default hash method to return hash value of a piece of string
        default setting use 'utf-8' encoding.
        """
        m = self.default_hash_method()
        m.update(text.encode(encoding))
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_pyobj(self, pyobj):
        """Use default hash method to return hash value of a piece of Python
        picklable object.
        """
        m = self.default_hash_method()
        m.update(pickle.dumps(pyobj, protocol=py23.pk_protocol))
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_file(self, abspath, nbytes=0):
        """Use default hash method to return hash value of a piece of a file

        Estimate processing time on:

        :param abspath: the absolute path to the file
        :param nbytes: only has first N bytes of the file. if 0, hash all file

        CPU = i7-4600U 2.10GHz - 2.70GHz, RAM = 8.00 GB
        1 second can process 0.25GB data

        - 0.59G - 2.43 sec
        - 1.3G - 5.68 sec
        - 1.9G - 7.72 sec
        - 2.5G - 10.32 sec
        - 3.9G - 16.0 sec

        ATTENTION:
            if you change the meta data (for example, the title, years
            information in audio, video) of a multi-media file, then the hash
            value gonna also change.
        """
        if not os.path.exists(abspath):
            raise FileNotFoundError(
                "[Errno 2] No such file or directory: '%s'" % abspath)

        m = self.default_hash_method()
        with open(abspath, "rb") as f:
            if nbytes:
                data = f.read(nbytes)
                if data:
                    m.update(data)
            else:
                while True:
                    data = f.read(self._chunk_size)
                    if not data:
                        break
                    m.update(data)
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

fingerprint = FingerPrint()


#--- Unittest ---
if __name__ == "__main__":
    import unittest

    class FingerPrintUnittest(unittest.TestCase):
        def test_hash_anything(self):
            for algorithm in ["md5", "sha1", "sha224",
                              "sha256", "sha384", "sha512"]:
                print("\n===%s hash value===" % algorithm)
                fingerprint.use(algorithm)
                print(fingerprint.of_bytes(bytes(123)))
                print(fingerprint.of_text("message"))
                print(fingerprint.of_pyobj({"key": "value"}))
                print(fingerprint.of_file("hashes.py"))

            fingerprint.set_return_int(True)
            for algorithm in ["md5", "sha1", "sha224",
                              "sha256", "sha384", "sha512"]:
                print("\n===%s hash value===" % algorithm)
                fingerprint.use(algorithm)
                print(fingerprint.of_bytes(bytes(123)))
                print(fingerprint.of_text("message"))
                print(fingerprint.of_pyobj({"key": "value"}))
                print(fingerprint.of_file("hashes.py"))

    unittest.main()