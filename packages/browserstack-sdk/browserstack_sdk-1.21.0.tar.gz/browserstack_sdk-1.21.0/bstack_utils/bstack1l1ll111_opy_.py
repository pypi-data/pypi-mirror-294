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
from uuid import uuid4
from bstack_utils.helper import bstack1l1lll1l_opy_, bstack1111l1ll11_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack1lll1l1111l_opy_
class bstack11lllll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1ll11l1l_opy_=None, framework=None, tags=[], scope=[], bstack1ll1lll1lll_opy_=None, bstack1ll1llllll1_opy_=True, bstack1ll1lll11ll_opy_=None, bstack11l1l1lll_opy_=None, result=None, duration=None, bstack1l111111_opy_=None, meta={}):
        self.bstack1l111111_opy_ = bstack1l111111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1llllll1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lll1lll_opy_ = bstack1ll1lll1lll_opy_
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.bstack11l1l1lll_opy_ = bstack11l1l1lll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l11lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1l1lllll_opy_(self, meta):
        self.meta = meta
    def bstack1lll1111111_opy_(self):
        bstack1ll1llll11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᘍ"): bstack1ll1llll11l_opy_,
            bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᘎ"): bstack1ll1llll11l_opy_,
            bstack11llll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᘏ"): bstack1ll1llll11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11llll_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᘐ") + key)
            setattr(self, key, val)
    def bstack1ll1lllllll_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘑ"): self.name,
            bstack11llll_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᘒ"): {
                bstack11llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᘓ"): bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᘔ"),
                bstack11llll_opy_ (u"ࠫࡨࡵࡤࡦࠩᘕ"): self.code
            },
            bstack11llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᘖ"): self.scope,
            bstack11llll_opy_ (u"࠭ࡴࡢࡩࡶࠫᘗ"): self.tags,
            bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᘘ"): self.framework,
            bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘙ"): self.bstack1ll11l1l_opy_
        }
    def bstack1ll1lll11l1_opy_(self):
        return {
         bstack11llll_opy_ (u"ࠩࡰࡩࡹࡧࠧᘚ"): self.meta
        }
    def bstack1ll1lll1l11_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᘛ"): {
                bstack11llll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᘜ"): self.bstack1ll1lll1lll_opy_
            }
        }
    def bstack1ll1lllll1l_opy_(self, bstack1ll1lll1ll1_opy_, details):
        step = next(filter(lambda st: st[bstack11llll_opy_ (u"ࠬ࡯ࡤࠨᘝ")] == bstack1ll1lll1ll1_opy_, self.meta[bstack11llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᘞ")]), None)
        step.update(details)
    def bstack1lll1ll1_opy_(self, bstack1ll1lll1ll1_opy_):
        step = next(filter(lambda st: st[bstack11llll_opy_ (u"ࠧࡪࡦࠪᘟ")] == bstack1ll1lll1ll1_opy_, self.meta[bstack11llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘠ")]), None)
        step.update({
            bstack11llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘡ"): bstack1l1lll1l_opy_()
        })
    def bstack1ll1111l_opy_(self, bstack1ll1lll1ll1_opy_, result, duration=None):
        bstack1ll1lll11ll_opy_ = bstack1l1lll1l_opy_()
        if bstack1ll1lll1ll1_opy_ is not None and self.meta.get(bstack11llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᘢ")):
            step = next(filter(lambda st: st[bstack11llll_opy_ (u"ࠫ࡮ࡪࠧᘣ")] == bstack1ll1lll1ll1_opy_, self.meta[bstack11llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᘤ")]), None)
            step.update({
                bstack11llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘥ"): bstack1ll1lll11ll_opy_,
                bstack11llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᘦ"): duration if duration else bstack1111l1ll11_opy_(step[bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘧ")], bstack1ll1lll11ll_opy_),
                bstack11llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᘨ"): result.result,
                bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᘩ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1lll1111_opy_):
        if self.meta.get(bstack11llll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘪ")):
            self.meta[bstack11llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᘫ")].append(bstack1ll1lll1111_opy_)
        else:
            self.meta[bstack11llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᘬ")] = [ bstack1ll1lll1111_opy_ ]
    def bstack1ll1ll1lll1_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘭ"): self.bstack11l11lll_opy_(),
            **self.bstack1ll1lllllll_opy_(),
            **self.bstack1lll1111111_opy_(),
            **self.bstack1ll1lll11l1_opy_()
        }
    def bstack1ll1lll111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᘮ"): self.bstack1ll1lll11ll_opy_,
            bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᘯ"): self.duration,
            bstack11llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᘰ"): self.result.result
        }
        if data[bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᘱ")] == bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᘲ"):
            data[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᘳ")] = self.result.bstack1lllll111_opy_()
            data[bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᘴ")] = [{bstack11llll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᘵ"): self.result.bstack1111l1l1l1_opy_()}]
        return data
    def bstack1ll1lll1l1l_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘶ"): self.bstack11l11lll_opy_(),
            **self.bstack1ll1lllllll_opy_(),
            **self.bstack1lll1111111_opy_(),
            **self.bstack1ll1lll111l_opy_(),
            **self.bstack1ll1lll11l1_opy_()
        }
    def bstack11l11l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11llll_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᘷ") in event:
            return self.bstack1ll1ll1lll1_opy_()
        elif bstack11llll_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᘸ") in event:
            return self.bstack1ll1lll1l1l_opy_()
    def bstack11l1llll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1lll11ll_opy_ = time if time else bstack1l1lll1l_opy_()
        self.duration = duration if duration else bstack1111l1ll11_opy_(self.bstack1ll11l1l_opy_, self.bstack1ll1lll11ll_opy_)
        if result:
            self.result = result
class bstack1ll111l1_opy_(bstack11lllll1_opy_):
    def __init__(self, hooks=[], bstack11ll1ll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll1ll1_opy_ = bstack11ll1ll1_opy_
        super().__init__(*args, **kwargs, bstack11l1l1lll_opy_=bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࠪᘹ"))
    @classmethod
    def bstack1ll1llll1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11llll_opy_ (u"࠭ࡩࡥࠩᘺ"): id(step),
                bstack11llll_opy_ (u"ࠧࡵࡧࡻࡸࠬᘻ"): step.name,
                bstack11llll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᘼ"): step.keyword,
            })
        return bstack1ll111l1_opy_(
            **kwargs,
            meta={
                bstack11llll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᘽ"): {
                    bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᘾ"): feature.name,
                    bstack11llll_opy_ (u"ࠫࡵࡧࡴࡩࠩᘿ"): feature.filename,
                    bstack11llll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᙀ"): feature.description
                },
                bstack11llll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᙁ"): {
                    bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᙂ"): scenario.name
                },
                bstack11llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᙃ"): steps,
                bstack11llll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᙄ"): bstack1lll1l1111l_opy_(test)
            }
        )
    def bstack1ll1ll1llll_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᙅ"): self.hooks
        }
    def bstack1ll1llll1ll_opy_(self):
        if self.bstack11ll1ll1_opy_:
            return {
                bstack11llll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᙆ"): self.bstack11ll1ll1_opy_
            }
        return {}
    def bstack1ll1lll1l1l_opy_(self):
        return {
            **super().bstack1ll1lll1l1l_opy_(),
            **self.bstack1ll1ll1llll_opy_()
        }
    def bstack1ll1ll1lll1_opy_(self):
        return {
            **super().bstack1ll1ll1lll1_opy_(),
            **self.bstack1ll1llll1ll_opy_()
        }
    def bstack11l1llll_opy_(self):
        return bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᙇ")
class bstack1lll1l1l_opy_(bstack11lllll1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1lllll11_opy_ = None
        super().__init__(*args, **kwargs, bstack11l1l1lll_opy_=bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᙈ"))
    def bstack11lll1ll_opy_(self):
        return self.hook_type
    def bstack1ll1llll111_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᙉ"): self.hook_type
        }
    def bstack1ll1lll1l1l_opy_(self):
        return {
            **super().bstack1ll1lll1l1l_opy_(),
            **self.bstack1ll1llll111_opy_()
        }
    def bstack1ll1ll1lll1_opy_(self):
        return {
            **super().bstack1ll1ll1lll1_opy_(),
            bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭ᙊ"): self.bstack1ll1lllll11_opy_,
            **self.bstack1ll1llll111_opy_()
        }
    def bstack11l1llll_opy_(self):
        return bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᙋ")
    def bstack1l1ll11l_opy_(self, bstack1ll1lllll11_opy_):
        self.bstack1ll1lllll11_opy_ = bstack1ll1lllll11_opy_