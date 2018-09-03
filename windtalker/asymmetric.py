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
from windtalker import fingerprint
from windtalker import files
from windtalker import py23


class AsymmetricCipher(BaseCipher):
    """
    A asymmetric encryption algorithm utility class helps you easily
    encrypt/decrypt text and files.

    :param my_pubkey: your public key
    :param my_privkey: your private key
    :param his_pubkey: other's public key you use to encrypt message

    **中文文档**

    非对称加密器。
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
        """
        Create a new pair of public and private key pair to use.
        """
        pubkey, privkey = rsa.newkeys(nbits, poolsize=1)
        return pubkey, privkey

    def encrypt(self, binary, use_sign=True):
        """
        Encrypt binary data.

        **中文文档**

        - 发送消息时只需要对方的pubkey
        - 如需使用签名, 则双方都需要持有对方的pubkey
        """
        token = rsa.encrypt(binary, self.his_pubkey)  # encrypt it
        if use_sign:
            self.sign = rsa.sign(binary, self.my_privkey, "SHA-1")  # sign it
        return token

    def decrypt(self, token, signature=None):
        """
        Decrypt binary data.

        **中文文档**

        - 接收消息时只需要自己的privkey
        - 如需使用签名, 则双方都需要持有对方的pubkey
        """
        binary = rsa.decrypt(token, self.my_privkey)
        if signature:
            rsa.verify(binary, signature, self.his_pubkey)
        return binary

    def encrypt_file(self,
                     path,
                     output_path=None,
                     overwrite=False,
                     enable_verbose=True):
        """
        Encrypt a file using rsa.

        RSA for big file encryption is very slow. For big file, I recommend
        to use symmetric encryption and use RSA to encrypt the password.
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_encrpyted_path,
        )

        with open(path, "rb") as infile, open(output_path, "wb") as outfile:
            encrypt_bigfile(infile, outfile, self.his_pubkey)

    def decrypt_file(self,
                     path,
                     output_path=None,
                     overwrite=False,
                     enable_verbose=True):
        """
        Decrypt a file using rsa.
        """
        path, output_path = files.process_dst_overwrite_args(
            src=path, dst=output_path, overwrite=overwrite,
            src_to_dst_func=files.get_decrpyted_path,
        )

        with open(path, "rb") as infile, open(output_path, "wb") as outfile:
            decrypt_bigfile(infile, outfile, self.my_privkey)
