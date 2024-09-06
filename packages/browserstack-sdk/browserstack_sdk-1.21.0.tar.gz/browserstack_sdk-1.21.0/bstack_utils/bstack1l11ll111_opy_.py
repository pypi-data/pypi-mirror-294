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
from browserstack_sdk.bstack11111l1l_opy_ import bstack1111ll1l_opy_
from browserstack_sdk.bstack11l1l1l1_opy_ import RobotHandler
def bstack1l11111ll1_opy_(framework):
    if framework.lower() == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪኰ"):
        return bstack1111ll1l_opy_.version()
    elif framework.lower() == bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ኱"):
        return RobotHandler.version()
    elif framework.lower() == bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬኲ"):
        import behave
        return behave.__version__
    else:
        return bstack11llll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧኳ")