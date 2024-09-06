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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from browserstack_sdk.bstack111lllll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l11l_opy_
class bstack1111ll1l_opy_:
    def __init__(self, args, logger, bstack1111l1l1_opy_, bstack11111lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1_opy_ = bstack1111l1l1_opy_
        self.bstack11111lll_opy_ = bstack11111lll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111111ll_opy_ = []
        self.bstack111l1l11_opy_ = None
        self.bstack111l1111_opy_ = []
        self.bstack111l11l1_opy_ = self.bstack1111llll_opy_()
        self.bstack111lll1l_opy_ = -1
    def bstack1111l111_opy_(self, bstack1111ll11_opy_):
        self.parse_args()
        self.bstack111ll1ll_opy_()
        self.bstack11111l11_opy_(bstack1111ll11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111lll1_opy_():
        import importlib
        if getattr(importlib, bstack11llll_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬম"), False):
            bstack111l1l1l_opy_ = importlib.find_loader(bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪয"))
        else:
            bstack111l1l1l_opy_ = importlib.util.find_spec(bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫর"))
    def bstack1llllll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111lll1l_opy_ = -1
        if self.bstack11111lll_opy_ and bstack11llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ঱") in self.bstack1111l1l1_opy_:
            self.bstack111lll1l_opy_ = int(self.bstack1111l1l1_opy_[bstack11llll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫল")])
        try:
            bstack111ll1l1_opy_ = [bstack11llll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ঳"), bstack11llll_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ঴"), bstack11llll_opy_ (u"ࠧ࠮ࡲࠪ঵")]
            if self.bstack111lll1l_opy_ >= 0:
                bstack111ll1l1_opy_.extend([bstack11llll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩশ"), bstack11llll_opy_ (u"ࠩ࠰ࡲࠬষ")])
            for arg in bstack111ll1l1_opy_:
                self.bstack1llllll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111ll1ll_opy_(self):
        bstack111l1l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l1l11_opy_ = bstack111l1l11_opy_
        return bstack111l1l11_opy_
    def bstack1lllllll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111lll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1111l11l_opy_)
    def bstack11111l11_opy_(self, bstack1111ll11_opy_):
        bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
        if bstack1111ll11_opy_:
            self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧস"))
            self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"࡙ࠫࡸࡵࡦࠩহ"))
        if bstack1111111l_opy_.bstack111lll11_opy_():
            self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ঺"))
            self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"࠭ࡔࡳࡷࡨࠫ঻"))
        self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠧ࠮ࡲ়ࠪ"))
        self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ঽ"))
        self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫা"))
        self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪি"))
        if self.bstack111lll1l_opy_ > 1:
            self.bstack111l1l11_opy_.append(bstack11llll_opy_ (u"ࠫ࠲ࡴࠧী"))
            self.bstack111l1l11_opy_.append(str(self.bstack111lll1l_opy_))
    def bstack111ll111_opy_(self):
        bstack111l1111_opy_ = []
        for spec in self.bstack111111ll_opy_:
            bstack1llllllll_opy_ = [spec]
            bstack1llllllll_opy_ += self.bstack111l1l11_opy_
            bstack111l1111_opy_.append(bstack1llllllll_opy_)
        self.bstack111l1111_opy_ = bstack111l1111_opy_
        return bstack111l1111_opy_
    def bstack1111llll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l11l1_opy_ = True
            return True
        except Exception as e:
            self.bstack111l11l1_opy_ = False
        return self.bstack111l11l1_opy_
    def bstack11111111_opy_(self, bstack1lllll1ll_opy_, bstack1111l111_opy_):
        bstack1111l111_opy_[bstack11llll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬু")] = self.bstack1111l1l1_opy_
        multiprocessing.set_start_method(bstack11llll_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬূ"))
        bstack111l1lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llllll1l_opy_ = manager.list()
        if bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪৃ") in self.bstack1111l1l1_opy_:
            for index, platform in enumerate(self.bstack1111l1l1_opy_[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৄ")]):
                bstack111l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lllll1ll_opy_,
                                                            args=(self.bstack111l1l11_opy_, bstack1111l111_opy_, bstack1llllll1l_opy_)))
            bstack111111l1_opy_ = len(self.bstack1111l1l1_opy_[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ৅")])
        else:
            bstack111l1lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lllll1ll_opy_,
                                                        args=(self.bstack111l1l11_opy_, bstack1111l111_opy_, bstack1llllll1l_opy_)))
            bstack111111l1_opy_ = 1
        i = 0
        for t in bstack111l1lll_opy_:
            os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ৆")] = str(i)
            if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে") in self.bstack1111l1l1_opy_:
                os.environ[bstack11llll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ৈ")] = json.dumps(self.bstack1111l1l1_opy_[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৉")][i % bstack111111l1_opy_])
            i += 1
            t.start()
        for t in bstack111l1lll_opy_:
            t.join()
        return list(bstack1llllll1l_opy_)
    @staticmethod
    def bstack11111ll1_opy_(driver, bstack1111l1ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ৊"), None)
        if item and getattr(item, bstack11llll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪো"), None) and not getattr(item, bstack11llll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫৌ"), False):
            logger.info(
                bstack11llll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤ্"))
            bstack111ll11l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111l111l_opy_.bstack111llll1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)