#!/usr/bin/python
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from eudplib import core as c

from ..utilf import EUDBinaryMax


@c.EUDFunc
def f_sqrt(n):
    return EUDBinaryMax(lambda x: x * x <= n, 0, 0xFFFF)
