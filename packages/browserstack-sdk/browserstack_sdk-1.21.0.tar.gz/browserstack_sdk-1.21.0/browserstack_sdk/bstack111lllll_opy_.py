# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack11l1lll_opy_ = 2048
bstack1ll1ll1_opy_ = 7
def bstack11llll_opy_ (bstack1111_opy_):
    global bstack11l1ll1_opy_
    bstack11l11l_opy_ = ord (bstack1111_opy_ [-1])
    bstack1l1l11l_opy_ = bstack1111_opy_ [:-1]
    bstack111l111_opy_ = bstack11l11l_opy_ % len (bstack1l1l11l_opy_)
    bstack1ll1111_opy_ = bstack1l1l11l_opy_ [:bstack111l111_opy_] + bstack1l1l11l_opy_ [bstack111l111_opy_:]
    if bstack11l1l1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1lll_opy_ - (bstack1lll111_opy_ + bstack11l11l_opy_) % bstack1ll1ll1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1ll1111_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11l1lll_opy_ - (bstack1lll111_opy_ + bstack11l11l_opy_) % bstack1ll1ll1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1ll1111_opy_)])
    return eval (bstack1l11l1l_opy_)
import threading
class bstack11l11111_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack11l11111_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret