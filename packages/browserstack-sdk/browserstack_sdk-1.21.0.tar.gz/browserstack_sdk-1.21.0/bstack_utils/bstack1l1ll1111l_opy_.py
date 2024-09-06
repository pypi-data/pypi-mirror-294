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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1111l1111l_opy_, bstack11lll1l11_opy_, bstack1lll1111_opy_, bstack11lll11ll_opy_, \
    bstack111l1l1l11_opy_
def bstack1l1llll111_opy_(bstack1lll111111l_opy_):
    for driver in bstack1lll111111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111llllll_opy_(driver, status, reason=bstack11llll_opy_ (u"ࠧࠨᗙ")):
    bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
    if bstack1111111l_opy_.bstack111lll11_opy_():
        return
    bstack1l11lll11l_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᗚ"), bstack11llll_opy_ (u"ࠩࠪᗛ"), status, reason, bstack11llll_opy_ (u"ࠪࠫᗜ"), bstack11llll_opy_ (u"ࠫࠬᗝ"))
    driver.execute_script(bstack1l11lll11l_opy_)
def bstack1ll1ll1lll_opy_(page, status, reason=bstack11llll_opy_ (u"ࠬ࠭ᗞ")):
    try:
        if page is None:
            return
        bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
        if bstack1111111l_opy_.bstack111lll11_opy_():
            return
        bstack1l11lll11l_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᗟ"), bstack11llll_opy_ (u"ࠧࠨᗠ"), status, reason, bstack11llll_opy_ (u"ࠨࠩᗡ"), bstack11llll_opy_ (u"ࠩࠪᗢ"))
        page.evaluate(bstack11llll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᗣ"), bstack1l11lll11l_opy_)
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᗤ"), e)
def bstack11ll11l11l_opy_(type, name, status, reason, bstack1l111l111l_opy_, bstack1l11l11l1l_opy_):
    bstack1llll11ll1_opy_ = {
        bstack11llll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᗥ"): type,
        bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗦ"): {}
    }
    if type == bstack11llll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᗧ"):
        bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗨ")][bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᗩ")] = bstack1l111l111l_opy_
        bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᗪ")][bstack11llll_opy_ (u"ࠫࡩࡧࡴࡢࠩᗫ")] = json.dumps(str(bstack1l11l11l1l_opy_))
    if type == bstack11llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᗬ"):
        bstack1llll11ll1_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗭ")][bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᗮ")] = name
    if type == bstack11llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᗯ"):
        bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗰ")][bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗱ")] = status
        if status == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᗲ") and str(reason) != bstack11llll_opy_ (u"ࠧࠨᗳ"):
            bstack1llll11ll1_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗴ")][bstack11llll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᗵ")] = json.dumps(str(reason))
    bstack11l1l1111_opy_ = bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᗶ").format(json.dumps(bstack1llll11ll1_opy_))
    return bstack11l1l1111_opy_
def bstack111ll1l11_opy_(url, config, logger, bstack11ll1l1ll_opy_=False):
    hostname = bstack11lll1l11_opy_(url)
    is_private = bstack11lll11ll_opy_(hostname)
    try:
        if is_private or bstack11ll1l1ll_opy_:
            file_path = bstack1111l1111l_opy_(bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᗷ"), bstack11llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᗸ"), logger)
            if os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᗹ")) and eval(
                    os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᗺ"))):
                return
            if (bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᗻ") in config and not config[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᗼ")]):
                os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᗽ")] = str(True)
                bstack1lll11111ll_opy_ = {bstack11llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᗾ"): hostname}
                bstack111l1l1l11_opy_(bstack11llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᗿ"), bstack11llll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᘀ"), bstack1lll11111ll_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1ll11_opy_(caps, bstack1lll11111l1_opy_):
    if bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘁ") in caps:
        caps[bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ")][bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᘃ")] = True
        if bstack1lll11111l1_opy_:
            caps[bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘄ")][bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᘅ")] = bstack1lll11111l1_opy_
    else:
        caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᘆ")] = True
        if bstack1lll11111l1_opy_:
            caps[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᘇ")] = bstack1lll11111l1_opy_
def bstack1lll11ll1l1_opy_(bstack11lll11l_opy_):
    bstack1lll1111l11_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᘈ"), bstack11llll_opy_ (u"࠭ࠧᘉ"))
    if bstack1lll1111l11_opy_ == bstack11llll_opy_ (u"ࠧࠨᘊ") or bstack1lll1111l11_opy_ == bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᘋ"):
        threading.current_thread().testStatus = bstack11lll11l_opy_
    else:
        if bstack11lll11l_opy_ == bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᘌ"):
            threading.current_thread().testStatus = bstack11lll11l_opy_