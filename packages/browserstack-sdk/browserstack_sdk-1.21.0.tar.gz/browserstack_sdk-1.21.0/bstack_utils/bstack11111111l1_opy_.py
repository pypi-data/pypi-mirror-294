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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11111l1lll_opy_
from browserstack_sdk.bstack11111l1l_opy_ import bstack1111ll1l_opy_
def _1111111l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111111l11l_opy_:
    def __init__(self, handler):
        self._111111ll11_opy_ = {}
        self._1111111lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1111ll1l_opy_.version()
        if bstack11111l1lll_opy_(pytest_version, bstack11llll_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᑼ")) >= 0:
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑽ")] = Module._register_setup_function_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑾ")] = Module._register_setup_module_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑿ")] = Class._register_setup_class_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒀ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒁ"))
            Module._register_setup_module_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒂ"))
            Class._register_setup_class_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒃ"))
            Class._register_setup_method_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒄ"))
        else:
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒅ")] = Module._inject_setup_function_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒆ")] = Module._inject_setup_module_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒇ")] = Class._inject_setup_class_fixture
            self._111111ll11_opy_[bstack11llll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒈ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒉ"))
            Module._inject_setup_module_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒊ"))
            Class._inject_setup_class_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒋ"))
            Class._inject_setup_method_fixture = self.bstack111111l1l1_opy_(bstack11llll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒌ"))
    def bstack111111ll1l_opy_(self, bstack111111111l_opy_, hook_type):
        meth = getattr(bstack111111111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111111lll_opy_[hook_type] = meth
            setattr(bstack111111111l_opy_, hook_type, self.bstack1111111111_opy_(hook_type))
    def bstack11111111ll_opy_(self, instance, bstack1111111ll1_opy_):
        if bstack1111111ll1_opy_ == bstack11llll_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᒍ"):
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᒎ"))
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᒏ"))
        if bstack1111111ll1_opy_ == bstack11llll_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᒐ"):
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᒑ"))
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᒒ"))
        if bstack1111111ll1_opy_ == bstack11llll_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᒓ"):
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᒔ"))
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᒕ"))
        if bstack1111111ll1_opy_ == bstack11llll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᒖ"):
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᒗ"))
            self.bstack111111ll1l_opy_(instance.obj, bstack11llll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᒘ"))
    @staticmethod
    def bstack111111lll1_opy_(hook_type, func, args):
        if hook_type in [bstack11llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᒙ"), bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᒚ")]:
            _1111111l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111111111_opy_(self, hook_type):
        def bstack1111111l1l_opy_(arg=None):
            self.handler(hook_type, bstack11llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᒛ"))
            result = None
            exception = None
            try:
                self.bstack111111lll1_opy_(hook_type, self._1111111lll_opy_[hook_type], (arg,))
                result = Result(result=bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᒜ"))
            except Exception as e:
                result = Result(result=bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒝ"), exception=e)
                self.handler(hook_type, bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᒞ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᒟ"), result)
        def bstack111111l1ll_opy_(this, arg=None):
            self.handler(hook_type, bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᒠ"))
            result = None
            exception = None
            try:
                self.bstack111111lll1_opy_(hook_type, self._1111111lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᒡ"))
            except Exception as e:
                result = Result(result=bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒢ"), exception=e)
                self.handler(hook_type, bstack11llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᒣ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᒤ"), result)
        if hook_type in [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᒥ"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᒦ")]:
            return bstack111111l1ll_opy_
        return bstack1111111l1l_opy_
    def bstack111111l1l1_opy_(self, bstack1111111ll1_opy_):
        def bstack111111l111_opy_(this, *args, **kwargs):
            self.bstack11111111ll_opy_(this, bstack1111111ll1_opy_)
            self._111111ll11_opy_[bstack1111111ll1_opy_](this, *args, **kwargs)
        return bstack111111l111_opy_