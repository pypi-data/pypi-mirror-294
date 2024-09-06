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
class bstack111llllll1_opy_(object):
  bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"࠭ࡾࠨྣ")), bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧྤ"))
  bstack111llll1l1_opy_ = os.path.join(bstack1lll1llll1_opy_, bstack11llll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨྥ"))
  bstack111lllll11_opy_ = None
  perform_scan = None
  bstack1l1llll1ll_opy_ = None
  bstack11l11llll_opy_ = None
  bstack11l111lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11llll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫྦ")):
      cls.instance = super(bstack111llllll1_opy_, cls).__new__(cls)
      cls.instance.bstack111lllll1l_opy_()
    return cls.instance
  def bstack111lllll1l_opy_(self):
    try:
      with open(self.bstack111llll1l1_opy_, bstack11llll_opy_ (u"ࠪࡶࠬྦྷ")) as bstack1ll1l11111_opy_:
        bstack111llll1ll_opy_ = bstack1ll1l11111_opy_.read()
        data = json.loads(bstack111llll1ll_opy_)
        if bstack11llll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ྨ") in data:
          self.bstack11l111ll1l_opy_(data[bstack11llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧྩ")])
        if bstack11llll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧྪ") in data:
          self.bstack11l1111l11_opy_(data[bstack11llll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨྫ")])
    except:
      pass
  def bstack11l1111l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11llll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ྫྷ")]
      self.bstack1l1llll1ll_opy_ = scripts[bstack11llll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ྭ")]
      self.bstack11l11llll_opy_ = scripts[bstack11llll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧྮ")]
      self.bstack11l111lll1_opy_ = scripts[bstack11llll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩྯ")]
  def bstack11l111ll1l_opy_(self, bstack111lllll11_opy_):
    if bstack111lllll11_opy_ != None and len(bstack111lllll11_opy_) != 0:
      self.bstack111lllll11_opy_ = bstack111lllll11_opy_
  def store(self):
    try:
      with open(self.bstack111llll1l1_opy_, bstack11llll_opy_ (u"ࠬࡽࠧྰ")) as file:
        json.dump({
          bstack11llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣྱ"): self.bstack111lllll11_opy_,
          bstack11llll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣྲ"): {
            bstack11llll_opy_ (u"ࠣࡵࡦࡥࡳࠨླ"): self.perform_scan,
            bstack11llll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨྴ"): self.bstack1l1llll1ll_opy_,
            bstack11llll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢྵ"): self.bstack11l11llll_opy_,
            bstack11llll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤྶ"): self.bstack11l111lll1_opy_
          }
        }, file)
    except:
      pass
  def bstack1l1l11ll1l_opy_(self, bstack111llll11l_opy_):
    try:
      return any(command.get(bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪྷ")) == bstack111llll11l_opy_ for command in self.bstack111lllll11_opy_)
    except:
      return False
bstack1lll11ll11_opy_ = bstack111llllll1_opy_()