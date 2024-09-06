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
import threading
import logging
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from bstack_utils.helper import bstack1lll1111_opy_
logger = logging.getLogger(__name__)
def bstack11l11lllll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1lll11111l_opy_(context, *args):
    tags = getattr(args[0], bstack11llll_opy_ (u"࠭ࡴࡢࡩࡶࠫྸ"), [])
    bstack1ll11l1l11_opy_ = bstack111l111l_opy_.bstack1lll11lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll11l1l11_opy_
    try:
      bstack1l1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lllll_opy_(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ྐྵ")) else context.browser
      if bstack1l1111l111_opy_ and bstack1l1111l111_opy_.session_id and bstack1ll11l1l11_opy_ and bstack1lll1111_opy_(
              threading.current_thread(), bstack11llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧྺ"), None):
          threading.current_thread().isA11yTest = bstack111l111l_opy_.bstack1l11l1l111_opy_(bstack1l1111l111_opy_, bstack1ll11l1l11_opy_)
    except Exception as e:
       logger.debug(bstack11llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩྻ").format(str(e)))
def bstack1ll1l1ll1_opy_(bstack1l1111l111_opy_):
    if bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧྼ"), None) and bstack1lll1111_opy_(
      threading.current_thread(), bstack11llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ྽"), None) and not bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨ྾"), False):
      threading.current_thread().a11y_stop = True
      bstack111l111l_opy_.bstack111llll1_opy_(bstack1l1111l111_opy_, name=bstack11llll_opy_ (u"ࠨࠢ྿"), path=bstack11llll_opy_ (u"ࠢࠣ࿀"))