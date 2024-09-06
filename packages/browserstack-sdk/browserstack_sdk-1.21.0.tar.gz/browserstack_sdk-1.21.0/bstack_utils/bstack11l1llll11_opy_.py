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
class bstack1l1l1l11l1_opy_:
    def __init__(self, handler):
        self._1lll1111lll_opy_ = None
        self.handler = handler
        self._1lll1111l1l_opy_ = self.bstack1lll111l111_opy_()
        self.patch()
    def patch(self):
        self._1lll1111lll_opy_ = self._1lll1111l1l_opy_.execute
        self._1lll1111l1l_opy_.execute = self.bstack1lll1111ll1_opy_()
    def bstack1lll1111ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᗗ"), driver_command, None, this, args)
            response = self._1lll1111lll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11llll_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᗘ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1111l1l_opy_.execute = self._1lll1111lll_opy_
    @staticmethod
    def bstack1lll111l111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver