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
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1l1ll111_opy_ import bstack1lll1l1l_opy_, bstack1ll111l1_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
from bstack_utils.helper import bstack1lll1111_opy_, bstack1l1lll1l_opy_, Result
from bstack_utils.bstack1lll111l_opy_ import bstack1ll11ll1_opy_
from bstack_utils.capture import bstack1l1l1l1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll11lll_opy_:
    def __init__(self):
        self.bstack1lll11l1_opy_ = bstack1l1l1l1l_opy_(self.bstack1lll11ll_opy_)
        self.tests = {}
    @staticmethod
    def bstack1lll11ll_opy_(log):
        if not (log[bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࢝")] and log[bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࢞")].strip()):
            return
        active = bstack1ll1l111_opy_.bstack1l1ll1ll_opy_()
        log = {
            bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࢟"): log[bstack11llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩࢠ")],
            bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧࢡ"): bstack1l1lll1l_opy_(),
            bstack11llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ࢢ"): log[bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧࢣ")],
        }
        if active:
            if active[bstack11llll_opy_ (u"ࠧࡵࡻࡳࡩࠬࢤ")] == bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ࢥ"):
                log[bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩࢦ")] = active[bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪࢧ")]
            elif active[bstack11llll_opy_ (u"ࠫࡹࡿࡰࡦࠩࢨ")] == bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࠪࢩ"):
                log[bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ࢪ")] = active[bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧࢫ")]
        bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_([log])
    def start_test(self, name, attrs):
        bstack1l1lll11_opy_ = uuid4().__str__()
        self.tests[bstack1l1lll11_opy_] = {}
        self.bstack1lll11l1_opy_.start()
        bstack1l1ll111_opy_ = bstack1ll111l1_opy_(
            name=name,
            uuid=bstack1l1lll11_opy_,
            bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
            file_path=attrs.filename,
            result=bstack11llll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤࢬ"),
            framework=bstack11llll_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩࢭ"),
            scope=[attrs.feature.name],
            meta={},
            tags=attrs.tags
        )
        self.tests[bstack1l1lll11_opy_][bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ࢮ")] = bstack1l1ll111_opy_
        threading.current_thread().current_test_uuid = bstack1l1lll11_opy_
        bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬࢯ"), bstack1l1ll111_opy_)
    def end_test(self, attrs):
        bstack1ll11l11_opy_ = {
            bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥࢰ"): attrs.feature.name,
            bstack11llll_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦࢱ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1l1ll111_opy_ = self.tests[current_test_uuid][bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪࢲ")]
        meta = {
            bstack11llll_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤࢳ"): bstack1ll11l11_opy_,
            bstack11llll_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣࢴ"): bstack1l1ll111_opy_.meta.get(bstack11llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩࢵ"), []),
            bstack11llll_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨࢶ"): {
                bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥࢷ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1l1ll111_opy_.bstack1l1lllll_opy_(meta)
        bstack1ll11111_opy_, exception = self._1ll1l11l_opy_(attrs)
        bstack1ll1llll_opy_ = Result(result=attrs.status.name, exception=exception, bstack1ll111ll_opy_=[bstack1ll11111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩࢸ")].stop(time=bstack1l1lll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack1ll1llll_opy_)
        bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩࢹ"), self.tests[threading.current_thread().current_test_uuid][bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫࢺ")])
    def bstack1lll1ll1_opy_(self, attrs):
        bstack1ll1l1ll_opy_ = {
            bstack11llll_opy_ (u"ࠩ࡬ࡨࠬࢻ"): uuid4().__str__(),
            bstack11llll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫࢼ"): attrs.keyword,
            bstack11llll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫࢽ"): [],
            bstack11llll_opy_ (u"ࠬࡺࡥࡹࡶࠪࢾ"): attrs.name,
            bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪࢿ"): bstack1l1lll1l_opy_(),
            bstack11llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧࣀ"): bstack11llll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩࣁ"),
            bstack11llll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧࣂ"): bstack11llll_opy_ (u"ࠪࠫࣃ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧࣄ")].add_step(bstack1ll1l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack1ll1l1ll_opy_[bstack11llll_opy_ (u"ࠬ࡯ࡤࠨࣅ")]
    def bstack1l1l1l11_opy_(self, attrs):
        current_test_id = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪࣆ"), None)
        current_step_uuid = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫࣇ"), None)
        bstack1ll11111_opy_, exception = self._1ll1l11l_opy_(attrs)
        bstack1ll1llll_opy_ = Result(result=attrs.status.name, exception=exception, bstack1ll111ll_opy_=[bstack1ll11111_opy_])
        self.tests[current_test_id][bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫࣈ")].bstack1ll1111l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1ll1llll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1lll1l11_opy_(self, name, attrs):
        bstack1ll1lll1_opy_ = uuid4().__str__()
        self.tests[bstack1ll1lll1_opy_] = {}
        self.bstack1lll11l1_opy_.start()
        if name == bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨࣉ") or name == bstack11llll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ࣊"):
            file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
        else:
            file_path = attrs.filename
        hook_data = bstack1lll1l1l_opy_(
            name=name,
            uuid=bstack1ll1lll1_opy_,
            bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
            file_path=file_path,
            framework=bstack11llll_opy_ (u"ࠦࡇ࡫ࡨࡢࡸࡨࠦ࣋"),
            result=bstack11llll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ࣌"),
            hook_type=bstack1l1l1ll1_opy_[name]
        )
        self.tests[bstack1ll1lll1_opy_][bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡧࡴࡢࠤ࣍")] = hook_data
        current_test_id = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠢࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦ࣎"), None)
        if current_test_id:
            hook_data.bstack1l1ll11l_opy_(current_test_id)
        if name == bstack11llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰ࣏ࠧ"):
            threading.current_thread().before_all_hook_uuid = bstack1ll1lll1_opy_
        threading.current_thread().current_hook_uuid = bstack1ll1lll1_opy_
        bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠤࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦ࣐ࠥ"), hook_data)
    def bstack1lll1lll_opy_(self, attrs):
        bstack1l1l1lll_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪ࣑ࠧ"), None)
        hook_data = self.tests[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ࣒ࠧ")]
        status = bstack11llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨ࣓ࠧ")
        exception = None
        bstack1ll11111_opy_ = None
        if hook_data.name == bstack11llll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤࣔ"):
            self.bstack1lll11l1_opy_.reset()
            bstack1ll1ll11_opy_ = self.tests[bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧࣕ"), None)][bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫࣖ")].result.result
            if bstack1ll1ll11_opy_ == bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤࣗ"):
                if attrs.hook_failures == 1:
                    status = bstack11llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥࣘ")
                elif attrs.hook_failures == 2:
                    status = bstack11llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦࣙ")
            elif attrs.bstack1l1ll1l1_opy_:
                status = bstack11llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧࣚ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪࣛ") and attrs.hook_failures == 1:
                status = bstack11llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢࣜ")
            elif hasattr(attrs, bstack11llll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨࣝ")) and attrs.error_message:
                status = bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤࣞ")
            bstack1ll11111_opy_, exception = self._1ll1l11l_opy_(attrs)
        bstack1ll1llll_opy_ = Result(result=status, exception=exception, bstack1ll111ll_opy_=[bstack1ll11111_opy_])
        hook_data.stop(time=bstack1l1lll1l_opy_(), duration=0, result=bstack1ll1llll_opy_)
        bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬࣟ"), self.tests[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࣠")])
        threading.current_thread().current_hook_uuid = None
    def _1ll1l11l_opy_(self, attrs):
        try:
            import traceback
            bstack1llll111_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1ll11111_opy_ = bstack1llll111_opy_[-1] if bstack1llll111_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ࣡"))
            bstack1ll11111_opy_ = None
            exception = None
        return bstack1ll11111_opy_, exception