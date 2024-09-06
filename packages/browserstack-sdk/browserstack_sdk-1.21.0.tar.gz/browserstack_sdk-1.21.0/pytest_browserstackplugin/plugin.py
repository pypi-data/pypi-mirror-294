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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11llll1111_opy_, bstack1lll111l11_opy_, update, bstack1l11lll1l_opy_,
                                       bstack1ll11lll1_opy_, bstack1lll11l111_opy_, bstack1llll1l11_opy_, bstack1l1l11l1l1_opy_,
                                       bstack111111lll_opy_, bstack11l1l11l11_opy_, bstack1111ll11l_opy_, bstack1l1111111l_opy_,
                                       bstack1l1111lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11lll11111_opy_)
from browserstack_sdk.bstack11111l1l_opy_ import bstack1111ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1l1l1l11_opy_
from bstack_utils.capture import bstack1l1l1l1l_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l111l1l_opy_, bstack1llll1111l_opy_, bstack1lll11l1l_opy_, \
    bstack1lll111l1_opy_
from bstack_utils.helper import bstack1lll1111_opy_, bstack11111ll1ll_opy_, bstack11ll111l_opy_, bstack11l1l1l1l_opy_, bstack111l1lllll_opy_, bstack1l1lll1l_opy_, \
    bstack111l1l111l_opy_, \
    bstack1111l11l1l_opy_, bstack1l111l11ll_opy_, bstack1lllll11l1_opy_, bstack111l1l1l1l_opy_, bstack11l1lll1l1_opy_, Notset, \
    bstack1l111llll_opy_, bstack1111l1ll11_opy_, bstack111111llll_opy_, Result, bstack1111l11111_opy_, bstack1111l11lll_opy_, bstack11l1l11l_opy_, \
    bstack111l1llll_opy_, bstack1lll1ll11l_opy_, bstack11ll1llll_opy_, bstack111l1lll11_opy_
from bstack_utils.bstack11111111l1_opy_ import bstack111111l11l_opy_
from bstack_utils.messages import bstack1ll11l1l1l_opy_, bstack1l11111111_opy_, bstack11ll1111l_opy_, bstack11l1l1llll_opy_, bstack1111l11l_opy_, \
    bstack1l1ll1lll_opy_, bstack11lll1l11l_opy_, bstack11l1ll1111_opy_, bstack1l1ll1ll1l_opy_, bstack1ll111l1l_opy_, \
    bstack11lll1ll11_opy_, bstack111ll1l1l_opy_
from bstack_utils.proxy import bstack11111ll11_opy_, bstack11lll1lll1_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack1lll11ll1ll_opy_, bstack1lll1l111l1_opy_, bstack1lll11l1ll1_opy_, bstack1lll11llll1_opy_, \
    bstack1lll11lll1l_opy_, bstack1lll11l1lll_opy_, bstack1lll1l11111_opy_, bstack1l1l111l11_opy_, bstack1lll11ll11l_opy_
from bstack_utils.bstack11l1llll11_opy_ import bstack1l1l1l11l1_opy_
from bstack_utils.bstack1l1ll1111l_opy_ import bstack11ll11l11l_opy_, bstack111ll1l11_opy_, bstack11ll1ll11_opy_, \
    bstack111llllll_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack1ll111l1_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1ll11ll1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
bstack1l11ll111l_opy_ = None
bstack1l1111l1l1_opy_ = None
bstack11l1l1ll11_opy_ = None
bstack1lll1llll_opy_ = None
bstack1ll1111lll_opy_ = None
bstack1ll111l11l_opy_ = None
bstack1l1l11lll_opy_ = None
bstack111l1l111_opy_ = None
bstack1l111ll1ll_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack11lll1llll_opy_ = None
bstack1l1l1111ll_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1ll1ll111l_opy_ = bstack11llll_opy_ (u"ࠬ࠭ថ")
CONFIG = {}
bstack11l1llllll_opy_ = False
bstack1ll1l1ll1l_opy_ = bstack11llll_opy_ (u"࠭ࠧទ")
bstack1l1llllll_opy_ = bstack11llll_opy_ (u"ࠧࠨធ")
bstack11l1lllll_opy_ = False
bstack1llll1l1l_opy_ = []
bstack1l11ll1ll_opy_ = bstack11l111l1l_opy_
bstack1ll11ll1l11_opy_ = bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨន")
bstack1ll11l1l11l_opy_ = False
bstack1l1111l1l_opy_ = {}
bstack1ll1l1l1ll_opy_ = False
logger = bstack1l1l1l1l11_opy_.get_logger(__name__, bstack1l11ll1ll_opy_)
store = {
    bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ប"): []
}
bstack1ll11lll11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l1ll1l_opy_ = {}
current_test_uuid = None
def bstack11llll111_opy_(page, bstack11ll1l1lll_opy_):
    try:
        page.evaluate(bstack11llll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦផ"),
                      bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨព") + json.dumps(
                          bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"ࠧࢃࡽࠣភ"))
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦម"), e)
def bstack1l1ll11l11_opy_(page, message, level):
    try:
        page.evaluate(bstack11llll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣយ"), bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭រ") + json.dumps(
            message) + bstack11llll_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬល") + json.dumps(level) + bstack11llll_opy_ (u"ࠪࢁࢂ࠭វ"))
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢឝ"), e)
def pytest_configure(config):
    bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
    config.args = bstack1ll1l111_opy_.bstack1ll11llllll_opy_(config.args)
    bstack1111111l_opy_.bstack11l1l11l1l_opy_(bstack11ll1llll_opy_(config.getoption(bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩឞ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11l11l11_opy_ = item.config.getoption(bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨស"))
    plugins = item.config.getoption(bstack11llll_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣហ"))
    report = outcome.get_result()
    bstack1ll11ll1l1l_opy_(item, call, report)
    if bstack11llll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨឡ") not in plugins or bstack11l1lll1l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11llll_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥអ"), None)
    page = getattr(item, bstack11llll_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤឣ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11l11111_opy_(item, report, summary, bstack1ll11l11l11_opy_)
    if (page is not None):
        bstack1ll11l1111l_opy_(item, report, summary, bstack1ll11l11l11_opy_)
def bstack1ll11l11111_opy_(item, report, summary, bstack1ll11l11l11_opy_):
    if report.when == bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪឤ") and report.skipped:
        bstack1lll11ll11l_opy_(report)
    if report.when in [bstack11llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦឥ"), bstack11llll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣឦ")]:
        return
    if not bstack111l1lllll_opy_():
        return
    try:
        if (str(bstack1ll11l11l11_opy_).lower() != bstack11llll_opy_ (u"ࠧࡵࡴࡸࡩࠬឧ")):
            item._driver.execute_script(
                bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ឨ") + json.dumps(
                    report.nodeid) + bstack11llll_opy_ (u"ࠩࢀࢁࠬឩ"))
        os.environ[bstack11llll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ឪ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11llll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦឫ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢឬ")))
    bstack111lllll1_opy_ = bstack11llll_opy_ (u"ࠨࠢឭ")
    bstack1lll11ll11l_opy_(report)
    if not passed:
        try:
            bstack111lllll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11llll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢឮ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111lllll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥឯ")))
        bstack111lllll1_opy_ = bstack11llll_opy_ (u"ࠤࠥឰ")
        if not passed:
            try:
                bstack111lllll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥឱ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111lllll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨឲ")
                    + json.dumps(bstack11llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨឳ"))
                    + bstack11llll_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ឴")
                )
            else:
                item._driver.execute_script(
                    bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ឵")
                    + json.dumps(str(bstack111lllll1_opy_))
                    + bstack11llll_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦា")
                )
        except Exception as e:
            summary.append(bstack11llll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢិ").format(e))
def bstack1ll11l11l1l_opy_(test_name, error_message):
    try:
        bstack1ll11ll11ll_opy_ = []
        bstack111lll1l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪី"), bstack11llll_opy_ (u"ࠫ࠵࠭ឹ"))
        bstack1l1l111l1l_opy_ = {bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪឺ"): test_name, bstack11llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬុ"): error_message, bstack11llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ូ"): bstack111lll1l1_opy_}
        bstack1ll11l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ួ"))
        if os.path.exists(bstack1ll11l1ll1l_opy_):
            with open(bstack1ll11l1ll1l_opy_) as f:
                bstack1ll11ll11ll_opy_ = json.load(f)
        bstack1ll11ll11ll_opy_.append(bstack1l1l111l1l_opy_)
        with open(bstack1ll11l1ll1l_opy_, bstack11llll_opy_ (u"ࠩࡺࠫើ")) as f:
            json.dump(bstack1ll11ll11ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨឿ") + str(e))
def bstack1ll11l1111l_opy_(item, report, summary, bstack1ll11l11l11_opy_):
    if report.when in [bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥៀ"), bstack11llll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢេ")]:
        return
    if (str(bstack1ll11l11l11_opy_).lower() != bstack11llll_opy_ (u"࠭ࡴࡳࡷࡨࠫែ")):
        bstack11llll111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤៃ")))
    bstack111lllll1_opy_ = bstack11llll_opy_ (u"ࠣࠤោ")
    bstack1lll11ll11l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111lllll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11llll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤៅ").format(e)
                )
        try:
            if passed:
                bstack1ll1ll1lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩំ"), None), bstack11llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦះ"))
            else:
                error_message = bstack11llll_opy_ (u"ࠬ࠭ៈ")
                if bstack111lllll1_opy_:
                    bstack1l1ll11l11_opy_(item._page, str(bstack111lllll1_opy_), bstack11llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ៉"))
                    bstack1ll1ll1lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭៊"), None), bstack11llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ់"), str(bstack111lllll1_opy_))
                    error_message = str(bstack111lllll1_opy_)
                else:
                    bstack1ll1ll1lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ៌"), None), bstack11llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ៍"))
                bstack1ll11l11l1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11llll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣ៎").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11llll_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ៏"), default=bstack11llll_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ័"), help=bstack11llll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ៑"))
    parser.addoption(bstack11llll_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹ្ࠢ"), default=bstack11llll_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ៓"), help=bstack11llll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ។"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11llll_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨ៕"), action=bstack11llll_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦ៖"), default=bstack11llll_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨៗ"),
                         help=bstack11llll_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨ៘"))
def bstack1lll11ll_opy_(log):
    if not (log[bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ៙")] and log[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ៚")].strip()):
        return
    active = bstack1l1ll1ll_opy_()
    log = {
        bstack11llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៛"): log[bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪៜ")],
        bstack11llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ៝"): bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"࡚࠭ࠨ៞"),
        bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៟"): log[bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ០")],
    }
    if active:
        if active[bstack11llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ១")] == bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ២"):
            log[bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៣")] = active[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៤")]
        elif active[bstack11llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ៥")] == bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࠬ៦"):
            log[bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៧")] = active[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ៨")]
    bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_([log])
def bstack1l1ll1ll_opy_():
    if len(store[bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៩")]) > 0 and store[bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ៪")][-1]:
        return {
            bstack11llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ៫"): bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ៬"),
            bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៭"): store[bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ៮")][-1]
        }
    if store.get(bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭៯"), None):
        return {
            bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨ៰"): bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ៱"),
            bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៲"): store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ៳")]
        }
    return None
bstack1lll11l1_opy_ = bstack1l1l1l1l_opy_(bstack1lll11ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll11l1l11l_opy_
        item._1ll111llll1_opy_ = True
        bstack1ll11l1l11_opy_ = bstack111l111l_opy_.bstack1lll11lll_opy_(bstack1111l11l1l_opy_(item.own_markers))
        item._a11y_test_case = bstack1ll11l1l11_opy_
        if bstack1ll11l1l11l_opy_:
            driver = getattr(item, bstack11llll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ៴"), None)
            item._a11y_started = bstack111l111l_opy_.bstack1l11l1l111_opy_(driver, bstack1ll11l1l11_opy_)
        if not bstack1ll11ll1_opy_.on() or bstack1ll11ll1l11_opy_ != bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ៵"):
            return
        global current_test_uuid, bstack1lll11l1_opy_
        bstack1lll11l1_opy_.start()
        bstack11lll1l1_opy_ = {
            bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ៶"): uuid4().__str__(),
            bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ៷"): bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"ࠫ࡟࠭៸")
        }
        current_test_uuid = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ៹")]
        store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ៺")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៻")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l1ll1l_opy_[item.nodeid] = {**_11l1ll1l_opy_[item.nodeid], **bstack11lll1l1_opy_}
        bstack1ll11llll1l_opy_(item, _11l1ll1l_opy_[item.nodeid], bstack11llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ៼"))
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ៽"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11lll11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l1l1l1l_opy_():
        atexit.register(bstack1l1llll111_opy_)
        if not bstack1ll11lll11l_opy_:
            try:
                bstack1ll11l11ll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l1lll11_opy_():
                    bstack1ll11l11ll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11l11ll1_opy_:
                    signal.signal(s, bstack1ll11ll1ll1_opy_)
                bstack1ll11lll11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ៾") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11ll1ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ៿")
    try:
        if not bstack1ll11ll1_opy_.on():
            return
        bstack1lll11l1_opy_.start()
        uuid = uuid4().__str__()
        bstack11lll1l1_opy_ = {
            bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠀"): uuid,
            bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᠁"): bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"࡛ࠧࠩ᠂"),
            bstack11llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭᠃"): bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᠄"),
            bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᠅"): bstack11llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᠆"),
            bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ᠇"): bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ᠈")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᠉")] = item
        store[bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᠊")] = [uuid]
        if not _11l1ll1l_opy_.get(item.nodeid, None):
            _11l1ll1l_opy_[item.nodeid] = {bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᠋"): [], bstack11llll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ᠌"): []}
        _11l1ll1l_opy_[item.nodeid][bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᠍")].append(bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠎")])
        _11l1ll1l_opy_[item.nodeid + bstack11llll_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭᠏")] = bstack11lll1l1_opy_
        bstack1ll11l111ll_opy_(item, bstack11lll1l1_opy_, bstack11llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᠐"))
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ᠑"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1111l1l_opy_
        bstack111lll1l1_opy_ = 0
        if bstack11l1lllll_opy_ is True:
            bstack111lll1l1_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᠒")))
        if CONFIG.get(bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᠓"), False):
            if CONFIG.get(bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ᠔"), bstack11llll_opy_ (u"ࠧࡧࡵࡵࡱࠥ᠕")) == bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᠖"):
                bstack1ll111lllll_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᠗"), None)
                bstack11ll1ll1l_opy_ = bstack1ll111lllll_opy_ + bstack11llll_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ᠘")
                driver = getattr(item, bstack11llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᠙"), None)
                bstack1l1l1ll1l1_opy_ = item.get(bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᠚")) or bstack11llll_opy_ (u"ࠫࠬ᠛")
                bstack11ll1l1l11_opy_ = item.get(bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠜")) or bstack11llll_opy_ (u"࠭ࠧ᠝")
                PercySDK.screenshot(driver, bstack11ll1ll1l_opy_, bstack1l1l1ll1l1_opy_=bstack1l1l1ll1l1_opy_, bstack11ll1l1l11_opy_=bstack11ll1l1l11_opy_, bstack1ll1l11l1l_opy_=bstack111lll1l1_opy_)
        if getattr(item, bstack11llll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ᠞"), False):
            bstack1111ll1l_opy_.bstack11111ll1_opy_(getattr(item, bstack11llll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᠟"), None), bstack1l1111l1l_opy_, logger, item)
        if not bstack1ll11ll1_opy_.on():
            return
        bstack11lll1l1_opy_ = {
            bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᠠ"): uuid4().__str__(),
            bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᠡ"): bstack11ll111l_opy_().isoformat() + bstack11llll_opy_ (u"ࠫ࡟࠭ᠢ"),
            bstack11llll_opy_ (u"ࠬࡺࡹࡱࡧࠪᠣ"): bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᠤ"),
            bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᠥ"): bstack11llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᠦ"),
            bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᠧ"): bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᠨ")
        }
        _11l1ll1l_opy_[item.nodeid + bstack11llll_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᠩ")] = bstack11lll1l1_opy_
        bstack1ll11l111ll_opy_(item, bstack11lll1l1_opy_, bstack11llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᠪ"))
    except Exception as err:
        print(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᠫ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll11ll1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll11llll1_opy_(fixturedef.argname):
        store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᠬ")] = request.node
    elif bstack1lll11lll1l_opy_(fixturedef.argname):
        store[bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᠭ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᠮ"): fixturedef.argname,
            bstack11llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᠯ"): bstack111l1l111l_opy_(outcome),
            bstack11llll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᠰ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᠱ")]
        if not _11l1ll1l_opy_.get(current_test_item.nodeid, None):
            _11l1ll1l_opy_[current_test_item.nodeid] = {bstack11llll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᠲ"): []}
        _11l1ll1l_opy_[current_test_item.nodeid][bstack11llll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᠳ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᠴ"), str(err))
if bstack11l1lll1l1_opy_() and bstack1ll11ll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l1ll1l_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᠵ")].bstack1lll1ll1_opy_(id(step))
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨᠶ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l1ll1l_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᠷ")].bstack1ll1111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᠸ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1ll111_opy_: bstack1ll111l1_opy_ = _11l1ll1l_opy_[request.node.nodeid][bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᠹ")]
            bstack1l1ll111_opy_.bstack1ll1111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᠺ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll11ll1l11_opy_
        try:
            if not bstack1ll11ll1_opy_.on() or bstack1ll11ll1l11_opy_ != bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᠻ"):
                return
            global bstack1lll11l1_opy_
            bstack1lll11l1_opy_.start()
            driver = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᠼ"), None)
            if not _11l1ll1l_opy_.get(request.node.nodeid, None):
                _11l1ll1l_opy_[request.node.nodeid] = {}
            bstack1l1ll111_opy_ = bstack1ll111l1_opy_.bstack1ll1llll1l1_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l1lll_opy_(request.node, scenario),
                bstack1ll11l1l_opy_=bstack1l1lll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11llll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᠽ"),
                tags=bstack1lll1l11111_opy_(feature, scenario),
                bstack11ll1ll1_opy_=bstack1ll11ll1_opy_.bstack1l111l11_opy_(driver) if driver and driver.session_id else {}
            )
            _11l1ll1l_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᠾ")] = bstack1l1ll111_opy_
            bstack1ll11l1lll1_opy_(bstack1l1ll111_opy_.uuid)
            bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᠿ"), bstack1l1ll111_opy_)
        except Exception as err:
            print(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨᡀ"), str(err))
def bstack1ll11ll1lll_opy_(bstack1ll1lll1_opy_):
    if bstack1ll1lll1_opy_ in store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᡁ")]:
        store[bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᡂ")].remove(bstack1ll1lll1_opy_)
def bstack1ll11l1lll1_opy_(bstack1l1lll11_opy_):
    store[bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡃ")] = bstack1l1lll11_opy_
    threading.current_thread().current_test_uuid = bstack1l1lll11_opy_
@bstack1ll11ll1_opy_.bstack1ll1l1l11ll_opy_
def bstack1ll11ll1l1l_opy_(item, call, report):
    global bstack1ll11ll1l11_opy_
    bstack1lll1l11l1_opy_ = bstack1l1lll1l_opy_()
    if hasattr(report, bstack11llll_opy_ (u"ࠪࡷࡹࡵࡰࠨᡄ")):
        bstack1lll1l11l1_opy_ = bstack1111l11111_opy_(report.stop)
    elif hasattr(report, bstack11llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᡅ")):
        bstack1lll1l11l1_opy_ = bstack1111l11111_opy_(report.start)
    try:
        if getattr(report, bstack11llll_opy_ (u"ࠬࡽࡨࡦࡰࠪᡆ"), bstack11llll_opy_ (u"࠭ࠧᡇ")) == bstack11llll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᡈ"):
            bstack1lll11l1_opy_.reset()
        if getattr(report, bstack11llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᡉ"), bstack11llll_opy_ (u"ࠩࠪᡊ")) == bstack11llll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᡋ"):
            if bstack1ll11ll1l11_opy_ == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᡌ"):
                _11l1ll1l_opy_[item.nodeid][bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᡍ")] = bstack1lll1l11l1_opy_
                bstack1ll11llll1l_opy_(item, _11l1ll1l_opy_[item.nodeid], bstack11llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᡎ"), report, call)
                store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᡏ")] = None
            elif bstack1ll11ll1l11_opy_ == bstack11llll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᡐ"):
                bstack1l1ll111_opy_ = _11l1ll1l_opy_[item.nodeid][bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᡑ")]
                bstack1l1ll111_opy_.set(hooks=_11l1ll1l_opy_[item.nodeid].get(bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᡒ"), []))
                exception, bstack1ll111ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1ll111ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack11llll_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪᡓ"), bstack11llll_opy_ (u"ࠬ࠭ᡔ"))]
                bstack1l1ll111_opy_.stop(time=bstack1lll1l11l1_opy_, result=Result(result=getattr(report, bstack11llll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᡕ"), bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᡖ")), exception=exception, bstack1ll111ll_opy_=bstack1ll111ll_opy_))
                bstack1ll11ll1_opy_.bstack1ll1l1l1_opy_(bstack11llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡗ"), _11l1ll1l_opy_[item.nodeid][bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᡘ")])
        elif getattr(report, bstack11llll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡙ"), bstack11llll_opy_ (u"ࠫࠬᡚ")) in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᡛ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᡜ")]:
            bstack1l1l1lll_opy_ = item.nodeid + bstack11llll_opy_ (u"ࠧ࠮ࠩᡝ") + getattr(report, bstack11llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᡞ"), bstack11llll_opy_ (u"ࠩࠪᡟ"))
            if getattr(report, bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᡠ"), False):
                hook_type = bstack11llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᡡ") if getattr(report, bstack11llll_opy_ (u"ࠬࡽࡨࡦࡰࠪᡢ"), bstack11llll_opy_ (u"࠭ࠧᡣ")) == bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᡤ") else bstack11llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᡥ")
                _11l1ll1l_opy_[bstack1l1l1lll_opy_] = {
                    bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᡦ"): uuid4().__str__(),
                    bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᡧ"): bstack1lll1l11l1_opy_,
                    bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᡨ"): hook_type
                }
            _11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᡩ")] = bstack1lll1l11l1_opy_
            bstack1ll11ll1lll_opy_(_11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᡪ")])
            bstack1ll11l111ll_opy_(item, _11l1ll1l_opy_[bstack1l1l1lll_opy_], bstack11llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᡫ"), report, call)
            if getattr(report, bstack11llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᡬ"), bstack11llll_opy_ (u"ࠩࠪᡭ")) == bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᡮ"):
                if getattr(report, bstack11llll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᡯ"), bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᡰ")) == bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᡱ"):
                    bstack11lll1l1_opy_ = {
                        bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᡲ"): uuid4().__str__(),
                        bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᡳ"): bstack1l1lll1l_opy_(),
                        bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᡴ"): bstack1l1lll1l_opy_()
                    }
                    _11l1ll1l_opy_[item.nodeid] = {**_11l1ll1l_opy_[item.nodeid], **bstack11lll1l1_opy_}
                    bstack1ll11llll1l_opy_(item, _11l1ll1l_opy_[item.nodeid], bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᡵ"))
                    bstack1ll11llll1l_opy_(item, _11l1ll1l_opy_[item.nodeid], bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᡶ"), report, call)
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᡷ"), str(err))
def bstack1ll11l111l1_opy_(test, bstack11lll1l1_opy_, result=None, call=None, bstack11l1l1lll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1ll111_opy_ = {
        bstack11llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᡸ"): bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᡹")],
        bstack11llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭᡺"): bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺࠧ᡻"),
        bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᡼"): test.name,
        bstack11llll_opy_ (u"ࠫࡧࡵࡤࡺࠩ᡽"): {
            bstack11llll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ᡾"): bstack11llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭᡿"),
            bstack11llll_opy_ (u"ࠧࡤࡱࡧࡩࠬᢀ"): inspect.getsource(test.obj)
        },
        bstack11llll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᢁ"): test.name,
        bstack11llll_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᢂ"): test.name,
        bstack11llll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᢃ"): bstack1ll1l111_opy_.bstack1l111lll_opy_(test),
        bstack11llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᢄ"): file_path,
        bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᢅ"): file_path,
        bstack11llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᢆ"): bstack11llll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᢇ"),
        bstack11llll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᢈ"): file_path,
        bstack11llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᢉ"): bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢊ")],
        bstack11llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᢋ"): bstack11llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᢌ"),
        bstack11llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᢍ"): {
            bstack11llll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᢎ"): test.nodeid
        },
        bstack11llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᢏ"): bstack1111l11l1l_opy_(test.own_markers)
    }
    if bstack11l1l1lll_opy_ in [bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᢐ"), bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᢑ")]:
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᢒ")] = {
            bstack11llll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᢓ"): bstack11lll1l1_opy_.get(bstack11llll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᢔ"), [])
        }
    if bstack11l1l1lll_opy_ == bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᢕ"):
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢖ")] = bstack11llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᢗ")
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᢘ")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᢙ")]
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢚ")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᢛ")]
    if result:
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢜ")] = result.outcome
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᢝ")] = result.duration * 1000
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᢞ")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᢟ")]
        if result.failed:
            bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᢠ")] = bstack1ll11ll1_opy_.bstack1lllll111_opy_(call.excinfo.typename)
            bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᢡ")] = bstack1ll11ll1_opy_.bstack1ll1ll111l1_opy_(call.excinfo, result)
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢢ")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢣ")]
    if outcome:
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢤ")] = bstack111l1l111l_opy_(outcome)
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᢥ")] = 0
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᢦ")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢧ")]
        if bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᢨ")] == bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩᢩ࠭"):
            bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᢪ")] = bstack11llll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ᢫")  # bstack1ll11l11lll_opy_
            bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᢬")] = [{bstack11llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᢭"): [bstack11llll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ᢮")]}]
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᢯")] = bstack11lll1l1_opy_[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢰ")]
    return bstack1l1ll111_opy_
def bstack1ll11ll11l1_opy_(test, bstack1l1l111l_opy_, bstack11l1l1lll_opy_, result, call, outcome, bstack1ll11l1l1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᢱ")]
    hook_name = bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᢲ")]
    hook_data = {
        bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢳ"): bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢴ")],
        bstack11llll_opy_ (u"ࠫࡹࡿࡰࡦࠩᢵ"): bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᢶ"),
        bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᢷ"): bstack11llll_opy_ (u"ࠧࡼࡿࠪᢸ").format(bstack1lll1l111l1_opy_(hook_name)),
        bstack11llll_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᢹ"): {
            bstack11llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᢺ"): bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᢻ"),
            bstack11llll_opy_ (u"ࠫࡨࡵࡤࡦࠩᢼ"): None
        },
        bstack11llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᢽ"): test.name,
        bstack11llll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᢾ"): bstack1ll1l111_opy_.bstack1l111lll_opy_(test, hook_name),
        bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᢿ"): file_path,
        bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᣀ"): file_path,
        bstack11llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᣁ"): bstack11llll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᣂ"),
        bstack11llll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᣃ"): file_path,
        bstack11llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᣄ"): bstack1l1l111l_opy_[bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᣅ")],
        bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᣆ"): bstack11llll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᣇ") if bstack1ll11ll1l11_opy_ == bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᣈ") else bstack11llll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᣉ"),
        bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᣊ"): hook_type
    }
    bstack1ll1lllll11_opy_ = bstack11l1lll1_opy_(_11l1ll1l_opy_.get(test.nodeid, None))
    if bstack1ll1lllll11_opy_:
        hook_data[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᣋ")] = bstack1ll1lllll11_opy_
    if result:
        hook_data[bstack11llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᣌ")] = result.outcome
        hook_data[bstack11llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᣍ")] = result.duration * 1000
        hook_data[bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣎ")] = bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣏ")]
        if result.failed:
            hook_data[bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᣐ")] = bstack1ll11ll1_opy_.bstack1lllll111_opy_(call.excinfo.typename)
            hook_data[bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᣑ")] = bstack1ll11ll1_opy_.bstack1ll1ll111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᣒ")] = bstack111l1l111l_opy_(outcome)
        hook_data[bstack11llll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᣓ")] = 100
        hook_data[bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣔ")] = bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣕ")]
        if hook_data[bstack11llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᣖ")] == bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᣗ"):
            hook_data[bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᣘ")] = bstack11llll_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᣙ")  # bstack1ll11l11lll_opy_
            hook_data[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣚ")] = [{bstack11llll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᣛ"): [bstack11llll_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᣜ")]}]
    if bstack1ll11l1l1ll_opy_:
        hook_data[bstack11llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᣝ")] = bstack1ll11l1l1ll_opy_.result
        hook_data[bstack11llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᣞ")] = bstack1111l1ll11_opy_(bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᣟ")], bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᣠ")])
        hook_data[bstack11llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣡ")] = bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣢ")]
        if hook_data[bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣣ")] == bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᣤ"):
            hook_data[bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᣥ")] = bstack1ll11ll1_opy_.bstack1lllll111_opy_(bstack1ll11l1l1ll_opy_.exception_type)
            hook_data[bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᣦ")] = [{bstack11llll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᣧ"): bstack111111llll_opy_(bstack1ll11l1l1ll_opy_.exception)}]
    return hook_data
def bstack1ll11llll1l_opy_(test, bstack11lll1l1_opy_, bstack11l1l1lll_opy_, result=None, call=None, outcome=None):
    bstack1l1ll111_opy_ = bstack1ll11l111l1_opy_(test, bstack11lll1l1_opy_, result, call, bstack11l1l1lll_opy_, outcome)
    driver = getattr(test, bstack11llll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᣨ"), None)
    if bstack11l1l1lll_opy_ == bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᣩ") and driver:
        bstack1l1ll111_opy_[bstack11llll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᣪ")] = bstack1ll11ll1_opy_.bstack1l111l11_opy_(driver)
    if bstack11l1l1lll_opy_ == bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᣫ"):
        bstack11l1l1lll_opy_ = bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᣬ")
    bstack11l1ll11_opy_ = {
        bstack11llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᣭ"): bstack11l1l1lll_opy_,
        bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᣮ"): bstack1l1ll111_opy_
    }
    bstack1ll11ll1_opy_.bstack1l11111l_opy_(bstack11l1ll11_opy_)
def bstack1ll11l111ll_opy_(test, bstack11lll1l1_opy_, bstack11l1l1lll_opy_, result=None, call=None, outcome=None, bstack1ll11l1l1ll_opy_=None):
    hook_data = bstack1ll11ll11l1_opy_(test, bstack11lll1l1_opy_, bstack11l1l1lll_opy_, result, call, outcome, bstack1ll11l1l1ll_opy_)
    bstack11l1ll11_opy_ = {
        bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᣯ"): bstack11l1l1lll_opy_,
        bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᣰ"): hook_data
    }
    bstack1ll11ll1_opy_.bstack1l11111l_opy_(bstack11l1ll11_opy_)
def bstack11l1lll1_opy_(bstack11lll1l1_opy_):
    if not bstack11lll1l1_opy_:
        return None
    if bstack11lll1l1_opy_.get(bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᣱ"), None):
        return getattr(bstack11lll1l1_opy_[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣲ")], bstack11llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᣳ"), None)
    return bstack11lll1l1_opy_.get(bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩᣴ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll11ll1_opy_.on():
            return
        places = [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᣵ"), bstack11llll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᣶"), bstack11llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ᣷")]
        bstack11llllll_opy_ = []
        for bstack1ll11llll11_opy_ in places:
            records = caplog.get_records(bstack1ll11llll11_opy_)
            bstack1ll11lll1l1_opy_ = bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᣸") if bstack1ll11llll11_opy_ == bstack11llll_opy_ (u"ࠩࡦࡥࡱࡲࠧ᣹") else bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᣺")
            bstack1ll11l1l1l1_opy_ = request.node.nodeid + (bstack11llll_opy_ (u"ࠫࠬ᣻") if bstack1ll11llll11_opy_ == bstack11llll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᣼") else bstack11llll_opy_ (u"࠭࠭ࠨ᣽") + bstack1ll11llll11_opy_)
            bstack1l1lll11_opy_ = bstack11l1lll1_opy_(_11l1ll1l_opy_.get(bstack1ll11l1l1l1_opy_, None))
            if not bstack1l1lll11_opy_:
                continue
            for record in records:
                if bstack1111l11lll_opy_(record.message):
                    continue
                bstack11llllll_opy_.append({
                    bstack11llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᣾"): bstack11111ll1ll_opy_(record.created).isoformat() + bstack11llll_opy_ (u"ࠨ࡜ࠪ᣿"),
                    bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᤀ"): record.levelname,
                    bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᤁ"): record.message,
                    bstack1ll11lll1l1_opy_: bstack1l1lll11_opy_
                })
        if len(bstack11llllll_opy_) > 0:
            bstack1ll11ll1_opy_.bstack1ll1ll1l_opy_(bstack11llllll_opy_)
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᤂ"), str(err))
def bstack1l11llll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1l1l1ll_opy_
    bstack1111l1l11_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᤃ"), None) and bstack1lll1111_opy_(
            threading.current_thread(), bstack11llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᤄ"), None)
    bstack111ll111l_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᤅ"), None) != None and getattr(driver, bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᤆ"), None) == True
    if sequence == bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᤇ") and driver != None:
      if not bstack1ll1l1l1ll_opy_ and bstack111l1lllll_opy_() and bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᤈ") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᤉ")] == True and bstack1lll11ll11_opy_.bstack1l1l11ll1l_opy_(driver_command) and (bstack111ll111l_opy_ or bstack1111l1l11_opy_) and not bstack11lll11111_opy_(args):
        try:
          bstack1ll1l1l1ll_opy_ = True
          logger.debug(bstack11llll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧᤊ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫᤋ").format(str(err)))
        bstack1ll1l1l1ll_opy_ = False
    if sequence == bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᤌ"):
        if driver_command == bstack11llll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᤍ"):
            bstack1ll11ll1_opy_.bstack1lll1lll1l_opy_({
                bstack11llll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᤎ"): response[bstack11llll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩᤏ")],
                bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᤐ"): store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᤑ")]
            })
def bstack1l1llll111_opy_():
    global bstack1llll1l1l_opy_
    bstack1l1l1l1l11_opy_.bstack1l1lll1l1l_opy_()
    logging.shutdown()
    bstack1ll11ll1_opy_.bstack1l11ll1l_opy_()
    for driver in bstack1llll1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11ll1ll1_opy_(*args):
    global bstack1llll1l1l_opy_
    bstack1ll11ll1_opy_.bstack1l11ll1l_opy_()
    for driver in bstack1llll1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll1lllll_opy_(self, *args, **kwargs):
    bstack11l1lll1l_opy_ = bstack1l11ll111l_opy_(self, *args, **kwargs)
    bstack1ll11ll1_opy_.bstack11llllll11_opy_(self)
    return bstack11l1lll1l_opy_
def bstack11llll111l_opy_(framework_name):
    global bstack1ll1ll111l_opy_
    global bstack1l1ll1l11_opy_
    bstack1ll1ll111l_opy_ = framework_name
    logger.info(bstack111ll1l1l_opy_.format(bstack1ll1ll111l_opy_.split(bstack11llll_opy_ (u"࠭࠭ࠨᤒ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111l1lllll_opy_():
            Service.start = bstack1llll1l11_opy_
            Service.stop = bstack1l1l11l1l1_opy_
            webdriver.Remote.__init__ = bstack1ll111llll_opy_
            webdriver.Remote.get = bstack11111l111_opy_
            if not isinstance(os.getenv(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨᤓ")), str):
                return
            WebDriver.close = bstack111111lll_opy_
            WebDriver.quit = bstack111l1ll1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111l1lllll_opy_() and bstack1ll11ll1_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1lllll_opy_
        bstack1l1ll1l11_opy_ = True
    except Exception as e:
        pass
    bstack11l1l1l11l_opy_()
    if os.environ.get(bstack11llll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ᤔ")):
        bstack1l1ll1l11_opy_ = eval(os.environ.get(bstack11llll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧᤕ")))
    if not bstack1l1ll1l11_opy_:
        bstack1111ll11l_opy_(bstack11llll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧᤖ"), bstack11lll1ll11_opy_)
    if bstack11ll11111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11lll1111l_opy_
        except Exception as e:
            logger.error(bstack1l1ll1lll_opy_.format(str(e)))
    if bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᤗ") in str(framework_name).lower():
        if not bstack111l1lllll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lll11l111_opy_
            Config.getoption = bstack1llllllll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11lllll1l1_opy_
        except Exception as e:
            pass
def bstack111l1ll1l_opy_(self):
    global bstack1ll1ll111l_opy_
    global bstack11ll11lll_opy_
    global bstack1l1111l1l1_opy_
    try:
        if bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᤘ") in bstack1ll1ll111l_opy_ and self.session_id != None and bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᤙ"), bstack11llll_opy_ (u"ࠧࠨᤚ")) != bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᤛ"):
            bstack1ll111lll_opy_ = bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᤜ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᤝ")
            bstack1lll1ll11l_opy_(logger, True)
            if self != None:
                bstack111llllll_opy_(self, bstack1ll111lll_opy_, bstack11llll_opy_ (u"ࠫ࠱ࠦࠧᤞ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᤟"), None)
        if item is not None and bstack1ll11l1l11l_opy_:
            bstack1111ll1l_opy_.bstack11111ll1_opy_(self, bstack1l1111l1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11llll_opy_ (u"࠭ࠧᤠ")
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣᤡ") + str(e))
    bstack1l1111l1l1_opy_(self)
    self.session_id = None
def bstack1ll111llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll11lll_opy_
    global bstack1l11l1111l_opy_
    global bstack11l1lllll_opy_
    global bstack1ll1ll111l_opy_
    global bstack1l11ll111l_opy_
    global bstack1llll1l1l_opy_
    global bstack1ll1l1ll1l_opy_
    global bstack1l1llllll_opy_
    global bstack1ll11l1l11l_opy_
    global bstack1l1111l1l_opy_
    CONFIG[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᤢ")] = str(bstack1ll1ll111l_opy_) + str(__version__)
    command_executor = bstack1lllll11l1_opy_(bstack1ll1l1ll1l_opy_)
    logger.debug(bstack11l1l1llll_opy_.format(command_executor))
    proxy = bstack1l1111lll_opy_(CONFIG, proxy)
    bstack111lll1l1_opy_ = 0
    try:
        if bstack11l1lllll_opy_ is True:
            bstack111lll1l1_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᤣ")))
    except:
        bstack111lll1l1_opy_ = 0
    bstack1l11l1lll1_opy_ = bstack11llll1111_opy_(CONFIG, bstack111lll1l1_opy_)
    logger.debug(bstack11l1ll1111_opy_.format(str(bstack1l11l1lll1_opy_)))
    bstack1l1111l1l_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᤤ"))[bstack111lll1l1_opy_]
    if bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᤥ") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᤦ")]:
        bstack11ll1ll11_opy_(bstack1l11l1lll1_opy_, bstack1l1llllll_opy_)
    if bstack111l111l_opy_.bstack111l1l1ll_opy_(CONFIG, bstack111lll1l1_opy_) and bstack111l111l_opy_.bstack1ll1lll11l_opy_(bstack1l11l1lll1_opy_, options, desired_capabilities):
        bstack1ll11l1l11l_opy_ = True
        bstack111l111l_opy_.set_capabilities(bstack1l11l1lll1_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1lll1_opy_ = bstack1lll111l11_opy_(desired_capabilities)
        bstack11ll1lll1_opy_[bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᤧ")] = bstack1l111llll_opy_(CONFIG)
        bstack1l11l11l11_opy_ = bstack11llll1111_opy_(bstack11ll1lll1_opy_)
        if bstack1l11l11l11_opy_:
            bstack1l11l1lll1_opy_ = update(bstack1l11l11l11_opy_, bstack1l11l1lll1_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l11l11_opy_(options, bstack1l11l1lll1_opy_)
    if not options:
        options = bstack1l11lll1l_opy_(bstack1l11l1lll1_opy_)
    if proxy and bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᤨ")):
        options.proxy(proxy)
    if options and bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᤩ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l111l11ll_opy_() < version.parse(bstack11llll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᤪ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11l1lll1_opy_)
    logger.info(bstack11ll1111l_opy_)
    if bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᤫ")):
        bstack1l11ll111l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ᤬")):
        bstack1l11ll111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ᤭")):
        bstack1l11ll111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11ll111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11llll1ll_opy_ = bstack11llll_opy_ (u"࠭ࠧ᤮")
        if bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨ᤯")):
            bstack11llll1ll_opy_ = self.caps.get(bstack11llll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᤰ"))
        else:
            bstack11llll1ll_opy_ = self.capabilities.get(bstack11llll_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤᤱ"))
        if bstack11llll1ll_opy_:
            bstack111l1llll_opy_(bstack11llll1ll_opy_)
            if bstack1l111l11ll_opy_() <= version.parse(bstack11llll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᤲ")):
                self.command_executor._url = bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᤳ") + bstack1ll1l1ll1l_opy_ + bstack11llll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᤴ")
            else:
                self.command_executor._url = bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᤵ") + bstack11llll1ll_opy_ + bstack11llll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᤶ")
            logger.debug(bstack1l11111111_opy_.format(bstack11llll1ll_opy_))
        else:
            logger.debug(bstack1ll11l1l1l_opy_.format(bstack11llll_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᤷ")))
    except Exception as e:
        logger.debug(bstack1ll11l1l1l_opy_.format(e))
    bstack11ll11lll_opy_ = self.session_id
    if bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᤸ") in bstack1ll1ll111l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳ᤹ࠧ"), None)
        if item:
            bstack1ll11ll111l_opy_ = getattr(item, bstack11llll_opy_ (u"ࠫࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࡠࡵࡷࡥࡷࡺࡥࡥࠩ᤺"), False)
            if not getattr(item, bstack11llll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ᤻࠭"), None) and bstack1ll11ll111l_opy_:
                setattr(store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᤼")], bstack11llll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᤽"), self)
        bstack1ll11ll1_opy_.bstack11llllll11_opy_(self)
    bstack1llll1l1l_opy_.append(self)
    if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᤾") in CONFIG and bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᤿") in CONFIG[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᥀")][bstack111lll1l1_opy_]:
        bstack1l11l1111l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᥁")][bstack111lll1l1_opy_][bstack11llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᥂")]
    logger.debug(bstack1ll111l1l_opy_.format(bstack11ll11lll_opy_))
def bstack11111l111_opy_(self, url):
    global bstack1l111ll1ll_opy_
    global CONFIG
    try:
        bstack111ll1l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1ll1ll1l_opy_.format(str(err)))
    try:
        bstack1l111ll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll1l11ll_opy_ = str(e)
            if any(err_msg in bstack1lll1l11ll_opy_ for err_msg in bstack1lll11l1l_opy_):
                bstack111ll1l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1ll1ll1l_opy_.format(str(err)))
        raise e
def bstack1llllll1ll_opy_(item, when):
    global bstack1l1l1111ll_opy_
    try:
        bstack1l1l1111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack11lllll1l1_opy_(item, call, rep):
    global bstack1l1ll1lll1_opy_
    global bstack1llll1l1l_opy_
    name = bstack11llll_opy_ (u"࠭ࠧ᥃")
    try:
        if rep.when == bstack11llll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ᥄"):
            bstack11ll11lll_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11l11l11_opy_ = item.config.getoption(bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᥅"))
            try:
                if (str(bstack1ll11l11l11_opy_).lower() != bstack11llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᥆")):
                    name = str(rep.nodeid)
                    bstack1l11lll11l_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᥇"), name, bstack11llll_opy_ (u"ࠫࠬ᥈"), bstack11llll_opy_ (u"ࠬ࠭᥉"), bstack11llll_opy_ (u"࠭ࠧ᥊"), bstack11llll_opy_ (u"ࠧࠨ᥋"))
                    os.environ[bstack11llll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ᥌")] = name
                    for driver in bstack1llll1l1l_opy_:
                        if bstack11ll11lll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11lll11l_opy_)
            except Exception as e:
                logger.debug(bstack11llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ᥍").format(str(e)))
            try:
                bstack1l1l111l11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᥎"):
                    status = bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᥏") if rep.outcome.lower() == bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᥐ") else bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᥑ")
                    reason = bstack11llll_opy_ (u"ࠧࠨᥒ")
                    if status == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᥓ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11llll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᥔ") if status == bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᥕ") else bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᥖ")
                    data = name + bstack11llll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᥗ") if status == bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᥘ") else name + bstack11llll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᥙ") + reason
                    bstack1ll11l1111_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᥚ"), bstack11llll_opy_ (u"ࠩࠪᥛ"), bstack11llll_opy_ (u"ࠪࠫᥜ"), bstack11llll_opy_ (u"ࠫࠬᥝ"), level, data)
                    for driver in bstack1llll1l1l_opy_:
                        if bstack11ll11lll_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11l1111_opy_)
            except Exception as e:
                logger.debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᥞ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᥟ").format(str(e)))
    bstack1l1ll1lll1_opy_(item, call, rep)
notset = Notset()
def bstack1llllllll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lll1llll_opy_
    if str(name).lower() == bstack11llll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᥠ"):
        return bstack11llll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᥡ")
    else:
        return bstack11lll1llll_opy_(self, name, default, skip)
def bstack11lll1111l_opy_(self):
    global CONFIG
    global bstack1l1l11lll_opy_
    try:
        proxy = bstack11111ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11llll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᥢ")):
                proxies = bstack11lll1lll1_opy_(proxy, bstack1lllll11l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack11ll1ll1ll_opy_ = proxies.popitem()
                    if bstack11llll_opy_ (u"ࠥ࠾࠴࠵ࠢᥣ") in bstack11ll1ll1ll_opy_:
                        return bstack11ll1ll1ll_opy_
                    else:
                        return bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᥤ") + bstack11ll1ll1ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᥥ").format(str(e)))
    return bstack1l1l11lll_opy_(self)
def bstack11ll11111l_opy_():
    return (bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᥦ") in CONFIG or bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᥧ") in CONFIG) and bstack11l1l1l1l_opy_() and bstack1l111l11ll_opy_() >= version.parse(
        bstack1llll1111l_opy_)
def bstack1l1111ll11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l11l1111l_opy_
    global bstack11l1lllll_opy_
    global bstack1ll1ll111l_opy_
    CONFIG[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᥨ")] = str(bstack1ll1ll111l_opy_) + str(__version__)
    bstack111lll1l1_opy_ = 0
    try:
        if bstack11l1lllll_opy_ is True:
            bstack111lll1l1_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᥩ")))
    except:
        bstack111lll1l1_opy_ = 0
    CONFIG[bstack11llll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᥪ")] = True
    bstack1l11l1lll1_opy_ = bstack11llll1111_opy_(CONFIG, bstack111lll1l1_opy_)
    logger.debug(bstack11l1ll1111_opy_.format(str(bstack1l11l1lll1_opy_)))
    if CONFIG.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᥫ")):
        bstack11ll1ll11_opy_(bstack1l11l1lll1_opy_, bstack1l1llllll_opy_)
    if bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᥬ") in CONFIG and bstack11llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᥭ") in CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᥮")][bstack111lll1l1_opy_]:
        bstack1l11l1111l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᥯")][bstack111lll1l1_opy_][bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᥰ")]
    import urllib
    import json
    bstack1l11lll1ll_opy_ = bstack11llll_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᥱ") + urllib.parse.quote(json.dumps(bstack1l11l1lll1_opy_))
    browser = self.connect(bstack1l11lll1ll_opy_)
    return browser
def bstack11l1l1l11l_opy_():
    global bstack1l1ll1l11_opy_
    global bstack1ll1ll111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111ll11l1_opy_
        if not bstack111l1lllll_opy_():
            global bstack111111l1l_opy_
            if not bstack111111l1l_opy_:
                from bstack_utils.helper import bstack1l11ll1l1_opy_, bstack1l1111llll_opy_
                bstack111111l1l_opy_ = bstack1l11ll1l1_opy_()
                bstack1l1111llll_opy_(bstack1ll1ll111l_opy_)
            BrowserType.connect = bstack111ll11l1_opy_
            return
        BrowserType.launch = bstack1l1111ll11_opy_
        bstack1l1ll1l11_opy_ = True
    except Exception as e:
        pass
def bstack1ll11lll1ll_opy_():
    global CONFIG
    global bstack11l1llllll_opy_
    global bstack1ll1l1ll1l_opy_
    global bstack1l1llllll_opy_
    global bstack11l1lllll_opy_
    global bstack1l11ll1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᥲ")))
    bstack11l1llllll_opy_ = eval(os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᥳ")))
    bstack1ll1l1ll1l_opy_ = os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᥴ"))
    bstack1l1111111l_opy_(CONFIG, bstack11l1llllll_opy_)
    bstack1l11ll1ll_opy_ = bstack1l1l1l1l11_opy_.bstack1111l111l_opy_(CONFIG, bstack1l11ll1ll_opy_)
    global bstack1l11ll111l_opy_
    global bstack1l1111l1l1_opy_
    global bstack11l1l1ll11_opy_
    global bstack1lll1llll_opy_
    global bstack1ll1111lll_opy_
    global bstack1ll111l11l_opy_
    global bstack111l1l111_opy_
    global bstack1l111ll1ll_opy_
    global bstack1l1l11lll_opy_
    global bstack11lll1llll_opy_
    global bstack1l1l1111ll_opy_
    global bstack1l1ll1lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11ll111l_opy_ = webdriver.Remote.__init__
        bstack1l1111l1l1_opy_ = WebDriver.quit
        bstack111l1l111_opy_ = WebDriver.close
        bstack1l111ll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᥵") in CONFIG or bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᥶") in CONFIG) and bstack11l1l1l1l_opy_():
        if bstack1l111l11ll_opy_() < version.parse(bstack1llll1111l_opy_):
            logger.error(bstack11lll1l11l_opy_.format(bstack1l111l11ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l11lll_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l1ll1lll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lll1llll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l1111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1111l11l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1ll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ᥷"))
    bstack1l1llllll_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ᥸"), {}).get(bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᥹"))
    bstack11l1lllll_opy_ = True
    bstack11llll111l_opy_(bstack1lll111l1_opy_)
if (bstack111l1l1l1l_opy_()):
    bstack1ll11lll1ll_opy_()
@bstack11l1l11l_opy_(class_method=False)
def bstack1ll11lll111_opy_(hook_name, event, bstack1ll11l1l111_opy_=None):
    if hook_name not in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᥺"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ᥻"), bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭᥼"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ᥽"), bstack11llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ᥾"), bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ᥿"), bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᦀ"), bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᦁ")]:
        return
    node = store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᦂ")]
    if hook_name in [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᦃ"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᦄ")]:
        node = store[bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᦅ")]
    elif hook_name in [bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᦆ"), bstack11llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᦇ")]:
        node = store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᦈ")]
    if event == bstack11llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᦉ"):
        hook_type = bstack1lll11l1ll1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1l111l_opy_ = {
            bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᦊ"): uuid,
            bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᦋ"): bstack1l1lll1l_opy_(),
            bstack11llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᦌ"): bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᦍ"),
            bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᦎ"): hook_type,
            bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᦏ"): hook_name
        }
        store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᦐ")].append(uuid)
        bstack1ll11ll1111_opy_ = node.nodeid
        if hook_type == bstack11llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᦑ"):
            if not _11l1ll1l_opy_.get(bstack1ll11ll1111_opy_, None):
                _11l1ll1l_opy_[bstack1ll11ll1111_opy_] = {bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᦒ"): []}
            _11l1ll1l_opy_[bstack1ll11ll1111_opy_][bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᦓ")].append(bstack1l1l111l_opy_[bstack11llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᦔ")])
        _11l1ll1l_opy_[bstack1ll11ll1111_opy_ + bstack11llll_opy_ (u"ࠫ࠲࠭ᦕ") + hook_name] = bstack1l1l111l_opy_
        bstack1ll11l111ll_opy_(node, bstack1l1l111l_opy_, bstack11llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᦖ"))
    elif event == bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᦗ"):
        bstack1l1l1lll_opy_ = node.nodeid + bstack11llll_opy_ (u"ࠧ࠮ࠩᦘ") + hook_name
        _11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᦙ")] = bstack1l1lll1l_opy_()
        bstack1ll11ll1lll_opy_(_11l1ll1l_opy_[bstack1l1l1lll_opy_][bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦚ")])
        bstack1ll11l111ll_opy_(node, _11l1ll1l_opy_[bstack1l1l1lll_opy_], bstack11llll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᦛ"), bstack1ll11l1l1ll_opy_=bstack1ll11l1l111_opy_)
def bstack1ll11l1ll11_opy_():
    global bstack1ll11ll1l11_opy_
    if bstack11l1lll1l1_opy_():
        bstack1ll11ll1l11_opy_ = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᦜ")
    else:
        bstack1ll11ll1l11_opy_ = bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦝ")
@bstack1ll11ll1_opy_.bstack1ll1l1l11ll_opy_
def bstack1ll11l1llll_opy_():
    bstack1ll11l1ll11_opy_()
    if bstack11l1l1l1l_opy_():
        bstack1l1l1l11l1_opy_(bstack1l11llll1_opy_)
    try:
        bstack111111l11l_opy_(bstack1ll11lll111_opy_)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᦞ").format(e))
bstack1ll11l1llll_opy_()