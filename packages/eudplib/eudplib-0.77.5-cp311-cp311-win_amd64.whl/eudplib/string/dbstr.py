#!/usr/bin/python
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from typing_extensions import Self

from eudplib import core as c
from eudplib import utils as ut


class DBString(ut.ExprProxy):
    """Object for storing single modifiable string.

    Manipulating STR section is hard. DBString stores only one string, so that
    modifying its structure is substantially easier than modifying entire STR
    section. You can do anything you would do with normal string with DBString.
    """

    def __init__(self, content=None, *, _from=None) -> None:
        """Constructor for DBString

        :param content: Initial DBString content / capacity. Capacity of
            DBString is determined by size of this. If content is integer, then
            initial capacity and content of DBString will be set to
            content(int) and empty string.

        :type content: str, bytes, int
        """
        if _from is None:
            super().__init__(DBStringData(content))
        elif type(_from) in (str, bytes):
            super().__init__(DBStringData(_from))
        else:
            super().__init__(_from)

    def GetStringMemoryAddr(self):  # noqa: N802
        """Get memory address of DBString content.

        :returns: Memory address of DBString content.
        """
        return self + 4

    @c.EUDMethod
    def Display(self):  # noqa: N802
        from .strbuffer import GetGlobalStringBuffer

        gsb = GetGlobalStringBuffer()
        gsb.printf("{:t}", ut.EPD(self) + 1)

    @c.EUDMethod
    def Play(self):  # noqa: N802
        from .strbuffer import GetGlobalStringBuffer

        gsb = GetGlobalStringBuffer()
        gsb.insert(0)
        gsb.appendf("{:t}", ut.EPD(self) + 1)
        gsb.Play()


class DBStringData(c.EUDObject):
    """Object containing DBString data"""

    def __new__(cls, *args, **kwargs) -> Self:
        return super().__new__(cls)

    def __init__(self, content) -> None:
        """Constructor for DBString

        :param content: Initial DBString content / capacity. Capacity of
            DBString is determined by size of this. If content is integer, then
            initial capacity and content of DBString will be set to
            content(int) and empty string.

        :type content: str, bytes, int
        """
        super().__init__()
        if isinstance(content, int):
            self.content = bytes(content)
        else:
            self.content = ut.u2utf8(content)

    def GetDataSize(self):  # noqa: N802
        return len(self.content) + 5

    def WritePayload(self, pbuf):  # noqa: N802
        pbuf.WriteBytes(b"\x01\x00\x04\x00")
        pbuf.WriteBytes(self.content)
        pbuf.WriteByte(0)
