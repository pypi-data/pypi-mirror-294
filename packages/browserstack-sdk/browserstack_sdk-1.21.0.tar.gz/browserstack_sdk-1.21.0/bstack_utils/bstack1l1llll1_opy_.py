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
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1llll_opy_
from bstack_utils.constants import bstack111ll1ll11_opy_
logger = logging.getLogger(__name__)
class bstack1ll1l111_opy_:
    bstack1lll11l11ll_opy_ = None
    @classmethod
    def bstack1l111l1lll_opy_(cls):
        if cls.on():
            logger.info(
                bstack11llll_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᝮ").format(os.environ[bstack11llll_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᝯ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᝰ"), None) is None or os.environ[bstack11llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪ᝱")] == bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᝲ"):
            return False
        return True
    @classmethod
    def bstack1ll1l11l1ll_opy_(cls, bs_config, framework=bstack11llll_opy_ (u"ࠦࠧᝳ")):
        if framework == bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ᝴"):
            return bstack11ll1llll_opy_(bs_config.get(bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᝵")))
        bstack1ll1l11111l_opy_ = framework in bstack111ll1ll11_opy_
        return bstack11ll1llll_opy_(bs_config.get(bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᝶"), bstack1ll1l11111l_opy_))
    @classmethod
    def bstack1ll1l1111ll_opy_(cls, framework):
        return framework in bstack111ll1ll11_opy_
    @classmethod
    def bstack1ll1ll1l11l_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l11l1ll_opy_(bs_config, framework) is True and cls.bstack1ll1l1111ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᝷"), None)
    @staticmethod
    def bstack1l1ll1ll_opy_():
        if getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᝸"), None):
            return {
                bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨ᝹"): bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ᝺"),
                bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝻"): getattr(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ᝼"), None)
            }
        if getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᝽"), None):
            return {
                bstack11llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭᝾"): bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᝿"),
                bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪក"): getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨខ"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l111111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l111lll_opy_(test, hook_name=None):
        bstack1ll11lllll1_opy_ = test.parent
        if hook_name in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪគ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧឃ"), bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ង"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪច")]:
            bstack1ll11lllll1_opy_ = test
        scope = []
        while bstack1ll11lllll1_opy_ is not None:
            scope.append(bstack1ll11lllll1_opy_.name)
            bstack1ll11lllll1_opy_ = bstack1ll11lllll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l1111l1_opy_(hook_type):
        if hook_type == bstack11llll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢឆ"):
            return bstack11llll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢជ")
        elif hook_type == bstack11llll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣឈ"):
            return bstack11llll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧញ")
    @staticmethod
    def bstack1ll11llllll_opy_(bstack111111ll_opy_):
        try:
            if not bstack1ll1l111_opy_.on():
                return bstack111111ll_opy_
            if os.environ.get(bstack11llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦដ"), None) == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧឋ"):
                tests = os.environ.get(bstack11llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧឌ"), None)
                if tests is None or tests == bstack11llll_opy_ (u"ࠤࡱࡹࡱࡲࠢឍ"):
                    return bstack111111ll_opy_
                bstack111111ll_opy_ = tests.split(bstack11llll_opy_ (u"ࠪ࠰ࠬណ"))
                return bstack111111ll_opy_
        except Exception as exc:
            print(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧត"), str(exc))
        return bstack111111ll_opy_