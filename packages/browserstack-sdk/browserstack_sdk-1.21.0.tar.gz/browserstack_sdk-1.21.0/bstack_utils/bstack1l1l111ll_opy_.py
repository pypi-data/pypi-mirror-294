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
from collections import deque
from bstack_utils.constants import *
class bstack11lll1l111_opy_:
    def __init__(self):
        self._1lll1l1ll11_opy_ = deque()
        self._1lll1lll111_opy_ = {}
        self._1lll1l1llll_opy_ = False
    def bstack1lll1ll11ll_opy_(self, test_name, bstack1lll1l1l1ll_opy_):
        bstack1lll1ll11l1_opy_ = self._1lll1lll111_opy_.get(test_name, {})
        return bstack1lll1ll11l1_opy_.get(bstack1lll1l1l1ll_opy_, 0)
    def bstack1lll1l1lll1_opy_(self, test_name, bstack1lll1l1l1ll_opy_):
        bstack1lll1l1ll1l_opy_ = self.bstack1lll1ll11ll_opy_(test_name, bstack1lll1l1l1ll_opy_)
        self.bstack1lll1ll111l_opy_(test_name, bstack1lll1l1l1ll_opy_)
        return bstack1lll1l1ll1l_opy_
    def bstack1lll1ll111l_opy_(self, test_name, bstack1lll1l1l1ll_opy_):
        if test_name not in self._1lll1lll111_opy_:
            self._1lll1lll111_opy_[test_name] = {}
        bstack1lll1ll11l1_opy_ = self._1lll1lll111_opy_[test_name]
        bstack1lll1l1ll1l_opy_ = bstack1lll1ll11l1_opy_.get(bstack1lll1l1l1ll_opy_, 0)
        bstack1lll1ll11l1_opy_[bstack1lll1l1l1ll_opy_] = bstack1lll1l1ll1l_opy_ + 1
    def bstack11l11l11l_opy_(self, bstack1lll1ll1l1l_opy_, bstack1lll1ll1lll_opy_):
        bstack1lll1ll1ll1_opy_ = self.bstack1lll1l1lll1_opy_(bstack1lll1ll1l1l_opy_, bstack1lll1ll1lll_opy_)
        bstack1lll1ll1111_opy_ = bstack111lll1111_opy_[bstack1lll1ll1lll_opy_]
        bstack1lll1ll1l11_opy_ = bstack11llll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᕽ").format(bstack1lll1ll1l1l_opy_, bstack1lll1ll1111_opy_, bstack1lll1ll1ll1_opy_)
        self._1lll1l1ll11_opy_.append(bstack1lll1ll1l11_opy_)
    def bstack1l1lll111_opy_(self):
        return len(self._1lll1l1ll11_opy_) == 0
    def bstack1l1111lll1_opy_(self):
        bstack1lll1l1l1l1_opy_ = self._1lll1l1ll11_opy_.popleft()
        return bstack1lll1l1l1l1_opy_
    def capturing(self):
        return self._1lll1l1llll_opy_
    def bstack1ll111l11_opy_(self):
        self._1lll1l1llll_opy_ = True
    def bstack1ll111111l_opy_(self):
        self._1lll1l1llll_opy_ = False