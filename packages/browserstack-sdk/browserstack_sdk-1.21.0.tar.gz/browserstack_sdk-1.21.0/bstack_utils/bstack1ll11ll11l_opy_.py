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
import re
from bstack_utils.bstack1l1ll1111l_opy_ import bstack1lll11ll1l1_opy_
def bstack1lll11lllll_opy_(fixture_name):
    if fixture_name.startswith(bstack11llll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖤ")):
        return bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᖥ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖦ")):
        return bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᖧ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖨ")):
        return bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᖩ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖪ")):
        return bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᖫ")
def bstack1lll11ll111_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᖬ"), fixture_name))
def bstack1lll11llll1_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᖭ"), fixture_name))
def bstack1lll11lll1l_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᖮ"), fixture_name))
def bstack1lll11lll11_opy_(fixture_name):
    if fixture_name.startswith(bstack11llll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᖯ")):
        return bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᖰ"), bstack11llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᖱ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖲ")):
        return bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖳ"), bstack11llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᖴ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᖵ")):
        return bstack11llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᖶ"), bstack11llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᖷ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖸ")):
        return bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᖹ"), bstack11llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᖺ")
    return None, None
def bstack1lll1l111l1_opy_(hook_name):
    if hook_name in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᖻ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᖼ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11l1ll1_opy_(hook_name):
    if hook_name in [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᖽ"), bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᖾ")]:
        return bstack11llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᖿ")
    elif hook_name in [bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᗀ"), bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᗁ")]:
        return bstack11llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᗂ")
    elif hook_name in [bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᗃ"), bstack11llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᗄ")]:
        return bstack11llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᗅ")
    elif hook_name in [bstack11llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᗆ"), bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᗇ")]:
        return bstack11llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᗈ")
    return hook_name
def bstack1lll11l1lll_opy_(node, scenario):
    if hasattr(node, bstack11llll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᗉ")):
        parts = node.nodeid.rsplit(bstack11llll_opy_ (u"ࠨ࡛ࠣᗊ"))
        params = parts[-1]
        return bstack11llll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᗋ").format(scenario.name, params)
    return scenario.name
def bstack1lll1l1111l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11llll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᗌ")):
            examples = list(node.callspec.params[bstack11llll_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᗍ")].values())
        return examples
    except:
        return []
def bstack1lll1l11111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11ll11l_opy_(report):
    try:
        status = bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᗎ")
        if report.passed or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᗏ"))):
            status = bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᗐ")
        elif report.skipped:
            status = bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᗑ")
        bstack1lll11ll1l1_opy_(status)
    except:
        pass
def bstack1l1l111l11_opy_(status):
    try:
        bstack1lll11l1l1l_opy_ = bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗒ")
        if status == bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗓ"):
            bstack1lll11l1l1l_opy_ = bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᗔ")
        elif status == bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᗕ"):
            bstack1lll11l1l1l_opy_ = bstack11llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᗖ")
        bstack1lll11ll1l1_opy_(bstack1lll11l1l1l_opy_)
    except:
        pass
def bstack1lll11ll1ll_opy_(item=None, report=None, summary=None, extra=None):
    return