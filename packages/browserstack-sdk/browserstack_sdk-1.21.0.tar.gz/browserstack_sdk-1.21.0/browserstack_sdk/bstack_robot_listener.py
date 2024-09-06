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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l1l1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1l1l1l_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack11lllll1_opy_, bstack1lll1l1l_opy_, bstack1ll111l1_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1ll11ll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll1111_opy_, bstack1l1lll1l_opy_, Result, \
    bstack11l1l11l_opy_, bstack11ll111l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ࣢"): [],
        bstack11llll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸࣣ࠭"): [],
        bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬࣤ"): []
    }
    bstack11llll1l_opy_ = []
    bstack1l11l1ll_opy_ = []
    @staticmethod
    def bstack1lll11ll_opy_(log):
        if not (log[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪࣥ")] and log[bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࣦࠫ")].strip()):
            return
        active = bstack1ll1l111_opy_.bstack1l1ll1ll_opy_()
        log = {
            bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪࣧ"): log[bstack11llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫࣨ")],
            bstack11llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࣩࠩ"): bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"࡛ࠧࠩ࣪"),
            bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࣫"): log[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࣬")],
        }
        if active:
            if active[bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨ࣭")] == bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬࣮ࠩ"):
                log[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨ࣯ࠬ")] = active[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࣰ࠭")]
            elif active[bstack11llll_opy_ (u"ࠧࡵࡻࡳࡩࣱࠬ")] == bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࣲ࠭"):
                log[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩࣳ")] = active[bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪࣴ")]
        bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll11ll_opy_ = None
        self._1l111ll1_opy_ = None
        self._11l1ll1l_opy_ = OrderedDict()
        self.bstack1lll11l1_opy_ = bstack1l1l1l1l_opy_(self.bstack1lll11ll_opy_)
    @bstack11l1l11l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l1l111_opy_()
        if not self._11l1ll1l_opy_.get(attrs.get(bstack11llll_opy_ (u"ࠫ࡮ࡪࠧࣵ")), None):
            self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"ࠬ࡯ࡤࠨࣶ"))] = {}
        bstack11ll1111_opy_ = bstack1ll111l1_opy_(
                bstack1l111111_opy_=attrs.get(bstack11llll_opy_ (u"࠭ࡩࡥࠩࣷ")),
                name=name,
                bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack11llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧࣸ")], start=os.getcwd()) if attrs.get(bstack11llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࣹ")) != bstack11llll_opy_ (u"ࣺࠩࠪ") else bstack11llll_opy_ (u"ࠪࠫࣻ"),
                framework=bstack11llll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪࣼ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11llll_opy_ (u"ࠬ࡯ࡤࠨࣽ"), None)
        self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"࠭ࡩࡥࠩࣾ"))][bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪࣿ")] = bstack11ll1111_opy_
    @bstack11l1l11l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11ll11l1_opy_()
        self._11l1l1ll_opy_(messages)
        for bstack11ll1l11_opy_ in self.bstack11llll1l_opy_:
            bstack11ll1l11_opy_[bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪऀ")][bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨँ")].extend(self.store[bstack11llll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩं")])
            bstack1ll11ll1_opy_.bstack1l11111l_opy_(bstack11ll1l11_opy_)
        self.bstack11llll1l_opy_ = []
        self.store[bstack11llll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪः")] = []
    @bstack11l1l11l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lll11l1_opy_.start()
        if not self._11l1ll1l_opy_.get(attrs.get(bstack11llll_opy_ (u"ࠬ࡯ࡤࠨऄ")), None):
            self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"࠭ࡩࡥࠩअ"))] = {}
        driver = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭आ"), None)
        bstack1l1ll111_opy_ = bstack1ll111l1_opy_(
            bstack1l111111_opy_=attrs.get(bstack11llll_opy_ (u"ࠨ࡫ࡧࠫइ")),
            name=name,
            bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack11llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩई")], start=os.getcwd()),
            scope=RobotHandler.bstack1l111lll_opy_(attrs.get(bstack11llll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪउ"), None)),
            framework=bstack11llll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪऊ"),
            tags=attrs[bstack11llll_opy_ (u"ࠬࡺࡡࡨࡵࠪऋ")],
            hooks=self.store[bstack11llll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬऌ")],
            bstack11ll1ll1_opy_=bstack1ll11ll1_opy_.bstack1l111l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11llll_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤऍ").format(bstack11llll_opy_ (u"ࠣࠢࠥऎ").join(attrs[bstack11llll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧए")]), name) if attrs[bstack11llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨऐ")] else name
        )
        self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"ࠫ࡮ࡪࠧऑ"))][bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨऒ")] = bstack1l1ll111_opy_
        threading.current_thread().current_test_uuid = bstack1l1ll111_opy_.bstack11l11lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11llll_opy_ (u"࠭ࡩࡥࠩओ"), None)
        self.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨऔ"), bstack1l1ll111_opy_)
    @bstack11l1l11l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lll11l1_opy_.reset()
        bstack11lll11l_opy_ = bstack1l11l111_opy_.get(attrs.get(bstack11llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨक")), bstack11llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪख"))
        self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"ࠪ࡭ࡩ࠭ग"))][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧघ")].stop(time=bstack1l1lll1l_opy_(), duration=int(attrs.get(bstack11llll_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪङ"), bstack11llll_opy_ (u"࠭࠰ࠨच"))), result=Result(result=bstack11lll11l_opy_, exception=attrs.get(bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨछ")), bstack1ll111ll_opy_=[attrs.get(bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩज"))]))
        self.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫझ"), self._11l1ll1l_opy_[attrs.get(bstack11llll_opy_ (u"ࠪ࡭ࡩ࠭ञ"))][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧट")], True)
        self.store[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩठ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l1l11l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l1l111_opy_()
        current_test_id = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨड"), None)
        bstack11l111ll_opy_ = current_test_id if bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩढ"), None) else bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫण"), None)
        if attrs.get(bstack11llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧत"), bstack11llll_opy_ (u"ࠪࠫथ")).lower() in [bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪद"), bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧध")]:
            hook_type = bstack11ll1lll_opy_(attrs.get(bstack11llll_opy_ (u"࠭ࡴࡺࡲࡨࠫन")), bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫऩ"), None))
            hook_name = bstack11llll_opy_ (u"ࠨࡽࢀࠫप").format(attrs.get(bstack11llll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩफ"), bstack11llll_opy_ (u"ࠪࠫब")))
            if hook_type in [bstack11llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨभ"), bstack11llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨम")]:
                hook_name = bstack11llll_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧय").format(bstack11l1111l_opy_.get(hook_type), attrs.get(bstack11llll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧर"), bstack11llll_opy_ (u"ࠨࠩऱ")))
            bstack1l1l111l_opy_ = bstack1lll1l1l_opy_(
                bstack1l111111_opy_=bstack11l111ll_opy_ + bstack11llll_opy_ (u"ࠩ࠰ࠫल") + attrs.get(bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨळ"), bstack11llll_opy_ (u"ࠫࠬऴ")).lower(),
                name=hook_name,
                bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11llll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬव")), start=os.getcwd()),
                framework=bstack11llll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬश"),
                tags=attrs[bstack11llll_opy_ (u"ࠧࡵࡣࡪࡷࠬष")],
                scope=RobotHandler.bstack1l111lll_opy_(attrs.get(bstack11llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨस"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l1l111l_opy_.bstack11l11lll_opy_()
            threading.current_thread().current_hook_id = bstack11l111ll_opy_ + bstack11llll_opy_ (u"ࠩ࠰ࠫह") + attrs.get(bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨऺ"), bstack11llll_opy_ (u"ࠫࠬऻ")).lower()
            self.store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥ़ࠩ")] = [bstack1l1l111l_opy_.bstack11l11lll_opy_()]
            if bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪऽ"), None):
                self.store[bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫा")].append(bstack1l1l111l_opy_.bstack11l11lll_opy_())
            else:
                self.store[bstack11llll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧि")].append(bstack1l1l111l_opy_.bstack11l11lll_opy_())
            if bstack11l111ll_opy_:
                self._11l1ll1l_opy_[bstack11l111ll_opy_ + bstack11llll_opy_ (u"ࠩ࠰ࠫी") + attrs.get(bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨु"), bstack11llll_opy_ (u"ࠫࠬू")).lower()] = { bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨृ"): bstack1l1l111l_opy_ }
            bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧॄ"), bstack1l1l111l_opy_)
        else:
            bstack1ll1l1ll_opy_ = {
                bstack11llll_opy_ (u"ࠧࡪࡦࠪॅ"): uuid4().__str__(),
                bstack11llll_opy_ (u"ࠨࡶࡨࡼࡹ࠭ॆ"): bstack11llll_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨे").format(attrs.get(bstack11llll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪै")), attrs.get(bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩॉ"), bstack11llll_opy_ (u"ࠬ࠭ॊ"))) if attrs.get(bstack11llll_opy_ (u"࠭ࡡࡳࡩࡶࠫो"), []) else attrs.get(bstack11llll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧौ")),
                bstack11llll_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ्"): attrs.get(bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॎ"), []),
                bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧॏ"): bstack1l1lll1l_opy_(),
                bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫॐ"): bstack11llll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭॑"),
                bstack11llll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱ॒ࠫ"): attrs.get(bstack11llll_opy_ (u"ࠧࡥࡱࡦࠫ॓"), bstack11llll_opy_ (u"ࠨࠩ॔"))
            }
            if attrs.get(bstack11llll_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪॕ"), bstack11llll_opy_ (u"ࠪࠫॖ")) != bstack11llll_opy_ (u"ࠫࠬॗ"):
                bstack1ll1l1ll_opy_[bstack11llll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭क़")] = attrs.get(bstack11llll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧख़"))
            if not self.bstack1l11l1ll_opy_:
                self._11l1ll1l_opy_[self._1l11llll_opy_()][bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪग़")].add_step(bstack1ll1l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack1ll1l1ll_opy_[bstack11llll_opy_ (u"ࠨ࡫ࡧࠫज़")]
            self.bstack1l11l1ll_opy_.append(bstack1ll1l1ll_opy_)
    @bstack11l1l11l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11ll11l1_opy_()
        self._11l1l1ll_opy_(messages)
        current_test_id = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫड़"), None)
        bstack11l111ll_opy_ = current_test_id if current_test_id else bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ढ़"), None)
        bstack11l11l1l_opy_ = bstack1l11l111_opy_.get(attrs.get(bstack11llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫफ़")), bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭य़"))
        bstack1l11lll1_opy_ = attrs.get(bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧॠ"))
        if bstack11l11l1l_opy_ != bstack11llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨॡ") and not attrs.get(bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩॢ")) and self._11ll11ll_opy_:
            bstack1l11lll1_opy_ = self._11ll11ll_opy_
        bstack1ll1llll_opy_ = Result(result=bstack11l11l1l_opy_, exception=bstack1l11lll1_opy_, bstack1ll111ll_opy_=[bstack1l11lll1_opy_])
        if attrs.get(bstack11llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧॣ"), bstack11llll_opy_ (u"ࠪࠫ।")).lower() in [bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ॥"), bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ०")]:
            bstack11l111ll_opy_ = current_test_id if current_test_id else bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ१"), None)
            if bstack11l111ll_opy_:
                bstack1l1l1lll_opy_ = bstack11l111ll_opy_ + bstack11llll_opy_ (u"ࠢ࠮ࠤ२") + attrs.get(bstack11llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭३"), bstack11llll_opy_ (u"ࠩࠪ४")).lower()
                self._11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭५")].stop(time=bstack1l1lll1l_opy_(), duration=int(attrs.get(bstack11llll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ६"), bstack11llll_opy_ (u"ࠬ࠶ࠧ७"))), result=bstack1ll1llll_opy_)
                bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ८"), self._11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ९")])
        else:
            bstack11l111ll_opy_ = current_test_id if current_test_id else bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ॰"), None)
            if bstack11l111ll_opy_ and len(self.bstack1l11l1ll_opy_) == 1:
                current_step_uuid = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ॱ"), None)
                self._11l1ll1l_opy_[bstack11l111ll_opy_][bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ॲ")].bstack1ll1111l_opy_(current_step_uuid, duration=int(attrs.get(bstack11llll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩॳ"), bstack11llll_opy_ (u"ࠬ࠶ࠧॴ"))), result=bstack1ll1llll_opy_)
            else:
                self.bstack1l1l11ll_opy_(attrs)
            self.bstack1l11l1ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11llll_opy_ (u"࠭ࡨࡵ࡯࡯ࠫॵ"), bstack11llll_opy_ (u"ࠧ࡯ࡱࠪॶ")) == bstack11llll_opy_ (u"ࠨࡻࡨࡷࠬॷ"):
                return
            self.messages.push(message)
            bstack11llllll_opy_ = []
            if bstack1ll1l111_opy_.bstack1l1ll1ll_opy_():
                bstack11llllll_opy_.append({
                    bstack11llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬॸ"): bstack1l1lll1l_opy_(),
                    bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫॹ"): message.get(bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬॺ")),
                    bstack11llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫॻ"): message.get(bstack11llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬॼ")),
                    **bstack1ll1l111_opy_.bstack1l1ll1ll_opy_()
                })
                if len(bstack11llllll_opy_) > 0:
                    bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_(bstack11llllll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll11ll1_opy_.bstack1l11ll1l_opy_()
    def bstack1l1l11ll_opy_(self, bstack1l111l1l_opy_):
        if not bstack1ll1l111_opy_.bstack1l1ll1ll_opy_():
            return
        kwname = bstack11llll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ॽ").format(bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨॾ")), bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ"), bstack11llll_opy_ (u"ࠪࠫঀ"))) if bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ"), []) else bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬং"))
        error_message = bstack11llll_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧঃ").format(kwname, bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ঄")), str(bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩঅ"))))
        bstack11llll11_opy_ = bstack11llll_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣআ").format(kwname, bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪই")))
        bstack1l1111ll_opy_ = error_message if bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬঈ")) else bstack11llll11_opy_
        bstack11ll1l1l_opy_ = {
            bstack11llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨউ"): self.bstack1l11l1ll_opy_[-1].get(bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪঊ"), bstack1l1lll1l_opy_()),
            bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨঋ"): bstack1l1111ll_opy_,
            bstack11llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧঌ"): bstack11llll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ঍") if bstack1l111l1l_opy_.get(bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ঎")) == bstack11llll_opy_ (u"ࠫࡋࡇࡉࡍࠩএ") else bstack11llll_opy_ (u"ࠬࡏࡎࡇࡑࠪঐ"),
            **bstack1ll1l111_opy_.bstack1l1ll1ll_opy_()
        }
        bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_([bstack11ll1l1l_opy_])
    def _1l11llll_opy_(self):
        for bstack1l111111_opy_ in reversed(self._11l1ll1l_opy_):
            bstack1l11l11l_opy_ = bstack1l111111_opy_
            data = self._11l1ll1l_opy_[bstack1l111111_opy_][bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ঑")]
            if isinstance(data, bstack1lll1l1l_opy_):
                if not bstack11llll_opy_ (u"ࠧࡆࡃࡆࡌࠬ঒") in data.bstack11lll1ll_opy_():
                    return bstack1l11l11l_opy_
            else:
                return bstack1l11l11l_opy_
    def _11l1l1ll_opy_(self, messages):
        try:
            bstack11l111l1_opy_ = BuiltIn().get_variable_value(bstack11llll_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢও")) in (bstack1l11l1l1_opy_.DEBUG, bstack1l11l1l1_opy_.TRACE)
            for message, bstack1l1111l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪঔ"))
                level = message.get(bstack11llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩক"))
                if level == bstack1l11l1l1_opy_.FAIL:
                    self._11ll11ll_opy_ = name or self._11ll11ll_opy_
                    self._1l111ll1_opy_ = bstack1l1111l1_opy_.get(bstack11llll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧখ")) if bstack11l111l1_opy_ and bstack1l1111l1_opy_ else self._1l111ll1_opy_
        except:
            pass
    @classmethod
    def bstack1ll1l1l1_opy_(self, event: str, bstack1l1l11l1_opy_: bstack11lllll1_opy_, bstack1l1l1111_opy_=False):
        if event == bstack11llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧগ"):
            bstack1l1l11l1_opy_.set(hooks=self.store[bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪঘ")])
        if event == bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨঙ"):
            event = bstack11llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪচ")
        if bstack1l1l1111_opy_:
            bstack11l1ll11_opy_ = {
                bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ছ"): event,
                bstack1l1l11l1_opy_.bstack11l1llll_opy_(): bstack1l1l11l1_opy_.bstack11l11l11_opy_(event)
            }
            self.bstack11llll1l_opy_.append(bstack11l1ll11_opy_)
        else:
            bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(event, bstack1l1l11l1_opy_)
class Messages:
    def __init__(self):
        self._11lll111_opy_ = []
    def bstack11l1l111_opy_(self):
        self._11lll111_opy_.append([])
    def bstack11ll11l1_opy_(self):
        return self._11lll111_opy_.pop() if self._11lll111_opy_ else list()
    def push(self, message):
        self._11lll111_opy_[-1].append(message) if self._11lll111_opy_ else self._11lll111_opy_.append([message])
class bstack1l11l1l1_opy_:
    FAIL = bstack11llll_opy_ (u"ࠪࡊࡆࡏࡌࠨজ")
    ERROR = bstack11llll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪঝ")
    WARNING = bstack11llll_opy_ (u"ࠬ࡝ࡁࡓࡐࠪঞ")
    bstack1l11ll11_opy_ = bstack11llll_opy_ (u"࠭ࡉࡏࡈࡒࠫট")
    DEBUG = bstack11llll_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭ঠ")
    TRACE = bstack11llll_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧড")
    bstack11l11ll1_opy_ = [FAIL, ERROR]
def bstack11l1lll1_opy_(bstack11lll1l1_opy_):
    if not bstack11lll1l1_opy_:
        return None
    if bstack11lll1l1_opy_.get(bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬঢ"), None):
        return getattr(bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ণ")], bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩত"), None)
    return bstack11lll1l1_opy_.get(bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪথ"), None)
def bstack11ll1lll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬদ"), bstack11llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩধ")]:
        return
    if hook_type.lower() == bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧন"):
        if current_test_uuid is None:
            return bstack11llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭঩")
        else:
            return bstack11llll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨপ")
    elif hook_type.lower() == bstack11llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ফ"):
        if current_test_uuid is None:
            return bstack11llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨব")
        else:
            return bstack11llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪভ")