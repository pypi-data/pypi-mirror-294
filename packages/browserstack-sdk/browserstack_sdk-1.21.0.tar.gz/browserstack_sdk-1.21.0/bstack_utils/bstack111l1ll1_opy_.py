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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l111l1ll_opy_ as bstack11l11l1lll_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.helper import bstack1l1lll1l_opy_, bstack11ll111l_opy_, bstack1l1l1l1ll_opy_, bstack11l11l1l1l_opy_, bstack11l11llll1_opy_, bstack11lll11ll1_opy_, get_host_info, bstack11l11l1l11_opy_, bstack11lll111l_opy_, bstack11l1l11l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11l1l11l_opy_(class_method=False)
def _11l111l111_opy_(driver, bstack1111l1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11llll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪ໷"): caps.get(bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ໸"), None),
        bstack11llll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໹"): bstack1111l1ll_opy_.get(bstack11llll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ໺"), None),
        bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ໻"): caps.get(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ໼"), None),
        bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໽"): caps.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ໾"), None)
    }
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧ໿") + str(error))
  return response
def on():
    if os.environ.get(bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩༀ"), None) is None or os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ༁")] == bstack11llll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ༂"):
        return False
    return True
def bstack111lllllll_opy_(config):
  return config.get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༃"), False) or any([p.get(bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ༄"), False) == True for p in config.get(bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ༅"), [])])
def bstack111l1l1ll_opy_(config, bstack111lll1l1_opy_):
  try:
    if not bstack1l1l1l1ll_opy_(config):
      return False
    bstack11l11ll11l_opy_ = config.get(bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ༆"), False)
    if int(bstack111lll1l1_opy_) < len(config.get(bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༇"), [])) and config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༈")][bstack111lll1l1_opy_]:
      bstack11l1111111_opy_ = config[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༉")][bstack111lll1l1_opy_].get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༊"), None)
    else:
      bstack11l1111111_opy_ = config.get(bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ་"), None)
    if bstack11l1111111_opy_ != None:
      bstack11l11ll11l_opy_ = bstack11l1111111_opy_
    bstack11l11l111l_opy_ = os.getenv(bstack11llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༌")) is not None and len(os.getenv(bstack11llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ།"))) > 0 and os.getenv(bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ༎")) != bstack11llll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ༏")
    return bstack11l11ll11l_opy_ and bstack11l11l111l_opy_
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭༐") + str(error))
  return False
def bstack1lll11lll_opy_(test_tags):
  bstack11l111111l_opy_ = os.getenv(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ༑"))
  if bstack11l111111l_opy_ is None:
    return True
  bstack11l111111l_opy_ = json.loads(bstack11l111111l_opy_)
  try:
    include_tags = bstack11l111111l_opy_[bstack11llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭༒")] if bstack11llll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ༓") in bstack11l111111l_opy_ and isinstance(bstack11l111111l_opy_[bstack11llll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ༔")], list) else []
    exclude_tags = bstack11l111111l_opy_[bstack11llll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ༕")] if bstack11llll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ༖") in bstack11l111111l_opy_ and isinstance(bstack11l111111l_opy_[bstack11llll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ༗")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿༘ࠦࠢ") + str(error))
  return False
def bstack11l11l1ll1_opy_(config, bstack11l11l1111_opy_, bstack11l11111l1_opy_, bstack11l111llll_opy_):
  bstack11l1111ll1_opy_ = bstack11l11l1l1l_opy_(config)
  bstack11l111l11l_opy_ = bstack11l11llll1_opy_(config)
  if bstack11l1111ll1_opy_ is None or bstack11l111l11l_opy_ is None:
    logger.error(bstack11llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯༙ࠩ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ༚"), bstack11llll_opy_ (u"ࠪࡿࢂ࠭༛")))
    data = {
        bstack11llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ༜"): config[bstack11llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ༝")],
        bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༞"): config.get(bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ༟"), os.path.basename(os.getcwd())),
        bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫ༠"): bstack1l1lll1l_opy_(),
        bstack11llll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ༡"): config.get(bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭༢"), bstack11llll_opy_ (u"ࠫࠬ༣")),
        bstack11llll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ༤"): {
            bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭༥"): bstack11l11l1111_opy_,
            bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ༦"): bstack11l11111l1_opy_,
            bstack11llll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ༧"): __version__,
            bstack11llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ༨"): bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ༩"),
            bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ༪"): bstack11llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ༫"),
            bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭༬"): bstack11l111llll_opy_
        },
        bstack11llll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ༭"): settings,
        bstack11llll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ༮"): bstack11l11l1l11_opy_(),
        bstack11llll_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ༯"): bstack11lll11ll1_opy_(),
        bstack11llll_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬ༰"): get_host_info(),
        bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭༱"): bstack1l1l1l1ll_opy_(config)
    }
    headers = {
        bstack11llll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ༲"): bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ༳"),
    }
    config = {
        bstack11llll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ༴"): (bstack11l1111ll1_opy_, bstack11l111l11l_opy_),
        bstack11llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴ༵ࠩ"): headers
    }
    response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ༶"), bstack11l11l1lll_opy_ + bstack11llll_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ༷ࠪ"), data, config)
    bstack11l11ll111_opy_ = response.json()
    if bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ༸")]:
      parsed = json.loads(os.getenv(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ༹࠭"), bstack11llll_opy_ (u"࠭ࡻࡾࠩ༺")))
      parsed[bstack11llll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ༻")] = bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠨࡦࡤࡸࡦ࠭༼")][bstack11llll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ༽")]
      os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ༾")] = json.dumps(parsed)
      bstack1lll11ll11_opy_.bstack11l1111l11_opy_(bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠫࡩࡧࡴࡢࠩ༿")][bstack11llll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ཀ")])
      bstack1lll11ll11_opy_.bstack11l111ll1l_opy_(bstack11l11ll111_opy_[bstack11llll_opy_ (u"࠭ࡤࡢࡶࡤࠫཁ")][bstack11llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩག")])
      bstack1lll11ll11_opy_.store()
      return bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠨࡦࡤࡸࡦ࠭གྷ")][bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧང")], bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨཅ")][bstack11llll_opy_ (u"ࠫ࡮ࡪࠧཆ")]
    else:
      logger.error(bstack11llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ཇ") + bstack11l11ll111_opy_[bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ཈")])
      if bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཉ")] == bstack11llll_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪཊ"):
        for bstack11l11ll1ll_opy_ in bstack11l11ll111_opy_[bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩཋ")]:
          logger.error(bstack11l11ll1ll_opy_[bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཌ")])
      return None, None
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧཌྷ") +  str(error))
    return None, None
def bstack11l11l11l1_opy_():
  if os.getenv(bstack11llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪཎ")) is None:
    return {
        bstack11llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ཏ"): bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ཐ"),
        bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩད"): bstack11llll_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨདྷ")
    }
  data = {bstack11llll_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫན"): bstack1l1lll1l_opy_()}
  headers = {
      bstack11llll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫཔ"): bstack11llll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ཕ") + os.getenv(bstack11llll_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦབ")),
      bstack11llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭བྷ"): bstack11llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫམ")
  }
  response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠩࡓ࡙࡙࠭ཙ"), bstack11l11l1lll_opy_ + bstack11llll_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬཚ"), data, { bstack11llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬཛ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11llll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨཛྷ") + bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"࡚࠭ࠨཝ"))
      return {bstack11llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧཞ"): bstack11llll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩཟ"), bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪའ"): bstack11llll_opy_ (u"ࠪࠫཡ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢར") + str(error))
    return {
        bstack11llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬལ"): bstack11llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬཤ"),
        bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཥ"): str(error)
    }
def bstack1ll1lll11l_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l11lll1l_opy_ = caps.get(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩས"), {}).get(bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ཧ"), caps.get(bstack11llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪཨ"), bstack11llll_opy_ (u"ࠫࠬཀྵ")))
    if bstack11l11lll1l_opy_:
      logger.warn(bstack11llll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤཪ"))
      return False
    if options:
      bstack11l11111ll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l11111ll_opy_ = desired_capabilities
    else:
      bstack11l11111ll_opy_ = {}
    browser = caps.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫཫ"), bstack11llll_opy_ (u"ࠧࠨཬ")).lower() or bstack11l11111ll_opy_.get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭཭"), bstack11llll_opy_ (u"ࠩࠪ཮")).lower()
    if browser != bstack11llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ཯"):
      logger.warn(bstack11llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ཰"))
      return False
    browser_version = caps.get(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳཱ࠭")) or caps.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨི")) or bstack11l11111ll_opy_.get(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨཱི")) or bstack11l11111ll_opy_.get(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴུࠩ"), {}).get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰཱུࠪ")) or bstack11l11111ll_opy_.get(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫྲྀ"), {}).get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ཷ"))
    if browser_version and browser_version != bstack11llll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬླྀ") and int(browser_version.split(bstack11llll_opy_ (u"࠭࠮ࠨཹ"))[0]) <= 98:
      logger.warn(bstack11llll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ེࠧ"))
      return False
    if not options:
      bstack11l111ll11_opy_ = caps.get(bstack11llll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸཻ࠭")) or bstack11l11111ll_opy_.get(bstack11llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹོࠧ"), {})
      if bstack11llll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹཽࠧ") in bstack11l111ll11_opy_.get(bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩཾ"), []):
        logger.warn(bstack11llll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢཿ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ྀࠣ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1111lll_opy_ = config.get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹཱྀࠧ"), {})
    bstack11l1111lll_opy_[bstack11llll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫྂ")] = os.getenv(bstack11llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧྃ"))
    bstack11l1111l1l_opy_ = json.loads(os.getenv(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏ྄ࠫ"), bstack11llll_opy_ (u"ࠫࢀࢃࠧ྅"))).get(bstack11llll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭྆"))
    caps[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭྇")] = True
    if bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨྈ") in caps:
      caps[bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩྉ")][bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩྊ")] = bstack11l1111lll_opy_
      caps[bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫྋ")][bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫྌ")][bstack11llll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ྍ")] = bstack11l1111l1l_opy_
    else:
      caps[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬྎ")] = bstack11l1111lll_opy_
      caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ྏ")][bstack11llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩྐ")] = bstack11l1111l1l_opy_
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥྑ") +  str(error))
def bstack1l11l1l111_opy_(driver, bstack11l111l1l1_opy_):
  try:
    setattr(driver, bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪྒ"), True)
    session = driver.session_id
    if session:
      bstack11l11ll1l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11ll1l1_opy_ = False
      bstack11l11ll1l1_opy_ = url.scheme in [bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱࠤྒྷ"), bstack11llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦྔ")]
      if bstack11l11ll1l1_opy_:
        if bstack11l111l1l1_opy_:
          logger.info(bstack11llll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨྕ"))
      return bstack11l111l1l1_opy_
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥྖ") + str(e))
    return False
def bstack111llll1_opy_(driver, name, path):
  try:
    bstack11l11lll11_opy_ = {
        bstack11llll_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨྗ"): threading.current_thread().current_test_uuid,
        bstack11llll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ྘"): os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨྙ"), bstack11llll_opy_ (u"ࠫࠬྚ")),
        bstack11llll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩྛ"): os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧྜ"), bstack11llll_opy_ (u"ࠧࠨྜྷ"))
    }
    logger.debug(bstack11llll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫྞ"))
    logger.debug(driver.execute_async_script(bstack1lll11ll11_opy_.perform_scan, {bstack11llll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤྟ"): name}))
    logger.debug(driver.execute_async_script(bstack1lll11ll11_opy_.bstack11l111lll1_opy_, bstack11l11lll11_opy_))
    logger.info(bstack11llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨྠ"))
  except Exception as bstack11l11l11ll_opy_:
    logger.error(bstack11llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨྡ") + str(path) + bstack11llll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢྡྷ") + str(bstack11l11l11ll_opy_))