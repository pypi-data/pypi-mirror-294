#!/usr/bin/python
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from eudplib import core as c
from eudplib import ctrlstru as cs
from eudplib import trigger as t
from eudplib import utils as ut

from ..eudarray import EUDArray
from ..memiof import f_dwread_epd, f_repmovsd_epd

_patch_max = 8192

patchstack = EUDArray(3 * _patch_max)
dws_top, ps_top = c.EUDVariable(), c.EUDVariable()
dwstack = EUDArray(_patch_max)


def pushpatchstack(value: c.EUDVariable | int) -> None:
    global ps_top
    patchstack[ps_top] = value
    ps_top += 1


def poppatchstack() -> c.EUDVariable:
    global ps_top
    ps_top -= 1
    return patchstack[ps_top]


@c.EUDFunc
def f_dwpatch_epd(dstepd, value):
    global dws_top

    prev_value = f_dwread_epd(dstepd)
    dws_pos = ut.EPD(dwstack) + dws_top
    c.VProc(
        [dstepd, value, dws_pos, prev_value],
        [
            dstepd.SetDest(ut.EPD(value.getDestAddr())),
            dws_pos.SetDest(ut.EPD(prev_value.getDestAddr())),
        ],
    )

    pushpatchstack(dstepd)
    pushpatchstack(dws_pos)
    pushpatchstack(1)
    dws_top += 1


@c.EUDFunc
def f_blockpatch_epd(dstepd, srcepd, dwn):
    """Patch 4*dwn bytes of memory at dstepd with memory of srcepd.

    .. note::
        After calling this function, contents at srcepd memory may change.
        Since new contents are required for :py:`f_unpatchall` to run, you
        shouldn't use the memory for any other means.
    """

    global dws_top

    # Push to stack
    pushpatchstack(dstepd)
    pushpatchstack(srcepd)
    pushpatchstack(dwn)
    dws_top += 1

    # Swap contents btw dstepd, srcepd
    tmpbuffer = c.Db(1024)

    if cs.EUDWhile()(dwn > 0):
        copydwn = c.EUDVariable()
        copydwn << 256
        t.Trigger(dwn <= 256, copydwn.SetNumber(dwn))
        dwn -= copydwn

        f_repmovsd_epd(ut.EPD(tmpbuffer), dstepd, copydwn)
        f_repmovsd_epd(dstepd, srcepd, copydwn)
        f_repmovsd_epd(srcepd, ut.EPD(tmpbuffer), copydwn)
    cs.EUDEndWhile()


@c.EUDFunc
def f_unpatchall():
    global ps_top, dws_top
    if cs.EUDWhile()(ps_top >= 1):
        dws_top -= 1
        dwn = poppatchstack()
        unpatchsrcepd = poppatchstack()
        dstepd = poppatchstack()
        f_repmovsd_epd(dstepd, unpatchsrcepd, dwn)
    cs.EUDEndWhile()
