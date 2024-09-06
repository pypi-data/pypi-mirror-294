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
import datetime
import threading
from bstack_utils.helper import bstack11l11l1l11_opy_, bstack11lll11ll1_opy_, get_host_info, bstack111l11ll11_opy_, \
 bstack1l1l1l1ll_opy_, bstack1lll1111_opy_, bstack11l1l11l_opy_, bstack111l11ll1l_opy_, bstack1l1lll1l_opy_
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
from bstack_utils.percy import bstack1l11l1l11l_opy_
from bstack_utils.config import Config
bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l11l1l11l_opy_()
@bstack11l1l11l_opy_(class_method=False)
def bstack1ll1ll11ll1_opy_(bs_config, bstack1l1l111l1_opy_):
  try:
    data = {
        bstack11llll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩᜲ"): bstack11llll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨᜳ"),
        bstack11llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧ᜴ࠪ"): bs_config.get(bstack11llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᜵"), bstack11llll_opy_ (u"࠭ࠧ᜶")),
        bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᜷"): bs_config.get(bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᜸"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᜹"): bs_config.get(bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᜺")),
        bstack11llll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ᜻"): bs_config.get(bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ᜼"), bstack11llll_opy_ (u"࠭ࠧ᜽")),
        bstack11llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᜾"): bstack1l1lll1l_opy_(),
        bstack11llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭᜿"): bstack111l11ll11_opy_(bs_config),
        bstack11llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬᝀ"): get_host_info(),
        bstack11llll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫᝁ"): bstack11lll11ll1_opy_(),
        bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝂ"): os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᝃ")),
        bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫᝄ"): os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬᝅ"), False),
        bstack11llll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪᝆ"): bstack11l11l1l11_opy_(),
        bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᝇ"): bstack1ll1l111lll_opy_(),
        bstack11llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧᝈ"): bstack1ll1l111l11_opy_(bstack1l1l111l1_opy_),
        bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩᝉ"): bstack111111ll1_opy_(bs_config, bstack1l1l111l1_opy_.get(bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᝊ"), bstack11llll_opy_ (u"࠭ࠧᝋ"))),
        bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᝌ"): bstack1l1l1l1ll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤᝍ").format(str(error)))
    return None
def bstack1ll1l111l11_opy_(framework):
  return {
    bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᝎ"): framework.get(bstack11llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫᝏ"), bstack11llll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᝐ")),
    bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᝑ"): framework.get(bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᝒ")),
    bstack11llll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᝓ"): framework.get(bstack11llll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᝔")),
    bstack11llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ᝕"): bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᝖"),
    bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ᝗"): framework.get(bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᝘"))
  }
def bstack111111ll1_opy_(bs_config, framework):
  bstack1llllll1l1_opy_ = False
  bstack1ll1l1llll_opy_ = False
  if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪ᝙") in bs_config:
    bstack1llllll1l1_opy_ = True
  else:
    bstack1ll1l1llll_opy_ = True
  bstack11lllllll1_opy_ = {
    bstack11llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᝚"): bstack1ll1l111_opy_.bstack1ll1l11l1ll_opy_(bs_config, framework),
    bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝛"): bstack111l111l_opy_.bstack111lllllll_opy_(bs_config),
    bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᝜"): bs_config.get(bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᝝"), False),
    bstack11llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᝞"): bstack1ll1l1llll_opy_,
    bstack11llll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᝟"): bstack1llllll1l1_opy_
  }
  return bstack11lllllll1_opy_
@bstack11l1l11l_opy_(class_method=False)
def bstack1ll1l111lll_opy_():
  try:
    bstack1ll1l111l1l_opy_ = json.loads(os.getenv(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᝠ"), bstack11llll_opy_ (u"ࠧࡼࡿࠪᝡ")))
    return {
        bstack11llll_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᝢ"): bstack1ll1l111l1l_opy_
    }
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣᝣ").format(str(error)))
    return {}
def bstack1ll1ll11l1l_opy_(array, bstack1ll1l11l111_opy_, bstack1ll1l11ll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l11l111_opy_]
    result[key] = o[bstack1ll1l11ll1l_opy_]
  return result
def bstack1ll1l1l1111_opy_(bstack11l1l1lll_opy_=bstack11llll_opy_ (u"ࠪࠫᝤ")):
  bstack1ll1l111ll1_opy_ = bstack111l111l_opy_.on()
  bstack1ll1l11l1l1_opy_ = bstack1ll1l111_opy_.on()
  bstack1ll1l11l11l_opy_ = percy.bstack1lll1lll11l_opy_()
  if bstack1ll1l11l11l_opy_ and not bstack1ll1l11l1l1_opy_ and not bstack1ll1l111ll1_opy_:
    return bstack11l1l1lll_opy_ not in [bstack11llll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᝥ"), bstack11llll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᝦ")]
  elif bstack1ll1l111ll1_opy_ and not bstack1ll1l11l1l1_opy_:
    return bstack11l1l1lll_opy_ not in [bstack11llll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᝧ"), bstack11llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᝨ"), bstack11llll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᝩ")]
  return bstack1ll1l111ll1_opy_ or bstack1ll1l11l1l1_opy_ or bstack1ll1l11l11l_opy_
@bstack11l1l11l_opy_(class_method=False)
def bstack1ll1l1l1l11_opy_(bstack11l1l1lll_opy_, test=None):
  bstack1ll1l11ll11_opy_ = bstack111l111l_opy_.on()
  if not bstack1ll1l11ll11_opy_ or bstack11l1l1lll_opy_ not in [bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᝪ")] or test == None:
    return None
  return {
    bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᝫ"): bstack1ll1l11ll11_opy_ and bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᝬ"), None) == True and bstack111l111l_opy_.bstack1lll11lll_opy_(test[bstack11llll_opy_ (u"ࠬࡺࡡࡨࡵࠪ᝭")])
  }