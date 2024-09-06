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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l11l1l1l_opy_, bstack11l11llll1_opy_, bstack11lll111l_opy_, bstack11l1l11l_opy_, bstack111l1l11l1_opy_, bstack111l11l11l_opy_, bstack111l11ll1l_opy_, bstack1l1lll1l_opy_
from bstack_utils.bstack1lll11l11ll_opy_ import bstack1lll11l1l11_opy_
import bstack_utils.bstack1l1llllll1_opy_ as bstack111lll111_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack11lllll1_opy_
bstack1ll1ll1111l_opy_ = bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᙌ")
logger = logging.getLogger(__name__)
class bstack1ll11ll1_opy_:
    bstack1lll11l11ll_opy_ = None
    bs_config = None
    bstack1l1l111l1_opy_ = None
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l1l111l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1l111l1_opy_ = bstack1l1l111l1_opy_
        try:
            cls.bstack1ll1l11lll1_opy_()
            bstack11l1111ll1_opy_ = bstack11l11l1l1l_opy_(bs_config)
            bstack11l111l11l_opy_ = bstack11l11llll1_opy_(bs_config)
            data = bstack111lll111_opy_.bstack1ll1ll11ll1_opy_(bs_config, bstack1l1l111l1_opy_)
            config = {
                bstack11llll_opy_ (u"ࠫࡦࡻࡴࡩࠩᙍ"): (bstack11l1111ll1_opy_, bstack11l111l11l_opy_),
                bstack11llll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᙎ"): cls.default_headers()
            }
            response = bstack11lll111l_opy_(bstack11llll_opy_ (u"࠭ࡐࡐࡕࡗࠫᙏ"), cls.request_url(bstack11llll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧᙐ")), data, config)
            if response.status_code != 200:
                bstack1ll1ll1l1l1_opy_ = response.json()
                if bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᙑ")] == False:
                    cls.bstack1ll1l1ll111_opy_(bstack1ll1ll1l1l1_opy_)
                    return
                cls.bstack1ll1l1l1ll1_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᙒ")])
                cls.bstack1ll1l1lllll_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᙓ")])
                return None
            bstack1ll1ll1ll1l_opy_ = cls.bstack1ll1ll11lll_opy_(response)
            return bstack1ll1ll1ll1l_opy_
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤᙔ").format(str(error)))
            return None
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def stop(cls, bstack1ll1l1lll11_opy_=None):
        if not bstack1ll1l111_opy_.on() and not bstack111l111l_opy_.on():
            return
        if os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᙕ")) == bstack11llll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᙖ") or os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᙗ")) == bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨᙘ"):
            logger.error(bstack11llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᙙ"))
            return {
                bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙚ"): bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᙛ"),
                bstack11llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙜ"): bstack11llll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᙝ")
            }
        try:
            cls.bstack1lll11l11ll_opy_.shutdown()
            data = {
                bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙞ"): bstack1l1lll1l_opy_()
            }
            if not bstack1ll1l1lll11_opy_ is None:
                data[bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬᙟ")] = [{
                    bstack11llll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᙠ"): bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨᙡ"),
                    bstack11llll_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫᙢ"): bstack1ll1l1lll11_opy_
                }]
            config = {
                bstack11llll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᙣ"): cls.default_headers()
            }
            bstack11111ll11l_opy_ = bstack11llll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧᙤ").format(os.environ[bstack11llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧᙥ")])
            bstack1ll1l1l1l1l_opy_ = cls.request_url(bstack11111ll11l_opy_)
            response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠨࡒࡘࡘࠬᙦ"), bstack1ll1l1l1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11llll_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣᙧ"))
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢᙨ") + str(error))
            return {
                bstack11llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᙩ"): bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙪ"),
                bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙫ"): str(error)
            }
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack1ll1ll11lll_opy_(cls, response):
        bstack1ll1ll1l1l1_opy_ = response.json()
        bstack1ll1ll1ll1l_opy_ = {}
        if bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠧ࡫ࡹࡷࠫᙬ")) is None:
            os.environ[bstack11llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᙭")] = bstack11llll_opy_ (u"ࠩࡱࡹࡱࡲࠧ᙮")
        else:
            os.environ[bstack11llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᙯ")] = bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠫ࡯ࡽࡴࠨᙰ"), bstack11llll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᙱ"))
        os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᙲ")] = bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᙳ"), bstack11llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᙴ"))
        if bstack1ll1l111_opy_.bstack1ll1ll1l11l_opy_(cls.bs_config, cls.bstack1l1l111l1_opy_.get(bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᙵ"), bstack11llll_opy_ (u"ࠪࠫᙶ"))) is True:
            bstack1ll1l1l1lll_opy_, bstack1ll1ll1ll11_opy_, bstack1ll1ll111ll_opy_ = cls.bstack1ll1l1l111l_opy_(bstack1ll1ll1l1l1_opy_)
            if bstack1ll1l1l1lll_opy_ != None and bstack1ll1ll1ll11_opy_ != None:
                bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᙷ")] = {
                    bstack11llll_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨᙸ"): bstack1ll1l1l1lll_opy_,
                    bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᙹ"): bstack1ll1ll1ll11_opy_,
                    bstack11llll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᙺ"): bstack1ll1ll111ll_opy_
                }
            else:
                bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᙻ")] = {}
        else:
            bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᙼ")] = {}
        if bstack111l111l_opy_.bstack111lllllll_opy_(cls.bs_config) is True:
            bstack1ll1ll1l1ll_opy_, bstack1ll1ll1ll11_opy_ = cls.bstack1ll1l1l11l1_opy_(bstack1ll1ll1l1l1_opy_)
            if bstack1ll1ll1l1ll_opy_ != None and bstack1ll1ll1ll11_opy_ != None:
                bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᙽ")] = {
                    bstack11llll_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨᙾ"): bstack1ll1ll1l1ll_opy_,
                    bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᙿ"): bstack1ll1ll1ll11_opy_,
                }
            else:
                bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ ")] = {}
        else:
            bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚁ")] = {}
        if bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚂ")].get(bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚃ")) != None or bstack1ll1ll1ll1l_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚄ")].get(bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚅ")) != None:
            cls.bstack1ll1l1ll1ll_opy_(bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠬࡰࡷࡵࠩᚆ")), bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚇ")))
        return bstack1ll1ll1ll1l_opy_
    @classmethod
    def bstack1ll1l1l111l_opy_(cls, bstack1ll1ll1l1l1_opy_):
        if bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚈ")) == None:
            cls.bstack1ll1l1l1ll1_opy_()
            return [None, None, None]
        if bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚉ")][bstack11llll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᚊ")] != True:
            cls.bstack1ll1l1l1ll1_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚋ")])
            return [None, None, None]
        logger.debug(bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᚌ"))
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᚍ")] = bstack11llll_opy_ (u"࠭ࡴࡳࡷࡨࠫᚎ")
        if bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠧ࡫ࡹࡷࠫᚏ")):
            os.environ[bstack11llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᚐ")] = bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᚑ")]
            os.environ[bstack11llll_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᚒ")] = json.dumps({
                bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᚓ"): bstack11l11l1l1l_opy_(cls.bs_config),
                bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᚔ"): bstack11l11llll1_opy_(cls.bs_config)
            })
        if bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚕ")):
            os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᚖ")] = bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚗ")]
        if bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚘ")].get(bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚙ"), {}).get(bstack11llll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᚚ")):
            os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭᚛")] = str(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᚜")][bstack11llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᚝")][bstack11llll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ᚞")])
        return [bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠩ࡭ࡻࡹ࠭᚟")], bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᚠ")], os.environ[bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᚡ")]]
    @classmethod
    def bstack1ll1l1l11l1_opy_(cls, bstack1ll1ll1l1l1_opy_):
        if bstack1ll1ll1l1l1_opy_.get(bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚢ")) == None:
            cls.bstack1ll1l1lllll_opy_()
            return [None, None]
        if bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚣ")][bstack11llll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᚤ")] != True:
            cls.bstack1ll1l1lllll_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚥ")])
            return [None, None]
        if bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚦ")].get(bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚧ")):
            logger.debug(bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᚨ"))
            parsed = json.loads(os.getenv(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᚩ"), bstack11llll_opy_ (u"࠭ࡻࡾࠩᚪ")))
            capabilities = bstack111lll111_opy_.bstack1ll1ll11l1l_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚫ")][bstack11llll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚬ")][bstack11llll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚭ")], bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᚮ"), bstack11llll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᚯ"))
            bstack1ll1ll1l1ll_opy_ = capabilities[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᚰ")]
            os.environ[bstack11llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᚱ")] = bstack1ll1ll1l1ll_opy_
            parsed[bstack11llll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚲ")] = capabilities[bstack11llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᚳ")]
            os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᚴ")] = json.dumps(parsed)
            scripts = bstack111lll111_opy_.bstack1ll1ll11l1l_opy_(bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ")][bstack11llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᚶ")][bstack11llll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᚷ")], bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚸ"), bstack11llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨᚹ"))
            bstack1lll11ll11_opy_.bstack11l1111l11_opy_(scripts)
            commands = bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚺ")][bstack11llll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᚻ")][bstack11llll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫᚼ")].get(bstack11llll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᚽ"))
            bstack1lll11ll11_opy_.bstack11l111ll1l_opy_(commands)
            bstack1lll11ll11_opy_.store()
        return [bstack1ll1ll1l1ll_opy_, bstack1ll1ll1l1l1_opy_[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚾ")]]
    @classmethod
    def bstack1ll1l1l1ll1_opy_(cls, response=None):
        os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᚿ")] = bstack11llll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛀ")
        os.environ[bstack11llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᛁ")] = bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᛂ")
        os.environ[bstack11llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛃ")] = bstack11llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛄ")
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᛅ")] = bstack11llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛆ")
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᛇ")] = bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨᛈ")
        os.environ[bstack11llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᛉ")] = bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᛊ")
        cls.bstack1ll1l1ll111_opy_(response, bstack11llll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᛋ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1lllll_opy_(cls, response=None):
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛌ")] = bstack11llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛍ")
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᛎ")] = bstack11llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᛏ")
        os.environ[bstack11llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᛐ")] = bstack11llll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛑ")
        cls.bstack1ll1l1ll111_opy_(response, bstack11llll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᛒ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1ll1ll_opy_(cls, bstack1ll1l1ll1l1_opy_, bstack1ll1ll1ll11_opy_):
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛓ")] = bstack1ll1l1ll1l1_opy_
        os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᛔ")] = bstack1ll1ll1ll11_opy_
    @classmethod
    def bstack1ll1l1ll111_opy_(cls, response=None, product=bstack11llll_opy_ (u"ࠢࠣᛕ")):
        if response == None:
            logger.error(product + bstack11llll_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥᛖ"))
        for error in response[bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᛗ")]:
            bstack11111llll1_opy_ = error[bstack11llll_opy_ (u"ࠪ࡯ࡪࡿࠧᛘ")]
            error_message = error[bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᛙ")]
            if error_message:
                if bstack11111llll1_opy_ == bstack11llll_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦᛚ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11llll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢᛛ") + product + bstack11llll_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᛜ"))
    @classmethod
    def bstack1ll1l11lll1_opy_(cls):
        if cls.bstack1lll11l11ll_opy_ is not None:
            return
        cls.bstack1lll11l11ll_opy_ = bstack1lll11l1l11_opy_(cls.bstack1ll1l1ll11l_opy_)
        cls.bstack1lll11l11ll_opy_.start()
    @classmethod
    def bstack1l11ll1l_opy_(cls):
        if cls.bstack1lll11l11ll_opy_ is None:
            return
        cls.bstack1lll11l11ll_opy_.shutdown()
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack1ll1l1ll11l_opy_(cls, bstack1l1l11l1_opy_, bstack1ll1l1lll1l_opy_=bstack11llll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᛝ")):
        config = {
            bstack11llll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᛞ"): cls.default_headers()
        }
        response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᛟ"), cls.request_url(bstack1ll1l1lll1l_opy_), bstack1l1l11l1_opy_, config)
        bstack11l11ll111_opy_ = response.json()
    @classmethod
    def bstack1l11111l_opy_(cls, bstack1l1l11l1_opy_, bstack1ll1l1lll1l_opy_=bstack11llll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᛠ")):
        if not bstack111lll111_opy_.bstack1ll1l1l1111_opy_(bstack1l1l11l1_opy_[bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᛡ")]):
            return
        bstack11lllllll1_opy_ = bstack111lll111_opy_.bstack1ll1l1l1l11_opy_(bstack1l1l11l1_opy_[bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᛢ")], bstack1l1l11l1_opy_.get(bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᛣ")))
        if bstack11lllllll1_opy_ != None:
            bstack1l1l11l1_opy_[bstack11llll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᛤ")] = bstack11lllllll1_opy_
        if bstack1ll1l1lll1l_opy_ == bstack11llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᛥ"):
            cls.bstack1ll1l11lll1_opy_()
            cls.bstack1lll11l11ll_opy_.add(bstack1l1l11l1_opy_)
        elif bstack1ll1l1lll1l_opy_ == bstack11llll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᛦ"):
            cls.bstack1ll1l1ll11l_opy_([bstack1l1l11l1_opy_], bstack1ll1l1lll1l_opy_)
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack1ll1ll1l_opy_(cls, bstack11llllll_opy_):
        bstack1ll1ll1l111_opy_ = []
        for log in bstack11llllll_opy_:
            bstack1ll1ll11111_opy_ = {
                bstack11llll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᛧ"): bstack11llll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧᛨ"),
                bstack11llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᛩ"): log[bstack11llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᛪ")],
                bstack11llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᛫"): log[bstack11llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᛬")],
                bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪ᛭"): {},
                bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᛮ"): log[bstack11llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᛯ")],
            }
            if bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᛰ") in log:
                bstack1ll1ll11111_opy_[bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᛱ")] = log[bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛲ")]
            elif bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᛳ") in log:
                bstack1ll1ll11111_opy_[bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛴ")] = log[bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᛵ")]
            bstack1ll1ll1l111_opy_.append(bstack1ll1ll11111_opy_)
        cls.bstack1l11111l_opy_({
            bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᛶ"): bstack11llll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᛷ"),
            bstack11llll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᛸ"): bstack1ll1ll1l111_opy_
        })
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack1ll1l1llll1_opy_(cls, steps):
        bstack1ll1ll11l11_opy_ = []
        for step in steps:
            bstack1ll1l11llll_opy_ = {
                bstack11llll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭᛹"): bstack11llll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬ᛺"),
                bstack11llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᛻"): step[bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ᛼")],
                bstack11llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᛽"): step[bstack11llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᛾")],
                bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᛿"): step[bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜀ")],
                bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᜁ"): step[bstack11llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᜂ")]
            }
            if bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜃ") in step:
                bstack1ll1l11llll_opy_[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜄ")] = step[bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜅ")]
            elif bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜆ") in step:
                bstack1ll1l11llll_opy_[bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜇ")] = step[bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜈ")]
            bstack1ll1ll11l11_opy_.append(bstack1ll1l11llll_opy_)
        cls.bstack1l11111l_opy_({
            bstack11llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜉ"): bstack11llll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᜊ"),
            bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᜋ"): bstack1ll1ll11l11_opy_
        })
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack1lll1lll1l_opy_(cls, screenshot):
        cls.bstack1l11111l_opy_({
            bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᜌ"): bstack11llll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᜍ"),
            bstack11llll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᜎ"): [{
                bstack11llll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᜏ"): bstack11llll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬᜐ"),
                bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᜑ"): datetime.datetime.utcnow().isoformat() + bstack11llll_opy_ (u"ࠬࡠࠧᜒ"),
                bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜓ"): screenshot[bstack11llll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ᜔࠭")],
                bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᜕"): screenshot[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᜖")]
            }]
        }, bstack1ll1l1lll1l_opy_=bstack11llll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ᜗"))
    @classmethod
    @bstack11l1l11l_opy_(class_method=True)
    def bstack11llllll11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11111l_opy_({
            bstack11llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ᜘"): bstack11llll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ᜙"),
            bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ᜚"): {
                bstack11llll_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ᜛"): cls.current_test_uuid(),
                bstack11llll_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢ᜜"): cls.bstack1l111l11_opy_(driver)
            }
        })
    @classmethod
    def bstack1ll1l1l1_opy_(cls, event: str, bstack1l1l11l1_opy_: bstack11lllll1_opy_):
        bstack11l1ll11_opy_ = {
            bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜝"): event,
            bstack1l1l11l1_opy_.bstack11l1llll_opy_(): bstack1l1l11l1_opy_.bstack11l11l11_opy_(event)
        }
        cls.bstack1l11111l_opy_(bstack11l1ll11_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ᜞"), None) is None or os.environ[bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᜟ")] == bstack11llll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᜠ")) and (os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᜡ"), None) is None or os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᜢ")] == bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨᜣ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1l11ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᜤ"): bstack11llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᜥ"),
            bstack11llll_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᜦ"): bstack11llll_opy_ (u"ࠬࡺࡲࡶࡧࠪᜧ")
        }
        if os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᜨ"), None):
            headers[bstack11llll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᜩ")] = bstack11llll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᜪ").format(os.environ[bstack11llll_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥᜫ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11llll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᜬ").format(bstack1ll1ll1111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᜭ"), None)
    @staticmethod
    def bstack1l111l11_opy_(driver):
        return {
            bstack111l1l11l1_opy_(): bstack111l11l11l_opy_(driver)
        }
    @staticmethod
    def bstack1ll1ll111l1_opy_(exception_info, report):
        return [{bstack11llll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᜮ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lllll111_opy_(typename):
        if bstack11llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᜯ") in typename:
            return bstack11llll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᜰ")
        return bstack11llll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᜱ")