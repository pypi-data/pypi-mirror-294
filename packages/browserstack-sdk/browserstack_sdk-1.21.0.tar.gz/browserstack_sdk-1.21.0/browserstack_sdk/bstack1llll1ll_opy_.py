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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1lllll11_opy_ = {}
        bstack1llll1l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫࡶ"), bstack11llll_opy_ (u"ࠫࠬࡷ"))
        if not bstack1llll1l1_opy_:
            return bstack1lllll11_opy_
        try:
            bstack1llll11l_opy_ = json.loads(bstack1llll1l1_opy_)
            if bstack11llll_opy_ (u"ࠧࡵࡳࠣࡸ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠨ࡯ࡴࠤࡹ")] = bstack1llll11l_opy_[bstack11llll_opy_ (u"ࠢࡰࡵࠥࡺ")]
            if bstack11llll_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧࡻ") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧࡼ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨࡽ")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣࡾ"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣࡿ")))
            if bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢࢀ") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧࢁ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨࢂ")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥࢃ"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣࢄ")))
            if bstack11llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨࢅ") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨࢆ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢࢇ")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ࢈"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤࢉ")))
            if bstack11llll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤࢊ") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢࢋ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣࢌ")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧࢍ"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥࢎ")))
            if bstack11llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ࢏") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ࢐") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ࢑")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ࢒"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ࢓")))
            if bstack11llll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ࢔") in bstack1llll11l_opy_ or bstack11llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ࢕") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ࢖")] = bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦࢗ"), bstack1llll11l_opy_.get(bstack11llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ࢘")))
            if bstack11llll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࢙ࠧ") in bstack1llll11l_opy_:
                bstack1lllll11_opy_[bstack11llll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ࢚")] = bstack1llll11l_opy_[bstack11llll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹ࢛ࠢ")]
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ࢜") +  str(error))
        return bstack1lllll11_opy_