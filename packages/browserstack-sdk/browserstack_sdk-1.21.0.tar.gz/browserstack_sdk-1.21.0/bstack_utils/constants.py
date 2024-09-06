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
import re
bstack1ll11l11ll_opy_ = {
	bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ࿌"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪ࿍"),
  bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࿎"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫ࿏"),
  bstack11llll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࿐"): bstack11llll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ࿑"),
  bstack11llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ࿒"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬ࿓"),
  bstack11llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ࿔"): bstack11llll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨ࿕"),
  bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࿖"): bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨ࿗"),
  bstack11llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࿘"): bstack11llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿙"),
  bstack11llll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ࿚"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫ࿛"),
  bstack11llll_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬ࿜"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨ࿝"),
  bstack11llll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ࿞"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ࿟"),
  bstack11llll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ࿠"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ࿡"),
  bstack11llll_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬ࿢"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࿣"),
  bstack11llll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࿤"): bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࿥"),
  bstack11llll_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪ࿦"): bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪ࿧"),
  bstack11llll_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ࿨"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ࿩"),
  bstack11llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ࿪"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ࿫"),
  bstack11llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࿬"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࿭"),
  bstack11llll_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ࿮"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ࿯"),
  bstack11llll_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ࿰"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ࿱"),
  bstack11llll_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ࿲"): bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨ࿳"),
  bstack11llll_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬ࿴"): bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬ࿵"),
  bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧ࿶"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧ࿷"),
  bstack11llll_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࿸"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࿹"),
  bstack11llll_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࿺"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࿻"),
  bstack11llll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࿼"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࿽"),
  bstack11llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࿾"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࿿"),
  bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬက"): bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩခ"),
  bstack11llll_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧဂ"): bstack11llll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩဃ"),
  bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬင"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭စ"),
  bstack11llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧဆ"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧဇ"),
  bstack11llll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪဈ"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪဉ"),
  bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪည"): bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ဋ"),
  bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨဌ"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨဍ"),
  bstack11llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨဎ"): bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨဏ"),
  bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬတ"): bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬထ"),
  bstack11llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧဒ"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧဓ"),
  bstack11llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪန"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪပ"),
  bstack11llll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ဖ"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ဗ"),
  bstack11llll_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩဘ"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩမ")
}
bstack111ll1l1ll_opy_ = [
  bstack11llll_opy_ (u"࠭࡯ࡴࠩယ"),
  bstack11llll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪရ"),
  bstack11llll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪလ"),
  bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧဝ"),
  bstack11llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧသ"),
  bstack11llll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨဟ"),
  bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬဠ"),
]
bstack11l11ll1l_opy_ = {
  bstack11llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨအ"): [bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨဢ"), bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪဣ")],
  bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬဤ"): bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ဥ"),
  bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧဦ"): bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨဧ"),
  bstack11llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫဨ"): bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬဩ"),
  bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪဪ"): bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫါ"),
  bstack11llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪာ"): bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬိ"),
  bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩီ"): bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫု"),
  bstack11llll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫူ"): bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬေ"),
  bstack11llll_opy_ (u"ࠩࡤࡴࡵ࠭ဲ"): [bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩဳ"), bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧဴ")],
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧဵ"): bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡏࡓࡌࡒࡅࡗࡇࡏࠫံ"),
  bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ့ࠫ"): bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫး"),
  bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ္࠭"): bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟်ࠧ")
}
bstack1l11lllll1_opy_ = {
  bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ျ"): [bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࡡࡱࡥࡲ࡫ࠧြ"), bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧွ")],
  bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪှ"): [bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹ࡟࡬ࡧࡼࠫဿ"), bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ၀")],
  bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭၁"): bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭၂"),
  bstack11llll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ၃"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ၄"),
  bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ၅"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ၆"),
  bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ၇"): [bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡴࡵ࠭၈"), bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ၉")],
  bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ၊"): bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ။"),
  bstack11llll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ၌"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ၍"),
  bstack11llll_opy_ (u"ࠩࡤࡴࡵ࠭၎"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࠭၏"),
  bstack11llll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ၐ"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡧࡍࡧࡹࡩࡱ࠭ၑ"),
  bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪၒ"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪၓ")
}
bstack1l11lll111_opy_ = {
  bstack11llll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫၔ"): bstack11llll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၕ"),
  bstack11llll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬၖ"): [bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၗ"), bstack11llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၘ")],
  bstack11llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫၙ"): bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬၚ"),
  bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬၛ"): bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩၜ"),
  bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨၝ"): [bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬၞ"), bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫၟ")],
  bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧၠ"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩၡ"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬၢ"): bstack11llll_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧၣ"),
  bstack11llll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪၤ"): [bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫၥ"), bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၦ")],
  bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬၧ"): [bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࡳࠨၨ"), bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࠨၩ")]
}
bstack11ll11ll1l_opy_ = [
  bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨၪ"),
  bstack11llll_opy_ (u"ࠪࡴࡦ࡭ࡥࡍࡱࡤࡨࡘࡺࡲࡢࡶࡨ࡫ࡾ࠭ၫ"),
  bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪၬ"),
  bstack11llll_opy_ (u"ࠬࡹࡥࡵ࡙࡬ࡲࡩࡵࡷࡓࡧࡦࡸࠬၭ"),
  bstack11llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨၮ"),
  bstack11llll_opy_ (u"ࠧࡴࡶࡵ࡭ࡨࡺࡆࡪ࡮ࡨࡍࡳࡺࡥࡳࡣࡦࡸࡦࡨࡩ࡭࡫ࡷࡽࠬၯ"),
  bstack11llll_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫၰ"),
  bstack11llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧၱ"),
  bstack11llll_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨၲ"),
  bstack11llll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬၳ"),
  bstack11llll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫၴ"),
  bstack11llll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧၵ"),
]
bstack1ll1l1111l_opy_ = [
  bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫၶ"),
  bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬၷ"),
  bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨၸ"),
  bstack11llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪၹ"),
  bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧၺ"),
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧၻ"),
  bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩၼ"),
  bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫၽ"),
  bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫၾ"),
  bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧၿ"),
  bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧႀ"),
  bstack11llll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ႁ"),
  bstack11llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡙ࡧࡧࠨႂ"),
  bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪႃ"),
  bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩႄ"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬႅ"),
  bstack11llll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠱ࠨႆ"),
  bstack11llll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠳ࠩႇ"),
  bstack11llll_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠵ࠪႈ"),
  bstack11llll_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠷ࠫႉ"),
  bstack11llll_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠹ࠬႊ"),
  bstack11llll_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠻࠭ႋ"),
  bstack11llll_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠽ࠧႌ"),
  bstack11llll_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠸ࠨႍ"),
  bstack11llll_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠺ࠩႎ"),
  bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪႏ"),
  bstack11llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ႐"),
  bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ႑"),
  bstack11llll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ႒")
]
bstack111ll11ll1_opy_ = [
  bstack11llll_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭႓"),
  bstack11llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ႔"),
  bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭႕"),
  bstack11llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ႖"),
  bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫ႗"),
  bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ႘"),
  bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩ႙"),
  bstack11llll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ႚ"),
  bstack11llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫႛ"),
  bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨႜ"),
  bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬႝ"),
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ႞"),
  bstack11llll_opy_ (u"࠭࡯ࡴࠩ႟"),
  bstack11llll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪႠ"),
  bstack11llll_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧႡ"),
  bstack11llll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫႢ"),
  bstack11llll_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪႣ"),
  bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭Ⴄ"),
  bstack11llll_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭Ⴅ"),
  bstack11llll_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪႦ"),
  bstack11llll_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬႧ"),
  bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬႨ"),
  bstack11llll_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨႩ"),
  bstack11llll_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧႪ"),
  bstack11llll_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬႫ"),
  bstack11llll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫႬ"),
  bstack11llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪႭ"),
  bstack11llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨႮ"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬႯ"),
  bstack11llll_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭Ⴐ"),
  bstack11llll_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬႱ"),
  bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ⴒ"),
  bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬႳ"),
  bstack11llll_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬႴ"),
  bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫႵ"),
  bstack11llll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨႶ"),
  bstack11llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ⴗ"),
  bstack11llll_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪࠫႸ"),
  bstack11llll_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵࠪႹ"),
  bstack11llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴࠩႺ"),
  bstack11llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨႻ"),
  bstack11llll_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩႼ"),
  bstack11llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧႽ"),
  bstack11llll_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧႾ"),
  bstack11llll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨႿ"),
  bstack11llll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩჀ"),
  bstack11llll_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪჁ"),
  bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭Ⴢ"),
  bstack11llll_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫჃ"),
  bstack11llll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪჄ"),
  bstack11llll_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪჅ"),
  bstack11llll_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫ჆"),
  bstack11llll_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬჇ"),
  bstack11llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ჈"),
  bstack11llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ჉"),
  bstack11llll_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ჊"),
  bstack11llll_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪ჋"),
  bstack11llll_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ჌"),
  bstack11llll_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨჍ"),
  bstack11llll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬ჎"),
  bstack11llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬ჏"),
  bstack11llll_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࠧა"),
  bstack11llll_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧბ"),
  bstack11llll_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨგ"),
  bstack11llll_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨდ"),
  bstack11llll_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪე"),
  bstack11llll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬვ"),
  bstack11llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨზ"),
  bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࠪთ"),
  bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ი"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࠫკ"),
  bstack11llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ლ"),
  bstack11llll_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪმ"),
  bstack11llll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬნ"),
  bstack11llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬო"),
  bstack11llll_opy_ (u"࠭ࡩࡦࠩპ"),
  bstack11llll_opy_ (u"ࠧࡦࡦࡪࡩࠬჟ"),
  bstack11llll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨრ"),
  bstack11llll_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨს"),
  bstack11llll_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬტ"),
  bstack11llll_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬუ"),
  bstack11llll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫფ"),
  bstack11llll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩქ"),
  bstack11llll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪღ"),
  bstack11llll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬყ"),
  bstack11llll_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩშ"),
  bstack11llll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪჩ"),
  bstack11llll_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ც"),
  bstack11llll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ძ"),
  bstack11llll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩწ"),
  bstack11llll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧჭ"),
  bstack11llll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩხ"),
  bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪჯ"),
  bstack11llll_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨჰ"),
  bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ჱ"),
  bstack11llll_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩჲ"),
  bstack11llll_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬჳ"),
  bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫჴ"),
  bstack11llll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫჵ"),
  bstack11llll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ჶ"),
  bstack11llll_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨჷ"),
  bstack11llll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ჸ"),
  bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧჹ"),
  bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨჺ"),
  bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭჻"),
  bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪჼ"),
  bstack11llll_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬჽ"),
  bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩჾ"),
  bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ჿ"),
  bstack11llll_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᄀ")
]
bstack1ll1111ll_opy_ = {
  bstack11llll_opy_ (u"࠭ࡶࠨᄁ"): bstack11llll_opy_ (u"ࠧࡷࠩᄂ"),
  bstack11llll_opy_ (u"ࠨࡨࠪᄃ"): bstack11llll_opy_ (u"ࠩࡩࠫᄄ"),
  bstack11llll_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩᄅ"): bstack11llll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪᄆ"),
  bstack11llll_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᄇ"): bstack11llll_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬᄈ"),
  bstack11llll_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫᄉ"): bstack11llll_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬᄊ"),
  bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬᄋ"): bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᄌ"),
  bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧᄍ"): bstack11llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᄎ"),
  bstack11llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩᄏ"): bstack11llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᄐ"),
  bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᄑ"): bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᄒ"),
  bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫᄓ"): bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬᄔ"),
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ᄕ"): bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᄖ"),
  bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᄗ"): bstack11llll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᄘ"),
  bstack11llll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᄙ"): bstack11llll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᄚ"),
  bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᄛ"): bstack11llll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᄜ"),
  bstack11llll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᄝ"): bstack11llll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᄞ"),
  bstack11llll_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬᄟ"): bstack11llll_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ᄠ"),
  bstack11llll_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫᄡ"): bstack11llll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᄢ"),
  bstack11llll_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᄣ"): bstack11llll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᄤ"),
  bstack11llll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᄥ"): bstack11llll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄦ"),
  bstack11llll_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪᄧ"): bstack11llll_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫᄨ"),
  bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᄩ"): bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᄪ"),
}
bstack111ll1llll_opy_ = bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡨ࡫ࡷ࡬ࡺࡨ࠮ࡤࡱࡰ࠳ࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯࠯ࡳࡧ࡯ࡩࡦࡹࡥࡴ࠱࡯ࡥࡹ࡫ࡳࡵ࠱ࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᄫ")
bstack111ll11l1l_opy_ = bstack11llll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠯ࡩࡧࡤࡰࡹ࡮ࡣࡩࡧࡦ࡯ࠧᄬ")
bstack1lll1ll111_opy_ = bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩᄭ")
bstack1111111l1_opy_ = bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬᄮ")
bstack11l1l1l111_opy_ = bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡭ࡻࡢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹࠧᄯ")
bstack111ll11l11_opy_ = {
  bstack11llll_opy_ (u"ࠫࡨࡸࡩࡵ࡫ࡦࡥࡱ࠭ᄰ"): 50,
  bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᄱ"): 40,
  bstack11llll_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᄲ"): 30,
  bstack11llll_opy_ (u"ࠧࡪࡰࡩࡳࠬᄳ"): 20,
  bstack11llll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᄴ"): 10
}
bstack11l111l1l_opy_ = bstack111ll11l11_opy_[bstack11llll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᄵ")]
bstack1llll1l11l_opy_ = bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᄶ")
bstack111l1l11l_opy_ = bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᄷ")
bstack1l1l1ll11_opy_ = bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫᄸ")
bstack1lll111l1_opy_ = bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᄹ")
bstack1111l11l_opy_ = bstack11llll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬᄺ")
bstack111lll111l_opy_ = [bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᄻ"), bstack11llll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩᄼ")]
bstack111ll1l11l_opy_ = [bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᄽ"), bstack11llll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ᄾ")]
bstack1l11l11111_opy_ = re.compile(bstack11llll_opy_ (u"ࠬࡤ࡛࡝࡞ࡺ࠱ࡢ࠱࠺࠯ࠬࠧࠫᄿ"))
bstack1l1lllll1_opy_ = [
  bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡑࡥࡲ࡫ࠧᅀ"),
  bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᅁ"),
  bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᅂ"),
  bstack11llll_opy_ (u"ࠩࡱࡩࡼࡉ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅃ"),
  bstack11llll_opy_ (u"ࠪࡥࡵࡶࠧᅄ"),
  bstack11llll_opy_ (u"ࠫࡺࡪࡩࡥࠩᅅ"),
  bstack11llll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᅆ"),
  bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࠭ᅇ"),
  bstack11llll_opy_ (u"ࠧࡰࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬᅈ"),
  bstack11llll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࠭ᅉ"),
  bstack11llll_opy_ (u"ࠩࡱࡳࡗ࡫ࡳࡦࡶࠪᅊ"), bstack11llll_opy_ (u"ࠪࡪࡺࡲ࡬ࡓࡧࡶࡩࡹ࠭ᅋ"),
  bstack11llll_opy_ (u"ࠫࡨࡲࡥࡢࡴࡖࡽࡸࡺࡥ࡮ࡈ࡬ࡰࡪࡹࠧᅌ"),
  bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡘ࡮ࡳࡩ࡯ࡩࡶࠫᅍ"),
  bstack11llll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࡏࡳ࡬࡭ࡩ࡯ࡩࠪᅎ"),
  bstack11llll_opy_ (u"ࠧࡰࡶ࡫ࡩࡷࡇࡰࡱࡵࠪᅏ"),
  bstack11llll_opy_ (u"ࠨࡲࡵ࡭ࡳࡺࡐࡢࡩࡨࡗࡴࡻࡲࡤࡧࡒࡲࡋ࡯࡮ࡥࡈࡤ࡭ࡱࡻࡲࡦࠩᅐ"),
  bstack11llll_opy_ (u"ࠩࡤࡴࡵࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧᅑ"), bstack11llll_opy_ (u"ࠪࡥࡵࡶࡐࡢࡥ࡮ࡥ࡬࡫ࠧᅒ"), bstack11llll_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡆࡩࡴࡪࡸ࡬ࡸࡾ࠭ᅓ"), bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡖࡡࡤ࡭ࡤ࡫ࡪ࠭ᅔ"), bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᅕ"),
  bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᅖ"),
  bstack11llll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡔࡦࡵࡷࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᅗ"),
  bstack11llll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡆࡳࡻ࡫ࡲࡢࡩࡨࠫᅘ"), bstack11llll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࡊࡴࡤࡊࡰࡷࡩࡳࡺࠧᅙ"),
  bstack11llll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᅚ"),
  bstack11llll_opy_ (u"ࠬࡧࡤࡣࡒࡲࡶࡹ࠭ᅛ"),
  bstack11llll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪ࡙࡯ࡤ࡭ࡨࡸࠬᅜ"),
  bstack11llll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡊࡰࡶࡸࡦࡲ࡬ࡕ࡫ࡰࡩࡴࡻࡴࠨᅝ"),
  bstack11llll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡸ࡭࠭ᅞ"),
  bstack11llll_opy_ (u"ࠩࡤࡺࡩ࠭ᅟ"), bstack11llll_opy_ (u"ࠪࡥࡻࡪࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅠ"), bstack11llll_opy_ (u"ࠫࡦࡼࡤࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅡ"), bstack11llll_opy_ (u"ࠬࡧࡶࡥࡃࡵ࡫ࡸ࠭ᅢ"),
  bstack11llll_opy_ (u"࠭ࡵࡴࡧࡎࡩࡾࡹࡴࡰࡴࡨࠫᅣ"), bstack11llll_opy_ (u"ࠧ࡬ࡧࡼࡷࡹࡵࡲࡦࡒࡤࡸ࡭࠭ᅤ"), bstack11llll_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡸࡹࡷࡰࡴࡧࠫᅥ"),
  bstack11llll_opy_ (u"ࠩ࡮ࡩࡾࡇ࡬ࡪࡣࡶࠫᅦ"), bstack11llll_opy_ (u"ࠪ࡯ࡪࡿࡐࡢࡵࡶࡻࡴࡸࡤࠨᅧ"),
  bstack11llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ᅨ"), bstack11llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡅࡷ࡭ࡳࠨᅩ"), bstack11llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࡅ࡫ࡵࠫᅪ"), bstack11llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡉࡨࡳࡱࡰࡩࡒࡧࡰࡱ࡫ࡱ࡫ࡋ࡯࡬ࡦࠩᅫ"), bstack11llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡕࡴࡧࡖࡽࡸࡺࡥ࡮ࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࠬᅬ"),
  bstack11llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡑࡱࡵࡸࠬᅭ"), bstack11llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹࡹࠧᅮ"),
  bstack11llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡇ࡭ࡸࡧࡢ࡭ࡧࡅࡹ࡮ࡲࡤࡄࡪࡨࡧࡰ࠭ᅯ"),
  bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅰ"),
  bstack11llll_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡇࡣࡵ࡫ࡲࡲࠬᅱ"), bstack11llll_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡃࡢࡶࡨ࡫ࡴࡸࡹࠨᅲ"), bstack11llll_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡇ࡮ࡤ࡫ࡸ࠭ᅳ"), bstack11llll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡣ࡯ࡍࡳࡺࡥ࡯ࡶࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᅴ"),
  bstack11llll_opy_ (u"ࠪࡨࡴࡴࡴࡔࡶࡲࡴࡆࡶࡰࡐࡰࡕࡩࡸ࡫ࡴࠨᅵ"),
  bstack11llll_opy_ (u"ࠫࡺࡴࡩࡤࡱࡧࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᅶ"), bstack11llll_opy_ (u"ࠬࡸࡥࡴࡧࡷࡏࡪࡿࡢࡰࡣࡵࡨࠬᅷ"),
  bstack11llll_opy_ (u"࠭࡮ࡰࡕ࡬࡫ࡳ࠭ᅸ"),
  bstack11llll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡕ࡯࡫ࡰࡴࡴࡸࡴࡢࡰࡷ࡚࡮࡫ࡷࡴࠩᅹ"),
  bstack11llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱࡨࡷࡵࡩࡥ࡙ࡤࡸࡨ࡮ࡥࡳࡵࠪᅺ"),
  bstack11llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅻ"),
  bstack11llll_opy_ (u"ࠪࡶࡪࡩࡲࡦࡣࡷࡩࡈ࡮ࡲࡰ࡯ࡨࡈࡷ࡯ࡶࡦࡴࡖࡩࡸࡹࡩࡰࡰࡶࠫᅼ"),
  bstack11llll_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᅽ"),
  bstack11llll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡒࡤࡸ࡭࠭ᅾ"),
  bstack11llll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡓࡱࡧࡨࡨࠬᅿ"),
  bstack11llll_opy_ (u"ࠧࡨࡲࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᆀ"),
  bstack11llll_opy_ (u"ࠨ࡫ࡶࡌࡪࡧࡤ࡭ࡧࡶࡷࠬᆁ"),
  bstack11llll_opy_ (u"ࠩࡤࡨࡧࡋࡸࡦࡥࡗ࡭ࡲ࡫࡯ࡶࡶࠪᆂ"),
  bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࡖࡧࡷ࡯ࡰࡵࠩᆃ"),
  bstack11llll_opy_ (u"ࠫࡸࡱࡩࡱࡆࡨࡺ࡮ࡩࡥࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨᆄ"),
  bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡊࡶࡦࡴࡴࡑࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠬᆅ"),
  bstack11llll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡎࡢࡶࡸࡶࡦࡲࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫᆆ"),
  bstack11llll_opy_ (u"ࠧࡴࡻࡶࡸࡪࡳࡐࡰࡴࡷࠫᆇ"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡦࡥࡌࡴࡹࡴࠨᆈ"),
  bstack11llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡕ࡯࡮ࡲࡧࡰ࠭ᆉ"), bstack11llll_opy_ (u"ࠪࡹࡳࡲ࡯ࡤ࡭ࡗࡽࡵ࡫ࠧᆊ"), bstack11llll_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡏࡪࡿࠧᆋ"),
  bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡏࡥࡺࡴࡣࡩࠩᆌ"),
  bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡣࡢࡶࡆࡥࡵࡺࡵࡳࡧࠪᆍ"),
  bstack11llll_opy_ (u"ࠧࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࡒࡸ࡭࡫ࡲࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᆎ"),
  bstack11llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦ࡙࡬ࡲࡩࡵࡷࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࠪᆏ"),
  bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡱࡲࡰࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᆐ"),
  bstack11llll_opy_ (u"ࠪࡩࡳ࡬࡯ࡳࡥࡨࡅࡵࡶࡉ࡯ࡵࡷࡥࡱࡲࠧᆑ"),
  bstack11llll_opy_ (u"ࠫࡪࡴࡳࡶࡴࡨ࡛ࡪࡨࡶࡪࡧࡺࡷࡍࡧࡶࡦࡒࡤ࡫ࡪࡹࠧᆒ"), bstack11llll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡊࡥࡷࡶࡲࡳࡱࡹࡐࡰࡴࡷࠫᆓ"), bstack11llll_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡊࡥࡵࡣ࡬ࡰࡸࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠩᆔ"),
  bstack11llll_opy_ (u"ࠧࡳࡧࡰࡳࡹ࡫ࡁࡱࡲࡶࡇࡦࡩࡨࡦࡎ࡬ࡱ࡮ࡺࠧᆕ"),
  bstack11llll_opy_ (u"ࠨࡥࡤࡰࡪࡴࡤࡢࡴࡉࡳࡷࡳࡡࡵࠩᆖ"),
  bstack11llll_opy_ (u"ࠩࡥࡹࡳࡪ࡬ࡦࡋࡧࠫᆗ"),
  bstack11llll_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᆘ"),
  bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࡙ࡥࡳࡸ࡬ࡧࡪࡹࡅ࡯ࡣࡥࡰࡪࡪࠧᆙ"), bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡂࡷࡷ࡬ࡴࡸࡩࡻࡧࡧࠫᆚ"),
  bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡅࡨࡩࡥࡱࡶࡄࡰࡪࡸࡴࡴࠩᆛ"), bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡉ࡯ࡳ࡮࡫ࡶࡷࡆࡲࡥࡳࡶࡶࠫᆜ"),
  bstack11llll_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡊࡰࡶࡸࡷࡻ࡭ࡦࡰࡷࡷࡑ࡯ࡢࠨᆝ"),
  bstack11llll_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦ࡙ࡧࡰࠨᆞ"),
  bstack11llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌࡲ࡮ࡺࡩࡢ࡮ࡘࡶࡱ࠭ᆟ"), bstack11llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡅࡱࡲ࡯ࡸࡒࡲࡴࡺࡶࡳࠨᆠ"), bstack11llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎ࡭࡮ࡰࡴࡨࡊࡷࡧࡵࡥ࡙ࡤࡶࡳ࡯࡮ࡨࠩᆡ"), bstack11llll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡦࡰࡏ࡭ࡳࡱࡳࡊࡰࡅࡥࡨࡱࡧࡳࡱࡸࡲࡩ࠭ᆢ"),
  bstack11llll_opy_ (u"ࠧ࡬ࡧࡨࡴࡐ࡫ࡹࡄࡪࡤ࡭ࡳࡹࠧᆣ"),
  bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡻࡣࡥࡰࡪ࡙ࡴࡳ࡫ࡱ࡫ࡸࡊࡩࡳࠩᆤ"),
  bstack11llll_opy_ (u"ࠩࡳࡶࡴࡩࡥࡴࡵࡄࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᆥ"),
  bstack11llll_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡍࡨࡽࡉ࡫࡬ࡢࡻࠪᆦ"),
  bstack11llll_opy_ (u"ࠫࡸ࡮࡯ࡸࡋࡒࡗࡑࡵࡧࠨᆧ"),
  bstack11llll_opy_ (u"ࠬࡹࡥ࡯ࡦࡎࡩࡾ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧᆨ"),
  bstack11llll_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡘࡥࡴࡲࡲࡲࡸ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᆩ"), bstack11llll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷ࡛ࡦ࡯ࡴࡕ࡫ࡰࡩࡴࡻࡴࠨᆪ"),
  bstack11llll_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࠫᆫ"),
  bstack11llll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡶࡽࡳࡩࡅࡹࡧࡦࡹࡹ࡫ࡆࡳࡱࡰࡌࡹࡺࡰࡴࠩᆬ"),
  bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡇࡦࡶࡴࡶࡴࡨࠫᆭ"),
  bstack11llll_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫᆮ"),
  bstack11llll_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡆࡳࡳࡺࡥࡹࡶࡏ࡭ࡸࡺࠧᆯ"),
  bstack11llll_opy_ (u"࠭ࡷࡢ࡫ࡷࡊࡴࡸࡁࡱࡲࡖࡧࡷ࡯ࡰࡵࠩᆰ"),
  bstack11llll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡄࡱࡱࡲࡪࡩࡴࡓࡧࡷࡶ࡮࡫ࡳࠨᆱ"),
  bstack11llll_opy_ (u"ࠨࡣࡳࡴࡓࡧ࡭ࡦࠩᆲ"),
  bstack11llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡖࡐࡈ࡫ࡲࡵࠩᆳ"),
  bstack11llll_opy_ (u"ࠪࡸࡦࡶࡗࡪࡶ࡫ࡗ࡭ࡵࡲࡵࡒࡵࡩࡸࡹࡄࡶࡴࡤࡸ࡮ࡵ࡮ࠨᆴ"),
  bstack11llll_opy_ (u"ࠫࡸࡩࡡ࡭ࡧࡉࡥࡨࡺ࡯ࡳࠩᆵ"),
  bstack11llll_opy_ (u"ࠬࡽࡤࡢࡎࡲࡧࡦࡲࡐࡰࡴࡷࠫᆶ"),
  bstack11llll_opy_ (u"࠭ࡳࡩࡱࡺ࡜ࡨࡵࡤࡦࡎࡲ࡫ࠬᆷ"),
  bstack11llll_opy_ (u"ࠧࡪࡱࡶࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡻࡳࡦࠩᆸ"),
  bstack11llll_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠪᆹ"),
  bstack11llll_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡹࡳࡸࡱࡵࡨࠬᆺ"),
  bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡐࡳࡧࡥࡹ࡮ࡲࡴࡘࡆࡄࠫᆻ"),
  bstack11llll_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸ࡜ࡊࡁࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠬᆼ"),
  bstack11llll_opy_ (u"ࠬࡽࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡂࡩࡨࡲࡹ࡛ࡲ࡭ࠩᆽ"),
  bstack11llll_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡷ࡬ࠬᆾ"),
  bstack11llll_opy_ (u"ࠧࡶࡵࡨࡒࡪࡽࡗࡅࡃࠪᆿ"),
  bstack11llll_opy_ (u"ࠨࡹࡧࡥࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫᇀ"), bstack11llll_opy_ (u"ࠩࡺࡨࡦࡉ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࡖ࡬ࡱࡪࡵࡵࡵࠩᇁ"),
  bstack11llll_opy_ (u"ࠪࡼࡨࡵࡤࡦࡑࡵ࡫ࡎࡪࠧᇂ"), bstack11llll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡖ࡭࡬ࡴࡩ࡯ࡩࡌࡨࠬᇃ"),
  bstack11llll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩ࡝ࡄࡂࡄࡸࡲࡩࡲࡥࡊࡦࠪᇄ"),
  bstack11llll_opy_ (u"࠭ࡲࡦࡵࡨࡸࡔࡴࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡵࡸࡔࡴ࡬ࡺࠩᇅ"),
  bstack11llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࡴࠩᇆ"),
  bstack11llll_opy_ (u"ࠨࡹࡧࡥࡘࡺࡡࡳࡶࡸࡴࡗ࡫ࡴࡳ࡫ࡨࡷࠬᇇ"), bstack11llll_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴࡼࡍࡳࡺࡥࡳࡸࡤࡰࠬᇈ"),
  bstack11llll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࡌࡦࡸࡤࡸࡣࡵࡩࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ᇉ"),
  bstack11llll_opy_ (u"ࠫࡲࡧࡸࡕࡻࡳ࡭ࡳ࡭ࡆࡳࡧࡴࡹࡪࡴࡣࡺࠩᇊ"),
  bstack11llll_opy_ (u"ࠬࡹࡩ࡮ࡲ࡯ࡩࡎࡹࡖࡪࡵ࡬ࡦࡱ࡫ࡃࡩࡧࡦ࡯ࠬᇋ"),
  bstack11llll_opy_ (u"࠭ࡵࡴࡧࡆࡥࡷࡺࡨࡢࡩࡨࡗࡸࡲࠧᇌ"),
  bstack11llll_opy_ (u"ࠧࡴࡪࡲࡹࡱࡪࡕࡴࡧࡖ࡭ࡳ࡭࡬ࡦࡶࡲࡲ࡙࡫ࡳࡵࡏࡤࡲࡦ࡭ࡥࡳࠩᇍ"),
  bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡉࡘࡆࡓࠫᇎ"),
  bstack11llll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡱࡸࡧ࡭ࡏࡤࡆࡰࡵࡳࡱࡲࠧᇏ"),
  bstack11llll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡋ࡭ࡩࡪࡥ࡯ࡃࡳ࡭ࡕࡵ࡬ࡪࡥࡼࡉࡷࡸ࡯ࡳࠩᇐ"),
  bstack11llll_opy_ (u"ࠫࡲࡵࡣ࡬ࡎࡲࡧࡦࡺࡩࡰࡰࡄࡴࡵ࠭ᇑ"),
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡥࡤࡸࡋࡵࡲ࡮ࡣࡷࠫᇒ"), bstack11llll_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌࡩ࡭ࡶࡨࡶࡘࡶࡥࡤࡵࠪᇓ"),
  bstack11llll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡊࡥ࡭ࡣࡼࡅࡩࡨࠧᇔ"),
  bstack11llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡋࡧࡐࡴࡩࡡࡵࡱࡵࡅࡺࡺ࡯ࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠫᇕ")
]
bstack1l1l1ll111_opy_ = bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨᇖ")
bstack1lllll1ll1_opy_ = [bstack11llll_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨᇗ"), bstack11llll_opy_ (u"ࠫ࠳ࡧࡡࡣࠩᇘ"), bstack11llll_opy_ (u"ࠬ࠴ࡩࡱࡣࠪᇙ")]
bstack1lll1lll11_opy_ = [bstack11llll_opy_ (u"࠭ࡩࡥࠩᇚ"), bstack11llll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᇛ"), bstack11llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫᇜ"), bstack11llll_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨᇝ")]
bstack1l1lll11l_opy_ = {
  bstack11llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᇞ"): bstack11llll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇟ"),
  bstack11llll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇠ"): bstack11llll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᇡ"),
  bstack11llll_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬᇢ"): bstack11llll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇣ"),
  bstack11llll_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᇤ"): bstack11llll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇥ"),
  bstack11llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫᇦ"): bstack11llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᇧ")
}
bstack11111111l_opy_ = [
  bstack11llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᇨ"),
  bstack11llll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᇩ"),
  bstack11llll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇪ"),
  bstack11llll_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᇫ"),
  bstack11llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᇬ"),
]
bstack1l11l1ll11_opy_ = bstack1ll1l1111l_opy_ + bstack111ll11ll1_opy_ + bstack1l1lllll1_opy_
bstack1l111l111_opy_ = [
  bstack11llll_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩᇭ"),
  bstack11llll_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭ᇮ"),
  bstack11llll_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬᇯ"),
  bstack11llll_opy_ (u"ࠧ࡟࠳࠳࠲ࠬᇰ"),
  bstack11llll_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧᇱ"),
  bstack11llll_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨᇲ"),
  bstack11llll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩᇳ"),
  bstack11llll_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧᇴ")
]
bstack111ll1l1l1_opy_ = bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᇵ")
bstack1l111l11l1_opy_ = bstack11llll_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬᇶ")
bstack1l1l11l1l_opy_ = [ bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᇷ") ]
bstack111l11l1l_opy_ = [ bstack11llll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᇸ") ]
bstack1l11lllll_opy_ = [ bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᇹ") ]
bstack11l1ll1ll1_opy_ = bstack11llll_opy_ (u"ࠪࡗࡉࡑࡓࡦࡶࡸࡴࠬᇺ")
bstack11ll1lll1l_opy_ = bstack11llll_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧᇻ")
bstack11ll111ll_opy_ = bstack11llll_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹ࡙ࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠩᇼ")
bstack1llll1111l_opy_ = bstack11llll_opy_ (u"࠭࠴࠯࠲࠱࠴ࠬᇽ")
bstack1lll11l1l_opy_ = [
  bstack11llll_opy_ (u"ࠧࡆࡔࡕࡣࡋࡇࡉࡍࡇࡇࠫᇾ"),
  bstack11llll_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨᇿ"),
  bstack11llll_opy_ (u"ࠩࡈࡖࡗࡥࡂࡍࡑࡆࡏࡊࡊ࡟ࡃ࡛ࡢࡇࡑࡏࡅࡏࡖࠪሀ"),
  bstack11llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡇࡗ࡛ࡔࡘࡋࡠࡅࡋࡅࡓࡍࡅࡅࠩሁ"),
  bstack11llll_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐࡋࡔࡠࡐࡒࡘࡤࡉࡏࡏࡐࡈࡇ࡙ࡋࡄࠨሂ"),
  bstack11llll_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡃࡍࡑࡖࡉࡉ࠭ሃ"),
  bstack11llll_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡖࡉ࡙࠭ሄ"),
  bstack11llll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡔࡈࡊ࡚࡙ࡅࡅࠩህ"),
  bstack11llll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡄࡆࡔࡘࡔࡆࡆࠪሆ"),
  bstack11llll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪሇ"),
  bstack11llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫለ"),
  bstack11llll_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡌࡒ࡛ࡇࡌࡊࡆࠪሉ"),
  bstack11llll_opy_ (u"ࠬࡋࡒࡓࡡࡄࡈࡉࡘࡅࡔࡕࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨሊ"),
  bstack11llll_opy_ (u"࠭ࡅࡓࡔࡢࡘ࡚ࡔࡎࡆࡎࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧላ"),
  bstack11llll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫሌ"),
  bstack11llll_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨል"),
  bstack11llll_opy_ (u"ࠩࡈࡖࡗࡥࡓࡐࡅࡎࡗࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡋࡓࡘ࡚࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬሎ"),
  bstack11llll_opy_ (u"ࠪࡉࡗࡘ࡟ࡑࡔࡒ࡜࡞ࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪሏ"),
  bstack11llll_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬሐ"),
  bstack11llll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡓࡇࡖࡓࡑ࡛ࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫሑ"),
  bstack11llll_opy_ (u"࠭ࡅࡓࡔࡢࡑࡆࡔࡄࡂࡖࡒࡖ࡞ࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬሒ"),
]
bstack1ll11lll11_opy_ = bstack11llll_opy_ (u"ࠧ࠯࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡣࡵࡸ࡮࡬ࡡࡤࡶࡶ࠳ࠬሓ")
bstack1ll1l1ll11_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪሔ")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩሕ"), bstack11llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩሖ"))
bstack11l111l1ll_opy_ = bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡳ࡭ࠬሗ")
bstack111ll1ll11_opy_ = [ bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬመ"), bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬሙ"), bstack11llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ሚ"), bstack11llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨማ")]
bstack1lllll1l1l_opy_ = [ bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩሜ"), bstack11llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩም"), bstack11llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪሞ"), bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬሟ") ]
bstack1l11l111_opy_ = {
  bstack11llll_opy_ (u"࠭ࡐࡂࡕࡖࠫሠ"): bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧሡ"),
  bstack11llll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ሢ"): bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩሣ"),
  bstack11llll_opy_ (u"ࠪࡗࡐࡏࡐࠨሤ"): bstack11llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬሥ")
}
bstack1l1111l11_opy_ = [
  bstack11llll_opy_ (u"ࠧ࡭ࡥࡵࠤሦ"),
  bstack11llll_opy_ (u"ࠨࡧࡰࡄࡤࡧࡰࠨሧ"),
  bstack11llll_opy_ (u"ࠢࡨࡱࡉࡳࡷࡽࡡࡳࡦࠥረ"),
  bstack11llll_opy_ (u"ࠣࡴࡨࡪࡷ࡫ࡳࡩࠤሩ"),
  bstack11llll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣሪ"),
  bstack11llll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢራ"),
  bstack11llll_opy_ (u"ࠦࡸࡻࡢ࡮࡫ࡷࡉࡱ࡫࡭ࡦࡰࡷࠦሬ"),
  bstack11llll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤር"),
  bstack11llll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤሮ"),
  bstack11llll_opy_ (u"ࠢࡤ࡮ࡨࡥࡷࡋ࡬ࡦ࡯ࡨࡲࡹࠨሯ"),
  bstack11llll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࡴࠤሰ"),
  bstack11llll_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠤሱ"),
  bstack11llll_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࡅࡸࡿ࡮ࡤࡕࡦࡶ࡮ࡶࡴࠣሲ"),
  bstack11llll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥሳ"),
  bstack11llll_opy_ (u"ࠧࡷࡵࡪࡶࠥሴ"),
  bstack11llll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡔࡰࡷࡦ࡬ࡆࡩࡴࡪࡱࡱࠦስ"),
  bstack11llll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡎࡷ࡯ࡸ࡮࡚࡯ࡶࡥ࡫ࠦሶ"),
  bstack11llll_opy_ (u"ࠣࡵ࡫ࡥࡰ࡫ࠢሷ"),
  bstack11llll_opy_ (u"ࠤࡦࡰࡴࡹࡥࡂࡲࡳࠦሸ")
]
bstack111ll1lll1_opy_ = [
  bstack11llll_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࠤሹ"),
  bstack11llll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣሺ"),
  bstack11llll_opy_ (u"ࠧࡧࡵࡵࡱࠥሻ"),
  bstack11llll_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨሼ"),
  bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤሽ")
]
bstack1l111lllll_opy_ = {
  bstack11llll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢሾ"): [bstack11llll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣሿ")],
  bstack11llll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢቀ"): [bstack11llll_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣቁ")],
  bstack11llll_opy_ (u"ࠧࡧࡵࡵࡱࠥቂ"): [bstack11llll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡈࡰࡪࡳࡥ࡯ࡶࠥቃ"), bstack11llll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡅࡨࡺࡩࡷࡧࡈࡰࡪࡳࡥ࡯ࡶࠥቄ"), bstack11llll_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧቅ"), bstack11llll_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࡆ࡮ࡨࡱࡪࡴࡴࠣቆ")],
  bstack11llll_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥቇ"): [bstack11llll_opy_ (u"ࠦࡲࡧ࡮ࡶࡣ࡯ࠦቈ")],
  bstack11llll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ቉"): [bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣቊ")],
}
bstack111lll1111_opy_ = {
  bstack11llll_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࡋ࡬ࡦ࡯ࡨࡲࡹࠨቋ"): bstack11llll_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࠢቌ"),
  bstack11llll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨቍ"): bstack11llll_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ቎"),
  bstack11llll_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣ቏"): bstack11llll_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࠢቐ"),
  bstack11llll_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤቑ"): bstack11llll_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࠤቒ"),
  bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥቓ"): bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦቔ")
}
bstack11l1111l_opy_ = {
  bstack11llll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧቕ"): bstack11llll_opy_ (u"ࠫࡘࡻࡩࡵࡧࠣࡗࡪࡺࡵࡱࠩቖ"),
  bstack11llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ቗"): bstack11llll_opy_ (u"࠭ࡓࡶ࡫ࡷࡩ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧቘ"),
  bstack11llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ቙"): bstack11llll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡓࡦࡶࡸࡴࠬቚ"),
  bstack11llll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ቛ"): bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪቜ")
}
bstack1l1l1ll1_opy_ = {
  bstack11llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨቝ"): bstack11llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ቞"),
  bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ቟"): bstack11llll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪበ"),
  bstack11llll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩቡ"): bstack11llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡉࡉࡆ࡚ࡕࡓࡇࠪቢ"),
  bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪባ"): bstack11llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡊࡊࡇࡔࡖࡔࡈࠫቤ"),
  bstack11llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩብ"): bstack11llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡔࡂࡉࠪቦ"),
  bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪቧ"): bstack11llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡕࡃࡊࠫቨ"),
  bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫቩ"): bstack11llll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨቪ"),
  bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬቫ"): bstack11llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩቬ"),
  bstack11llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠫቭ"): bstack11llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡔࡖࡈࡔࠬቮ"),
  bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬቯ"): bstack11llll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡕࡗࡉࡕ࠭ተ")
}
bstack111ll11lll_opy_ = 65536
bstack111ll1l111_opy_ = bstack11llll_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫቱ")
bstack111ll1ll1l_opy_ = [
      bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ቲ"), bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨታ"), bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩቴ"), bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫት"), bstack11llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪቶ"),
      bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬቷ"), bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ቸ"), bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬቹ"), bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ቺ"),
      bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧቻ"), bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩቼ"), bstack11llll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫች")
    ]
bstack111lll11l1_opy_= {
  bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ቾ"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧቿ"),
  bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨኀ"): bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩኁ"),
  bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬኂ"): bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫኃ"),
  bstack11llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨኄ"): bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩኅ"),
  bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ኆ"): bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧኇ"),
  bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧኈ"): bstack11llll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ኉"),
  bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪኊ"): bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫኋ"),
  bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ኌ"): bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧኍ"),
  bstack11llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ኎"): bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ኏"),
  bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫነ"): bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬኑ"),
  bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬኒ"): bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ና"),
  bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧኔ"): bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨን"),
  bstack11llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧኖ"): bstack11llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨኗ"),
  bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኘ"): bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪኙ"),
  bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫኚ"): bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬኛ"),
  bstack11llll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨኜ"): bstack11llll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩኝ"),
  bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬኞ"): bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ኟ"),
  bstack11llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧአ"): bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨኡ"),
  bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ኢ"): bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧኣ"),
  bstack11llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧኤ"): bstack11llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨእ"),
  bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧኦ"): bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨኧ"),
  bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩከ"): bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪኩ"),
  bstack11llll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨኪ"): bstack11llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩካ"),
  bstack11llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪኬ"): bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫክ"),
  bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨኮ"): bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩኯ")
}