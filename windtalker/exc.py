#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PasswordError(Exception):
    """symmetric encrypt wrong password error.
    """


class SignatureError(Exception):
    """asymmetric encrypt wrong signature error.
    """
