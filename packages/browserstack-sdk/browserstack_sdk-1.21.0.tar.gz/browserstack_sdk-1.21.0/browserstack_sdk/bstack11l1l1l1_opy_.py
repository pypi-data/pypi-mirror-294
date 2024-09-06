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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1l1_opy_, bstack11111lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1_opy_ = bstack1111l1l1_opy_
        self.bstack11111lll_opy_ = bstack11111lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l111lll_opy_(bstack1lllll1l1_opy_):
        bstack1lllll11l_opy_ = []
        if bstack1lllll1l1_opy_:
            tokens = str(os.path.basename(bstack1lllll1l1_opy_)).split(bstack11llll_opy_ (u"ࠦࡤࠨৎ"))
            camelcase_name = bstack11llll_opy_ (u"ࠧࠦࠢ৏").join(t.title() for t in tokens)
            suite_name, bstack1llll1lll_opy_ = os.path.splitext(camelcase_name)
            bstack1lllll11l_opy_.append(suite_name)
        return bstack1lllll11l_opy_
    @staticmethod
    def bstack1lllll111_opy_(typename):
        if bstack11llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ৐") in typename:
            return bstack11llll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ৑")
        return bstack11llll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ৒")