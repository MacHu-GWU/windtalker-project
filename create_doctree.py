#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import os

try:
    os.remove(r"source\windtalker")
except Exception as e:
    print(e)

docfly = Docfly(
    "windtalker", 
    dst="source", 
    ignore=[
        "windtalker.zzz_manual_install.py",
    ],
)
docfly.fly()