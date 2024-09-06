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
import sys
class bstack1l1l1l1l_opy_:
    def __init__(self, handler):
        self._111llll111_opy_ = sys.stdout.write
        self._111lll1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111lll1lll_opy_
        sys.stdout.error = self.bstack111lll1ll1_opy_
    def bstack111lll1lll_opy_(self, _str):
        self._111llll111_opy_(_str)
        if self.handler:
            self.handler({bstack11llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿁"): bstack11llll_opy_ (u"ࠩࡌࡒࡋࡕࠧ࿂"), bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃"): _str})
    def bstack111lll1ll1_opy_(self, _str):
        self._111lll1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿄"): bstack11llll_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿅"), bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫࿆ࠧ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111llll111_opy_
        sys.stderr.write = self._111lll1l1l_opy_