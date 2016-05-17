#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
2016年还在由活跃的社区维护的rsa扩展有 ``cryptography`` 和 ``rsa``。 cryp集合了非常
多主流的加密算法, 并且都做了非常多的安全和性能优化(C语言实现)。而rsa是纯Python
实现, 安装非常方便, 使用起来也较为简单。所以本模块最后决定使用rsa进行开发。
"""

from __future__ import print_function, unicode_literals

import os
from os.path import join

import rsa
from rsa.bigfile import *

from windtalker.cipher import BaseCipher
from windtalker.exc import PasswordError
from windtalker import hashes
from windtalker import files
from windtalker import py23


class AsymmetricCipher(BaseCipher):
    """A asymmtric encryption algorithm utility class helps you easily 
    encrypt/decrypt text and files.

    :param my_pubkey: your public key
    :param my_privkey: your private key
    :param his_pubkey: other's public key you use to encrypt message
    """
    # key length/max length msg, 512/53, 1024/117, 2045/245
    _encrypt_chunk_size = 53
    _decrypt_chunk_size = 53

    def __init__(self, my_pubkey, my_privkey, his_pubkey):
        self.my_pubkey = my_pubkey
        self.my_privkey = my_privkey
        self.his_pubkey = his_pubkey

    @staticmethod
    def newkeys(nbits=1024):
        """Create a new pair of public and private key pair to use.
        """
        pubkey, privkey = rsa.newkeys(nbits, poolsize=1)
        return pubkey, privkey

    def encrypt(self, content, use_sign=True):
        """Encrypt

        **中文文档**

        - 发送消息时只需要对方的pubkey
        - 如需使用签名, 则双方都需要持有对方的pubkey 
        """
        token = rsa.encrypt(content, self.his_pubkey)  # encrypt it
        if use_sign:
            self.sign = rsa.sign(content, self.my_privkey, "SHA-1")  # sign it
        return token

    def decrypt(self, token, signature=None):
        """

        **中文文档**

        - 接收消息时只需要自己的privkey
        - 如需使用签名, 则双方都需要持有对方的pubkey
        """
        content = rsa.decrypt(token, self.my_privkey)
        if signature:
            rsa.verify(content, signature, self.his_pubkey)
        return content

    def encrypt_file(self, path, output_path=None,
                     overwrite=False,
                     enable_verbose=True):
        """RSA for big file encryption is very slow. For big file, use 
        symmetric encryption and use RSA to encrypt the password please.
        """
        path = os.path.abspath(path)

        if not output_path:
            output_path = files.get_encrypted_file_path(path)

        if not overwrite:
            if os.path.exists(output_path):
                raise FileExistsError(
                    "output path '%s' already exists.." % output_path)

        with open(path, "rb") as infile, open(output_path, "wb") as outfile:
            encrypt_bigfile(infile, outfile, self.his_pubkey)

    def decrypt_file(self, path, output_path=None,
                     overwrite=False,
                     enable_verbose=True):
        """
        """
        path = os.path.abspath(path)

        if not output_path:
            output_path = files.recover_path(path)

        if not overwrite:
            if os.path.exists(output_path):
                raise FileExistsError(
                    "output path '%s' already exists.." % output_path)

        with open(path, "rb") as infile, open(output_path, "wb") as outfile:
            decrypt_bigfile(infile, outfile, self.my_privkey)