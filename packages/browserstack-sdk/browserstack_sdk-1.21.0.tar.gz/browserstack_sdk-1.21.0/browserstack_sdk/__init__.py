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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1llll1ll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1l111ll_opy_ import bstack11lll1l111_opy_
import time
import requests
def bstack1l111lll1_opy_():
  global CONFIG
  headers = {
        bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ৓"): bstack11llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭৔"),
      }
  proxies = bstack1ll11ll11_opy_(CONFIG, bstack11l1l1l111_opy_)
  try:
    response = requests.get(bstack11l1l1l111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11llll11l1_opy_ = response.json()[bstack11llll_opy_ (u"ࠫ࡭ࡻࡢࡴࠩ৕")]
      logger.debug(bstack11ll1111l1_opy_.format(response.json()))
      return bstack11llll11l1_opy_
    else:
      logger.debug(bstack111ll1ll1_opy_.format(bstack11llll_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦ৖")))
  except Exception as e:
    logger.debug(bstack111ll1ll1_opy_.format(e))
def bstack1111ll1ll_opy_(hub_url):
  global CONFIG
  url = bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣৗ")+  hub_url + bstack11llll_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢ৘")
  headers = {
        bstack11llll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ৙"): bstack11llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ৚"),
      }
  proxies = bstack1ll11ll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll11l1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll111lll_opy_.format(hub_url, e))
def bstack1llll1l1ll_opy_():
  try:
    global bstack1ll1l1ll1l_opy_
    bstack11llll11l1_opy_ = bstack1l111lll1_opy_()
    bstack11l1l111l_opy_ = []
    results = []
    for bstack1l111l1l1l_opy_ in bstack11llll11l1_opy_:
      bstack11l1l111l_opy_.append(bstack11l11111_opy_(target=bstack1111ll1ll_opy_,args=(bstack1l111l1l1l_opy_,)))
    for t in bstack11l1l111l_opy_:
      t.start()
    for t in bstack11l1l111l_opy_:
      results.append(t.join())
    bstack11lllll1l_opy_ = {}
    for item in results:
      hub_url = item[bstack11llll_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ৛")]
      latency = item[bstack11llll_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬড়")]
      bstack11lllll1l_opy_[hub_url] = latency
    bstack1ll11llll_opy_ = min(bstack11lllll1l_opy_, key= lambda x: bstack11lllll1l_opy_[x])
    bstack1ll1l1ll1l_opy_ = bstack1ll11llll_opy_
    logger.debug(bstack11llll11ll_opy_.format(bstack1ll11llll_opy_))
  except Exception as e:
    logger.debug(bstack1l1lllllll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1l1l1l11_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1111l1_opy_, bstack11lll111l_opy_, bstack1l1l11l1ll_opy_, bstack1lll1111_opy_, bstack1l1l1l1ll_opy_, \
  Notset, bstack1l111llll_opy_, \
  bstack1l1l1ll11l_opy_, bstack1l11l1l1l_opy_, bstack1ll11l11l_opy_, bstack11lll11ll1_opy_, bstack11l1lll1l1_opy_, bstack11l1l1l1l_opy_, \
  bstack11ll111ll1_opy_, \
  bstack1ll1l1l1l1_opy_, bstack1ll1111l11_opy_, bstack111l1llll_opy_, bstack1l11l1l1ll_opy_, \
  bstack1lll1ll11l_opy_, bstack1ll1lll1l_opy_, bstack11ll1llll_opy_, bstack1l11llll11_opy_
from bstack_utils.bstack1l11ll111_opy_ import bstack1l11111ll1_opy_
from bstack_utils.bstack11l1llll11_opy_ import bstack1l1l1l11l1_opy_
from bstack_utils.bstack1l1ll1111l_opy_ import bstack111llllll_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1ll11ll1_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1ll1l111_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.proxy import bstack11lll1lll1_opy_, bstack1ll11ll11_opy_, bstack11111ll11_opy_, bstack1l1l1111l_opy_
import bstack_utils.bstack111l1ll1_opy_ as bstack111l111l_opy_
from browserstack_sdk.bstack11111l1l_opy_ import *
from browserstack_sdk.bstack111lllll_opy_ import *
from bstack_utils.bstack1ll11ll11l_opy_ import bstack1l1l111l11_opy_
from browserstack_sdk.bstack1ll11lll_opy_ import *
import bstack_utils.bstack1l1llllll1_opy_ as bstack111lll111_opy_
import bstack_utils.bstack11ll1l1l1_opy_ as bstack1lll111ll1_opy_
bstack1l11111l1l_opy_ = bstack11llll_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬঢ়")
bstack1l11ll1111_opy_ = bstack11llll_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ৞")
from ._version import __version__
bstack1lll1l111_opy_ = None
CONFIG = {}
bstack1l11l1l1l1_opy_ = {}
bstack1lll111111_opy_ = {}
bstack11ll11lll_opy_ = None
bstack1llll1l1l1_opy_ = None
bstack1l11l1111l_opy_ = None
bstack11ll1l1ll1_opy_ = -1
bstack11ll1111ll_opy_ = 0
bstack1l11ll1ll_opy_ = bstack11l111l1l_opy_
bstack1l11l11ll_opy_ = 1
bstack11l1lllll_opy_ = False
bstack11l1l1lll1_opy_ = False
bstack1ll1ll111l_opy_ = bstack11llll_opy_ (u"ࠧࠨয়")
bstack1l1llllll_opy_ = bstack11llll_opy_ (u"ࠨࠩৠ")
bstack11l1llllll_opy_ = False
bstack1lll1l1ll1_opy_ = True
bstack1lllllll1l_opy_ = bstack11llll_opy_ (u"ࠩࠪৡ")
bstack1llll1l1l_opy_ = []
bstack1ll1l1ll1l_opy_ = bstack11llll_opy_ (u"ࠪࠫৢ")
bstack1l1ll1l11_opy_ = False
bstack1ll1lll1l1_opy_ = None
bstack1l1111ll1_opy_ = None
bstack1l111111l1_opy_ = None
bstack1l111lll1l_opy_ = -1
bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠫࢃ࠭ৣ")), bstack11llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৤"), bstack11llll_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ৥"))
bstack1l11l11l1_opy_ = 0
bstack1lll1111l_opy_ = 0
bstack111ll11ll_opy_ = []
bstack1l11l111ll_opy_ = []
bstack1lll11111_opy_ = []
bstack1lll1l11l_opy_ = []
bstack1l11ll11l_opy_ = bstack11llll_opy_ (u"ࠧࠨ০")
bstack11l1111ll_opy_ = bstack11llll_opy_ (u"ࠨࠩ১")
bstack1l1l1llll_opy_ = False
bstack1lllll111l_opy_ = False
bstack1l1111l1l_opy_ = {}
bstack1l11ll111l_opy_ = None
bstack1l1111l1l1_opy_ = None
bstack1l1l11ll11_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1ll1l11ll_opy_ = None
bstack1l11111ll_opy_ = None
bstack11l1l1ll11_opy_ = None
bstack1lll1llll_opy_ = None
bstack11ll11ll11_opy_ = None
bstack1ll1111lll_opy_ = None
bstack1ll111l11l_opy_ = None
bstack1l1l11lll_opy_ = None
bstack111l1l111_opy_ = None
bstack1l111ll1ll_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack11lll1llll_opy_ = None
bstack1l1l1111ll_opy_ = None
bstack1ll1111ll1_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack111l111l1_opy_ = None
bstack1l1llll11l_opy_ = None
bstack111111l1l_opy_ = None
bstack1ll1l1l1ll_opy_ = False
bstack11ll11l1ll_opy_ = bstack11llll_opy_ (u"ࠤࠥ২")
logger = bstack1l1l1l1l11_opy_.get_logger(__name__, bstack1l11ll1ll_opy_)
bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
percy = bstack1l11l1l11l_opy_()
bstack1l1ll1l111_opy_ = bstack11lll1l111_opy_()
bstack1lll111l1l_opy_ = bstack1ll11lll_opy_()
def bstack11l1l111l1_opy_():
  global CONFIG
  global bstack1l1l1llll_opy_
  global bstack1111111l_opy_
  bstack1llll1ll1_opy_ = bstack11l1ll11l1_opy_(CONFIG)
  if bstack1l1l1l1ll_opy_(CONFIG):
    if (bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ৩") in bstack1llll1ll1_opy_ and str(bstack1llll1ll1_opy_[bstack11llll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭৪")]).lower() == bstack11llll_opy_ (u"ࠬࡺࡲࡶࡧࠪ৫")):
      bstack1l1l1llll_opy_ = True
    bstack1111111l_opy_.bstack11l1l11l1l_opy_(bstack1llll1ll1_opy_.get(bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ৬"), False))
  else:
    bstack1l1l1llll_opy_ = True
    bstack1111111l_opy_.bstack11l1l11l1l_opy_(True)
def bstack1ll1l111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l111l11ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1ll111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11llll_opy_ (u"ࠢ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡤࡱࡱࡪ࡮࡭ࡦࡪ࡮ࡨࠦ৭") == args[i].lower() or bstack11llll_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳ࡬ࡩࡨࠤ৮") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllllll1l_opy_
      bstack1lllllll1l_opy_ += bstack11llll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪࠦࠧ৯") + path
      return path
  return None
bstack1l1ll11l1l_opy_ = re.compile(bstack11llll_opy_ (u"ࡵࠦ࠳࠰࠿࡝ࠦࡾࠬ࠳࠰࠿ࠪࡿ࠱࠮ࡄࠨৰ"))
def bstack1l1l11lll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll11l1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11llll_opy_ (u"ࠦࠩࢁࠢৱ") + group + bstack11llll_opy_ (u"ࠧࢃࠢ৲"), os.environ.get(group))
  return value
def bstack1l1ll11111_opy_():
  bstack11lll1ll1l_opy_ = bstack11l1ll111_opy_()
  if bstack11lll1ll1l_opy_ and os.path.exists(os.path.abspath(bstack11lll1ll1l_opy_)):
    fileName = bstack11lll1ll1l_opy_
  if bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ৳") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ৴")])) and not bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ৵") in locals():
    fileName = os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭৶")]
  if bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬ৷") in locals():
    bstack11ll1_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll1_opy_ = bstack11llll_opy_ (u"ࠫࠬ৸")
  bstack1l11ll1ll1_opy_ = os.getcwd()
  bstack1ll111ll11_opy_ = bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ৹")
  bstack1l1lllll11_opy_ = bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿࡡ࡮࡮ࠪ৺")
  while (not os.path.exists(bstack11ll1_opy_)) and bstack1l11ll1ll1_opy_ != bstack11llll_opy_ (u"ࠢࠣ৻"):
    bstack11ll1_opy_ = os.path.join(bstack1l11ll1ll1_opy_, bstack1ll111ll11_opy_)
    if not os.path.exists(bstack11ll1_opy_):
      bstack11ll1_opy_ = os.path.join(bstack1l11ll1ll1_opy_, bstack1l1lllll11_opy_)
    if bstack1l11ll1ll1_opy_ != os.path.dirname(bstack1l11ll1ll1_opy_):
      bstack1l11ll1ll1_opy_ = os.path.dirname(bstack1l11ll1ll1_opy_)
    else:
      bstack1l11ll1ll1_opy_ = bstack11llll_opy_ (u"ࠣࠤৼ")
  if not os.path.exists(bstack11ll1_opy_):
    bstack1111lllll_opy_(
      bstack1llllll11l_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll1_opy_, bstack11llll_opy_ (u"ࠩࡵࠫ৽")) as stream:
      yaml.add_implicit_resolver(bstack11llll_opy_ (u"ࠥࠥࡵࡧࡴࡩࡧࡻࠦ৾"), bstack1l1ll11l1l_opy_)
      yaml.add_constructor(bstack11llll_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧ৿"), bstack1l1l11lll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11ll1_opy_, bstack11llll_opy_ (u"ࠬࡸࠧ਀")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1111lllll_opy_(bstack1ll11ll1ll_opy_.format(str(exc)))
def bstack1l111l1ll_opy_(config):
  bstack1lll1l1ll_opy_ = bstack1l1ll1ll11_opy_(config)
  for option in list(bstack1lll1l1ll_opy_):
    if option.lower() in bstack1ll1111ll_opy_ and option != bstack1ll1111ll_opy_[option.lower()]:
      bstack1lll1l1ll_opy_[bstack1ll1111ll_opy_[option.lower()]] = bstack1lll1l1ll_opy_[option]
      del bstack1lll1l1ll_opy_[option]
  return config
def bstack1ll1lll111_opy_():
  global bstack1lll111111_opy_
  for key, bstack1l1ll1llll_opy_ in bstack11l11ll1l_opy_.items():
    if isinstance(bstack1l1ll1llll_opy_, list):
      for var in bstack1l1ll1llll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll111111_opy_[key] = os.environ[var]
          break
    elif bstack1l1ll1llll_opy_ in os.environ and os.environ[bstack1l1ll1llll_opy_] and str(os.environ[bstack1l1ll1llll_opy_]).strip():
      bstack1lll111111_opy_[key] = os.environ[bstack1l1ll1llll_opy_]
  if bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨਁ") in os.environ:
    bstack1lll111111_opy_[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫਂ")] = {}
    bstack1lll111111_opy_[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬਃ")][bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ਄")] = os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬਅ")]
def bstack1l1ll11l1_opy_():
  global bstack1l11l1l1l1_opy_
  global bstack1lllllll1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਆ").lower() == val.lower():
      bstack1l11l1l1l1_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩਇ")] = {}
      bstack1l11l1l1l1_opy_[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪਈ")][bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਉ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack111l1lll1_opy_ in bstack1l11lllll1_opy_.items():
    if isinstance(bstack111l1lll1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111l1lll1_opy_:
          if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠨ࠯࠰ࠫਊ") + var.lower() == val.lower() and not key in bstack1l11l1l1l1_opy_:
            bstack1l11l1l1l1_opy_[key] = sys.argv[idx + 1]
            bstack1lllllll1l_opy_ += bstack11llll_opy_ (u"ࠩࠣ࠱࠲࠭਋") + var + bstack11llll_opy_ (u"ࠪࠤࠬ਌") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠫ࠲࠳ࠧ਍") + bstack111l1lll1_opy_.lower() == val.lower() and not key in bstack1l11l1l1l1_opy_:
          bstack1l11l1l1l1_opy_[key] = sys.argv[idx + 1]
          bstack1lllllll1l_opy_ += bstack11llll_opy_ (u"ࠬࠦ࠭࠮ࠩ਎") + bstack111l1lll1_opy_ + bstack11llll_opy_ (u"࠭ࠠࠨਏ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1lll111l11_opy_(config):
  bstack1l111l1ll1_opy_ = config.keys()
  for bstack1ll1l1111_opy_, bstack1llll1ll1l_opy_ in bstack1ll11l11ll_opy_.items():
    if bstack1llll1ll1l_opy_ in bstack1l111l1ll1_opy_:
      config[bstack1ll1l1111_opy_] = config[bstack1llll1ll1l_opy_]
      del config[bstack1llll1ll1l_opy_]
  for bstack1ll1l1111_opy_, bstack1llll1ll1l_opy_ in bstack1l11lll111_opy_.items():
    if isinstance(bstack1llll1ll1l_opy_, list):
      for bstack1lllll1lll_opy_ in bstack1llll1ll1l_opy_:
        if bstack1lllll1lll_opy_ in bstack1l111l1ll1_opy_:
          config[bstack1ll1l1111_opy_] = config[bstack1lllll1lll_opy_]
          del config[bstack1lllll1lll_opy_]
          break
    elif bstack1llll1ll1l_opy_ in bstack1l111l1ll1_opy_:
      config[bstack1ll1l1111_opy_] = config[bstack1llll1ll1l_opy_]
      del config[bstack1llll1ll1l_opy_]
  for bstack1lllll1lll_opy_ in list(config):
    for bstack11ll11l11_opy_ in bstack1l11l1ll11_opy_:
      if bstack1lllll1lll_opy_.lower() == bstack11ll11l11_opy_.lower() and bstack1lllll1lll_opy_ != bstack11ll11l11_opy_:
        config[bstack11ll11l11_opy_] = config[bstack1lllll1lll_opy_]
        del config[bstack1lllll1lll_opy_]
  bstack1l1l1l111l_opy_ = [{}]
  if not config.get(bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਐ")):
    config[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑")] = [{}]
  bstack1l1l1l111l_opy_ = config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ਒")]
  for platform in bstack1l1l1l111l_opy_:
    for bstack1lllll1lll_opy_ in list(platform):
      for bstack11ll11l11_opy_ in bstack1l11l1ll11_opy_:
        if bstack1lllll1lll_opy_.lower() == bstack11ll11l11_opy_.lower() and bstack1lllll1lll_opy_ != bstack11ll11l11_opy_:
          platform[bstack11ll11l11_opy_] = platform[bstack1lllll1lll_opy_]
          del platform[bstack1lllll1lll_opy_]
  for bstack1ll1l1111_opy_, bstack1llll1ll1l_opy_ in bstack1l11lll111_opy_.items():
    for platform in bstack1l1l1l111l_opy_:
      if isinstance(bstack1llll1ll1l_opy_, list):
        for bstack1lllll1lll_opy_ in bstack1llll1ll1l_opy_:
          if bstack1lllll1lll_opy_ in platform:
            platform[bstack1ll1l1111_opy_] = platform[bstack1lllll1lll_opy_]
            del platform[bstack1lllll1lll_opy_]
            break
      elif bstack1llll1ll1l_opy_ in platform:
        platform[bstack1ll1l1111_opy_] = platform[bstack1llll1ll1l_opy_]
        del platform[bstack1llll1ll1l_opy_]
  for bstack1ll11ll1l1_opy_ in bstack1l1lll11l_opy_:
    if bstack1ll11ll1l1_opy_ in config:
      if not bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_] in config:
        config[bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_]] = {}
      config[bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_]].update(config[bstack1ll11ll1l1_opy_])
      del config[bstack1ll11ll1l1_opy_]
  for platform in bstack1l1l1l111l_opy_:
    for bstack1ll11ll1l1_opy_ in bstack1l1lll11l_opy_:
      if bstack1ll11ll1l1_opy_ in list(platform):
        if not bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_] in platform:
          platform[bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_]] = {}
        platform[bstack1l1lll11l_opy_[bstack1ll11ll1l1_opy_]].update(platform[bstack1ll11ll1l1_opy_])
        del platform[bstack1ll11ll1l1_opy_]
  config = bstack1l111l1ll_opy_(config)
  return config
def bstack1l1lll1111_opy_(config):
  global bstack1l1llllll_opy_
  if bstack1l1l1l1ll_opy_(config) and bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧਓ") in config and str(config[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨਔ")]).lower() != bstack11llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫਕ"):
    if not bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪਖ") in config:
      config[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫਗ")] = {}
    if not config[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬਘ")].get(bstack11llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡂࡪࡰࡤࡶࡾࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡢࡶ࡬ࡳࡳ࠭ਙ")) and not bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਚ") in config[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨਛ")]:
      bstack1l1lll1l_opy_ = datetime.datetime.now()
      bstack11l11lll1_opy_ = bstack1l1lll1l_opy_.strftime(bstack11llll_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩਜ"))
      hostname = socket.gethostname()
      bstack1111lll1l_opy_ = bstack11llll_opy_ (u"࠭ࠧਝ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11llll_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩਞ").format(bstack11l11lll1_opy_, hostname, bstack1111lll1l_opy_)
      config[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬਟ")][bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਠ")] = identifier
    bstack1l1llllll_opy_ = config[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਡ")].get(bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਢ"))
  return config
def bstack1ll11111l_opy_():
  bstack1ll1ll1l11_opy_ =  bstack11lll11ll1_opy_()[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠫਣ")]
  return bstack1ll1ll1l11_opy_ if bstack1ll1ll1l11_opy_ else -1
def bstack1lllll11ll_opy_(bstack1ll1ll1l11_opy_):
  global CONFIG
  if not bstack11llll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨਤ") in CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਥ")]:
    return
  CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪਦ")] = CONFIG[bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਧ")].replace(
    bstack11llll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬਨ"),
    str(bstack1ll1ll1l11_opy_)
  )
def bstack1l1l1lll1_opy_():
  global CONFIG
  if not bstack11llll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ਩") in CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਪ")]:
    return
  bstack1l1lll1l_opy_ = datetime.datetime.now()
  bstack11l11lll1_opy_ = bstack1l1lll1l_opy_.strftime(bstack11llll_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫਫ"))
  CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਬ")] = CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪਭ")].replace(
    bstack11llll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨਮ"),
    bstack11l11lll1_opy_
  )
def bstack1l1l1lll11_opy_():
  global CONFIG
  if bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਯ") in CONFIG and not bool(CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")]):
    del CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ਱")]
    return
  if not bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਲ") in CONFIG:
    CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਲ਼")] = bstack11llll_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ਴")
  if bstack11llll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨਵ") in CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਸ਼")]:
    bstack1l1l1lll1_opy_()
    os.environ[bstack11llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ਷")] = CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")]
  if not bstack11llll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨਹ") in CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਺")]:
    return
  bstack1ll1ll1l11_opy_ = bstack11llll_opy_ (u"ࠨࠩ਻")
  bstack1l1lll1ll_opy_ = bstack1ll11111l_opy_()
  if bstack1l1lll1ll_opy_ != -1:
    bstack1ll1ll1l11_opy_ = bstack11llll_opy_ (u"ࠩࡆࡍ਼ࠥ࠭") + str(bstack1l1lll1ll_opy_)
  if bstack1ll1ll1l11_opy_ == bstack11llll_opy_ (u"ࠪࠫ਽"):
    bstack1lll1ll1l1_opy_ = bstack11ll1ll1l1_opy_(CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧਾ")])
    if bstack1lll1ll1l1_opy_ != -1:
      bstack1ll1ll1l11_opy_ = str(bstack1lll1ll1l1_opy_)
  if bstack1ll1ll1l11_opy_:
    bstack1lllll11ll_opy_(bstack1ll1ll1l11_opy_)
    os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩਿ")] = CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੀ")]
def bstack1lll11ll1_opy_(bstack111l11lll_opy_, bstack11l1lllll1_opy_, path):
  bstack1ll1lll1ll_opy_ = {
    bstack11llll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫੁ"): bstack11l1lllll1_opy_
  }
  if os.path.exists(path):
    bstack11l1llll1_opy_ = json.load(open(path, bstack11llll_opy_ (u"ࠨࡴࡥࠫੂ")))
  else:
    bstack11l1llll1_opy_ = {}
  bstack11l1llll1_opy_[bstack111l11lll_opy_] = bstack1ll1lll1ll_opy_
  with open(path, bstack11llll_opy_ (u"ࠤࡺ࠯ࠧ੃")) as outfile:
    json.dump(bstack11l1llll1_opy_, outfile)
def bstack11ll1ll1l1_opy_(bstack111l11lll_opy_):
  bstack111l11lll_opy_ = str(bstack111l11lll_opy_)
  bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬ੄")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੅"))
  try:
    if not os.path.exists(bstack1lll1llll1_opy_):
      os.makedirs(bstack1lll1llll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠬࢄࠧ੆")), bstack11llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ੇ"), bstack11llll_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩੈ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11llll_opy_ (u"ࠨࡹࠪ੉")):
        pass
      with open(file_path, bstack11llll_opy_ (u"ࠤࡺ࠯ࠧ੊")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11llll_opy_ (u"ࠪࡶࠬੋ")) as bstack1ll1l11111_opy_:
      bstack1l1ll1l1l1_opy_ = json.load(bstack1ll1l11111_opy_)
    if bstack111l11lll_opy_ in bstack1l1ll1l1l1_opy_:
      bstack11l111lll_opy_ = bstack1l1ll1l1l1_opy_[bstack111l11lll_opy_][bstack11llll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੌ")]
      bstack11ll111l11_opy_ = int(bstack11l111lll_opy_) + 1
      bstack1lll11ll1_opy_(bstack111l11lll_opy_, bstack11ll111l11_opy_, file_path)
      return bstack11ll111l11_opy_
    else:
      bstack1lll11ll1_opy_(bstack111l11lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111llll11_opy_.format(str(e)))
    return -1
def bstack1ll1111111_opy_(config):
  if not config[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫੍ࠧ")] or not config[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ੎")]:
    return True
  else:
    return False
def bstack1l1ll111l_opy_(config, index=0):
  global bstack11l1llllll_opy_
  bstack11l1ll1l1l_opy_ = {}
  caps = bstack1ll1l1111l_opy_ + bstack11ll11ll1l_opy_
  if bstack11l1llllll_opy_:
    caps += bstack1l1lllll1_opy_
  for key in config:
    if key in caps + [bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੏")]:
      continue
    bstack11l1ll1l1l_opy_[key] = config[key]
  if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੐") in config:
    for bstack1llll11l1l_opy_ in config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬੑ")][index]:
      if bstack1llll11l1l_opy_ in caps:
        continue
      bstack11l1ll1l1l_opy_[bstack1llll11l1l_opy_] = config[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੒")][index][bstack1llll11l1l_opy_]
  bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭੓")] = socket.gethostname()
  if bstack11llll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭੔") in bstack11l1ll1l1l_opy_:
    del (bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ੕")])
  return bstack11l1ll1l1l_opy_
def bstack1ll1ll1ll_opy_(config):
  global bstack11l1llllll_opy_
  bstack1l111111l_opy_ = {}
  caps = bstack11ll11ll1l_opy_
  if bstack11l1llllll_opy_:
    caps += bstack1l1lllll1_opy_
  for key in caps:
    if key in config:
      bstack1l111111l_opy_[key] = config[key]
  return bstack1l111111l_opy_
def bstack1l11l111l1_opy_(bstack11l1ll1l1l_opy_, bstack1l111111l_opy_):
  bstack1l1l1lll1l_opy_ = {}
  for key in bstack11l1ll1l1l_opy_.keys():
    if key in bstack1ll11l11ll_opy_:
      bstack1l1l1lll1l_opy_[bstack1ll11l11ll_opy_[key]] = bstack11l1ll1l1l_opy_[key]
    else:
      bstack1l1l1lll1l_opy_[key] = bstack11l1ll1l1l_opy_[key]
  for key in bstack1l111111l_opy_:
    if key in bstack1ll11l11ll_opy_:
      bstack1l1l1lll1l_opy_[bstack1ll11l11ll_opy_[key]] = bstack1l111111l_opy_[key]
    else:
      bstack1l1l1lll1l_opy_[key] = bstack1l111111l_opy_[key]
  return bstack1l1l1lll1l_opy_
def bstack11llll1111_opy_(config, index=0):
  global bstack11l1llllll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1lll1lll_opy_ = bstack11l1111l1_opy_(bstack1l11l11111_opy_, config, logger)
  bstack1l111111l_opy_ = bstack1ll1ll1ll_opy_(config)
  bstack11lll1l1ll_opy_ = bstack11ll11ll1l_opy_
  bstack11lll1l1ll_opy_ += bstack11111111l_opy_
  bstack1l111111l_opy_ = update(bstack1l111111l_opy_, bstack1l1lll1lll_opy_)
  if bstack11l1llllll_opy_:
    bstack11lll1l1ll_opy_ += bstack1l1lllll1_opy_
  if bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੖") in config:
    if bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭੗") in config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘")][index]:
      caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨਖ਼")] = config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][index][bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪਜ਼")]
    if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧੜ") in config[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੝")][index]:
      caps[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩਫ਼")] = str(config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੟")][index][bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ੠")])
    bstack1l1111ll1l_opy_ = bstack11l1111l1_opy_(bstack1l11l11111_opy_, config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੡")][index], logger)
    bstack11lll1l1ll_opy_ += list(bstack1l1111ll1l_opy_.keys())
    for bstack1l1l111111_opy_ in bstack11lll1l1ll_opy_:
      if bstack1l1l111111_opy_ in config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੢")][index]:
        if bstack1l1l111111_opy_ == bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ੣"):
          try:
            bstack1l1111ll1l_opy_[bstack1l1l111111_opy_] = str(config[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤")][index][bstack1l1l111111_opy_] * 1.0)
          except:
            bstack1l1111ll1l_opy_[bstack1l1l111111_opy_] = str(config[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੥")][index][bstack1l1l111111_opy_])
        else:
          bstack1l1111ll1l_opy_[bstack1l1l111111_opy_] = config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][index][bstack1l1l111111_opy_]
        del (config[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][index][bstack1l1l111111_opy_])
    bstack1l111111l_opy_ = update(bstack1l111111l_opy_, bstack1l1111ll1l_opy_)
  bstack11l1ll1l1l_opy_ = bstack1l1ll111l_opy_(config, index)
  for bstack1lllll1lll_opy_ in bstack11ll11ll1l_opy_ + list(bstack1l1lll1lll_opy_.keys()):
    if bstack1lllll1lll_opy_ in bstack11l1ll1l1l_opy_:
      bstack1l111111l_opy_[bstack1lllll1lll_opy_] = bstack11l1ll1l1l_opy_[bstack1lllll1lll_opy_]
      del (bstack11l1ll1l1l_opy_[bstack1lllll1lll_opy_])
  if bstack1l111llll_opy_(config):
    bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ੨")] = True
    caps.update(bstack1l111111l_opy_)
    caps[bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭੩")] = bstack11l1ll1l1l_opy_
  else:
    bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭੪")] = False
    caps.update(bstack1l11l111l1_opy_(bstack11l1ll1l1l_opy_, bstack1l111111l_opy_))
    if bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ੫") in caps:
      caps[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ੬")] = caps[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ੭")]
      del (caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ੮")])
    if bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ੯") in caps:
      caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧੰ")] = caps[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧੱ")]
      del (caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨੲ")])
  return caps
def bstack1lllll11l1_opy_():
  global bstack1ll1l1ll1l_opy_
  if bstack1l111l11ll_opy_() <= version.parse(bstack11llll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨੳ")):
    if bstack1ll1l1ll1l_opy_ != bstack11llll_opy_ (u"ࠩࠪੴ"):
      return bstack11llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦੵ") + bstack1ll1l1ll1l_opy_ + bstack11llll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ੶")
    return bstack1111111l1_opy_
  if bstack1ll1l1ll1l_opy_ != bstack11llll_opy_ (u"ࠬ࠭੷"):
    return bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ੸") + bstack1ll1l1ll1l_opy_ + bstack11llll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ੹")
  return bstack1lll1ll111_opy_
def bstack11111llll_opy_(options):
  return hasattr(options, bstack11llll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ੺"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1l1l1l1_opy_(options, bstack1ll11ll111_opy_):
  for bstack1l1l1ll1l_opy_ in bstack1ll11ll111_opy_:
    if bstack1l1l1ll1l_opy_ in [bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ੻"), bstack11llll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ੼")]:
      continue
    if bstack1l1l1ll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1l1ll1l_opy_] = update(options._experimental_options[bstack1l1l1ll1l_opy_],
                                                         bstack1ll11ll111_opy_[bstack1l1l1ll1l_opy_])
    else:
      options.add_experimental_option(bstack1l1l1ll1l_opy_, bstack1ll11ll111_opy_[bstack1l1l1ll1l_opy_])
  if bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ੽") in bstack1ll11ll111_opy_:
    for arg in bstack1ll11ll111_opy_[bstack11llll_opy_ (u"ࠬࡧࡲࡨࡵࠪ੾")]:
      options.add_argument(arg)
    del (bstack1ll11ll111_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡶࠫ੿")])
  if bstack11llll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ઀") in bstack1ll11ll111_opy_:
    for ext in bstack1ll11ll111_opy_[bstack11llll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬઁ")]:
      options.add_extension(ext)
    del (bstack1ll11ll111_opy_[bstack11llll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ં")])
def bstack1l1llll11_opy_(options, bstack1ll1lllll1_opy_):
  if bstack11llll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩઃ") in bstack1ll1lllll1_opy_:
    for bstack1ll1l1l11l_opy_ in bstack1ll1lllll1_opy_[bstack11llll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ઄")]:
      if bstack1ll1l1l11l_opy_ in options._preferences:
        options._preferences[bstack1ll1l1l11l_opy_] = update(options._preferences[bstack1ll1l1l11l_opy_], bstack1ll1lllll1_opy_[bstack11llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫઅ")][bstack1ll1l1l11l_opy_])
      else:
        options.set_preference(bstack1ll1l1l11l_opy_, bstack1ll1lllll1_opy_[bstack11llll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬઆ")][bstack1ll1l1l11l_opy_])
  if bstack11llll_opy_ (u"ࠧࡢࡴࡪࡷࠬઇ") in bstack1ll1lllll1_opy_:
    for arg in bstack1ll1lllll1_opy_[bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ઈ")]:
      options.add_argument(arg)
def bstack1lll11l11_opy_(options, bstack1ll11lllll_opy_):
  if bstack11llll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪઉ") in bstack1ll11lllll_opy_:
    options.use_webview(bool(bstack1ll11lllll_opy_[bstack11llll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫઊ")]))
  bstack1l1l1l1l1_opy_(options, bstack1ll11lllll_opy_)
def bstack1l1llll1l1_opy_(options, bstack111lll1ll_opy_):
  for bstack11l11l111_opy_ in bstack111lll1ll_opy_:
    if bstack11l11l111_opy_ in [bstack11llll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨઋ"), bstack11llll_opy_ (u"ࠬࡧࡲࡨࡵࠪઌ")]:
      continue
    options.set_capability(bstack11l11l111_opy_, bstack111lll1ll_opy_[bstack11l11l111_opy_])
  if bstack11llll_opy_ (u"࠭ࡡࡳࡩࡶࠫઍ") in bstack111lll1ll_opy_:
    for arg in bstack111lll1ll_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ઎")]:
      options.add_argument(arg)
  if bstack11llll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬએ") in bstack111lll1ll_opy_:
    options.bstack1lll11lll1_opy_(bool(bstack111lll1ll_opy_[bstack11llll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ઐ")]))
def bstack11ll11ll1_opy_(options, bstack1ll1llll11_opy_):
  for bstack11lll1111_opy_ in bstack1ll1llll11_opy_:
    if bstack11lll1111_opy_ in [bstack11llll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઑ"), bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ઒")]:
      continue
    options._options[bstack11lll1111_opy_] = bstack1ll1llll11_opy_[bstack11lll1111_opy_]
  if bstack11llll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩઓ") in bstack1ll1llll11_opy_:
    for bstack1111l11l1_opy_ in bstack1ll1llll11_opy_[bstack11llll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪઔ")]:
      options.bstack11ll11l111_opy_(
        bstack1111l11l1_opy_, bstack1ll1llll11_opy_[bstack11llll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫક")][bstack1111l11l1_opy_])
  if bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ખ") in bstack1ll1llll11_opy_:
    for arg in bstack1ll1llll11_opy_[bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧગ")]:
      options.add_argument(arg)
def bstack1l1l11111_opy_(options, caps):
  if not hasattr(options, bstack11llll_opy_ (u"ࠪࡏࡊ࡟ࠧઘ")):
    return
  if options.KEY == bstack11llll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩઙ") and options.KEY in caps:
    bstack1l1l1l1l1_opy_(options, caps[bstack11llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪચ")])
  elif options.KEY == bstack11llll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫછ") and options.KEY in caps:
    bstack1l1llll11_opy_(options, caps[bstack11llll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬજ")])
  elif options.KEY == bstack11llll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩઝ") and options.KEY in caps:
    bstack1l1llll1l1_opy_(options, caps[bstack11llll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪઞ")])
  elif options.KEY == bstack11llll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫટ") and options.KEY in caps:
    bstack1lll11l11_opy_(options, caps[bstack11llll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬઠ")])
  elif options.KEY == bstack11llll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫડ") and options.KEY in caps:
    bstack11ll11ll1_opy_(options, caps[bstack11llll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬઢ")])
def bstack1l11lll1l_opy_(caps):
  global bstack11l1llllll_opy_
  if isinstance(os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨણ")), str):
    bstack11l1llllll_opy_ = eval(os.getenv(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩત")))
  if bstack11l1llllll_opy_:
    if bstack1ll1l111ll_opy_() < version.parse(bstack11llll_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨથ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪદ")
    if bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩધ") in caps:
      browser = caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪન")]
    elif bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ઩") in caps:
      browser = caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨપ")]
    browser = str(browser).lower()
    if browser == bstack11llll_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨફ") or browser == bstack11llll_opy_ (u"ࠩ࡬ࡴࡦࡪࠧબ"):
      browser = bstack11llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪભ")
    if browser == bstack11llll_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬમ"):
      browser = bstack11llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬય")
    if browser not in [bstack11llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ર"), bstack11llll_opy_ (u"ࠧࡦࡦࡪࡩࠬ઱"), bstack11llll_opy_ (u"ࠨ࡫ࡨࠫલ"), bstack11llll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩળ"), bstack11llll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ઴")]:
      return None
    try:
      package = bstack11llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭વ").format(browser)
      name = bstack11llll_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭શ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11111llll_opy_(options):
        return None
      for bstack1lllll1lll_opy_ in caps.keys():
        options.set_capability(bstack1lllll1lll_opy_, caps[bstack1lllll1lll_opy_])
      bstack1l1l11111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1l11l11_opy_(options, bstack1l11l1lll1_opy_):
  if not bstack11111llll_opy_(options):
    return
  for bstack1lllll1lll_opy_ in bstack1l11l1lll1_opy_.keys():
    if bstack1lllll1lll_opy_ in bstack11111111l_opy_:
      continue
    if bstack1lllll1lll_opy_ in options._caps and type(options._caps[bstack1lllll1lll_opy_]) in [dict, list]:
      options._caps[bstack1lllll1lll_opy_] = update(options._caps[bstack1lllll1lll_opy_], bstack1l11l1lll1_opy_[bstack1lllll1lll_opy_])
    else:
      options.set_capability(bstack1lllll1lll_opy_, bstack1l11l1lll1_opy_[bstack1lllll1lll_opy_])
  bstack1l1l11111_opy_(options, bstack1l11l1lll1_opy_)
  if bstack11llll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬષ") in options._caps:
    if options._caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬસ")] and options._caps[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭હ")].lower() != bstack11llll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ઺"):
      del options._caps[bstack11llll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ઻")]
def bstack111l111ll_opy_(proxy_config):
  if bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ઼") in proxy_config:
    proxy_config[bstack11llll_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧઽ")] = proxy_config[bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪા")]
    del (proxy_config[bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫિ")])
  if bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫી") in proxy_config and proxy_config[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬુ")].lower() != bstack11llll_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪૂ"):
    proxy_config[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧૃ")] = bstack11llll_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬૄ")
  if bstack11llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫૅ") in proxy_config:
    proxy_config[bstack11llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ૆")] = bstack11llll_opy_ (u"ࠨࡲࡤࡧࠬે")
  return proxy_config
def bstack1l1111lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨૈ") in config:
    return proxy
  config[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩૉ")] = bstack111l111ll_opy_(config[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ૊")])
  if proxy == None:
    proxy = Proxy(config[bstack11llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫો")])
  return proxy
def bstack11lll1111l_opy_(self):
  global CONFIG
  global bstack1l1l11lll_opy_
  try:
    proxy = bstack11111ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11llll_opy_ (u"࠭࠮ࡱࡣࡦࠫૌ")):
        proxies = bstack11lll1lll1_opy_(proxy, bstack1lllll11l1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1ll1ll_opy_ = proxies.popitem()
          if bstack11llll_opy_ (u"ࠢ࠻࠱࠲્ࠦ") in bstack11ll1ll1ll_opy_:
            return bstack11ll1ll1ll_opy_
          else:
            return bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ૎") + bstack11ll1ll1ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ૏").format(str(e)))
  return bstack1l1l11lll_opy_(self)
def bstack11ll11111l_opy_():
  global CONFIG
  return bstack1l1l1111l_opy_(CONFIG) and bstack11l1l1l1l_opy_() and bstack1l111l11ll_opy_() >= version.parse(bstack1llll1111l_opy_)
def bstack1lll1l1l11_opy_():
  global CONFIG
  return (bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ૐ") in CONFIG or bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ૑") in CONFIG) and bstack11ll111ll1_opy_()
def bstack1l1ll1ll11_opy_(config):
  bstack1lll1l1ll_opy_ = {}
  if bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૒") in config:
    bstack1lll1l1ll_opy_ = config[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ૓")]
  if bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭૔") in config:
    bstack1lll1l1ll_opy_ = config[bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ૕")]
  proxy = bstack11111ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack11llll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ૖")) and os.path.isfile(proxy):
      bstack1lll1l1ll_opy_[bstack11llll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭૗")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11llll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ૘")):
        proxies = bstack1ll11ll11_opy_(config, bstack1lllll11l1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1ll1ll_opy_ = proxies.popitem()
          if bstack11llll_opy_ (u"ࠧࡀ࠯࠰ࠤ૙") in bstack11ll1ll1ll_opy_:
            parsed_url = urlparse(bstack11ll1ll1ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11llll_opy_ (u"ࠨ࠺࠰࠱ࠥ૚") + bstack11ll1ll1ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll1l1ll_opy_[bstack11llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ૛")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll1l1ll_opy_[bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ૜")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll1l1ll_opy_[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ૝")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll1l1ll_opy_[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭૞")] = str(parsed_url.password)
  return bstack1lll1l1ll_opy_
def bstack11l1ll11l1_opy_(config):
  if bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૟") in config:
    return config[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪૠ")]
  return {}
def bstack11ll1ll11_opy_(caps):
  global bstack1l1llllll_opy_
  if bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧૡ") in caps:
    caps[bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨૢ")][bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧૣ")] = True
    if bstack1l1llllll_opy_:
      caps[bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ૤")][bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")] = bstack1l1llllll_opy_
  else:
    caps[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ૦")] = True
    if bstack1l1llllll_opy_:
      caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૧")] = bstack1l1llllll_opy_
def bstack1lllll1l11_opy_():
  global CONFIG
  if not bstack1l1l1l1ll_opy_(CONFIG):
    return
  if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ૨") in CONFIG and bstack11ll1llll_opy_(CONFIG[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ૩")]):
    if (
      bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ૪") in CONFIG
      and bstack11ll1llll_opy_(CONFIG[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭૫")].get(bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ૬")))
    ):
      logger.debug(bstack11llll_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧ૭"))
      return
    bstack1lll1l1ll_opy_ = bstack1l1ll1ll11_opy_(CONFIG)
    bstack1ll11lll1l_opy_(CONFIG[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ૮")], bstack1lll1l1ll_opy_)
def bstack1ll11lll1l_opy_(key, bstack1lll1l1ll_opy_):
  global bstack1lll1l111_opy_
  logger.info(bstack1l11lll1l1_opy_)
  try:
    bstack1lll1l111_opy_ = Local()
    bstack1l1l1l1l1l_opy_ = {bstack11llll_opy_ (u"࠭࡫ࡦࡻࠪ૯"): key}
    bstack1l1l1l1l1l_opy_.update(bstack1lll1l1ll_opy_)
    logger.debug(bstack11l1ll1lll_opy_.format(str(bstack1l1l1l1l1l_opy_)))
    bstack1lll1l111_opy_.start(**bstack1l1l1l1l1l_opy_)
    if bstack1lll1l111_opy_.isRunning():
      logger.info(bstack11l1l1111l_opy_)
  except Exception as e:
    bstack1111lllll_opy_(bstack11l1l111ll_opy_.format(str(e)))
def bstack1llll1llll_opy_():
  global bstack1lll1l111_opy_
  if bstack1lll1l111_opy_.isRunning():
    logger.info(bstack1l11ll1l11_opy_)
    bstack1lll1l111_opy_.stop()
  bstack1lll1l111_opy_ = None
def bstack1lll1l1lll_opy_(bstack11111l1ll_opy_=[]):
  global CONFIG
  bstack1l1lllll1l_opy_ = []
  bstack1111l1lll_opy_ = [bstack11llll_opy_ (u"ࠧࡰࡵࠪ૰"), bstack11llll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ૱"), bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭૲"), bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૳"), bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ૴"), bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૵")]
  try:
    for err in bstack11111l1ll_opy_:
      bstack11111l1l1_opy_ = {}
      for k in bstack1111l1lll_opy_:
        val = CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૶")][int(err[bstack11llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭૷")])].get(k)
        if val:
          bstack11111l1l1_opy_[k] = val
      if(err[bstack11llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ૸")] != bstack11llll_opy_ (u"ࠩࠪૹ")):
        bstack11111l1l1_opy_[bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩૺ")] = {
          err[bstack11llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩૻ")]: err[bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫૼ")]
        }
        bstack1l1lllll1l_opy_.append(bstack11111l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ૽") + str(e))
  finally:
    return bstack1l1lllll1l_opy_
def bstack1l11l1l11_opy_(file_name):
  bstack1ll111l1l1_opy_ = []
  try:
    bstack1lll11llll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1lll11llll_opy_):
      with open(bstack1lll11llll_opy_) as f:
        bstack11l1ll1ll_opy_ = json.load(f)
        bstack1ll111l1l1_opy_ = bstack11l1ll1ll_opy_
      os.remove(bstack1lll11llll_opy_)
    return bstack1ll111l1l1_opy_
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ૾") + str(e))
    return bstack1ll111l1l1_opy_
def bstack1l1llll111_opy_():
  global bstack11ll11l1ll_opy_
  global bstack1llll1l1l_opy_
  global bstack111ll11ll_opy_
  global bstack1l11l111ll_opy_
  global bstack1lll11111_opy_
  global bstack11l1111ll_opy_
  global CONFIG
  bstack1l1l1lllll_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ૿"))
  if bstack1l1l1lllll_opy_ in [bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ଀"), bstack11llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩଁ")]:
    bstack1ll111ll1l_opy_()
  percy.shutdown()
  if bstack11ll11l1ll_opy_:
    logger.warning(bstack1l111l1l11_opy_.format(str(bstack11ll11l1ll_opy_)))
  else:
    try:
      bstack11l1llll1_opy_ = bstack1l1l1ll11l_opy_(bstack11llll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪଂ"), logger)
      if bstack11l1llll1_opy_.get(bstack11llll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪଃ")) and bstack11l1llll1_opy_.get(bstack11llll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ଄")).get(bstack11llll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩଅ")):
        logger.warning(bstack1l111l1l11_opy_.format(str(bstack11l1llll1_opy_[bstack11llll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ଆ")][bstack11llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫଇ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11ll1l11ll_opy_)
  global bstack1lll1l111_opy_
  if bstack1lll1l111_opy_:
    bstack1llll1llll_opy_()
  try:
    for driver in bstack1llll1l1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack111111111_opy_)
  if bstack11l1111ll_opy_ == bstack11llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଈ"):
    bstack1lll11111_opy_ = bstack1l11l1l11_opy_(bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬଉ"))
  if bstack11l1111ll_opy_ == bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬଊ") and len(bstack1l11l111ll_opy_) == 0:
    bstack1l11l111ll_opy_ = bstack1l11l1l11_opy_(bstack11llll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫଋ"))
    if len(bstack1l11l111ll_opy_) == 0:
      bstack1l11l111ll_opy_ = bstack1l11l1l11_opy_(bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ଌ"))
  bstack1l111l1111_opy_ = bstack11llll_opy_ (u"ࠨࠩ଍")
  if len(bstack111ll11ll_opy_) > 0:
    bstack1l111l1111_opy_ = bstack1lll1l1lll_opy_(bstack111ll11ll_opy_)
  elif len(bstack1l11l111ll_opy_) > 0:
    bstack1l111l1111_opy_ = bstack1lll1l1lll_opy_(bstack1l11l111ll_opy_)
  elif len(bstack1lll11111_opy_) > 0:
    bstack1l111l1111_opy_ = bstack1lll1l1lll_opy_(bstack1lll11111_opy_)
  elif len(bstack1lll1l11l_opy_) > 0:
    bstack1l111l1111_opy_ = bstack1lll1l1lll_opy_(bstack1lll1l11l_opy_)
  if bool(bstack1l111l1111_opy_):
    bstack11l111ll1_opy_(bstack1l111l1111_opy_)
  else:
    bstack11l111ll1_opy_()
  bstack1l11l1l1l_opy_(bstack1ll1l1ll11_opy_, logger)
  bstack1l1l1l1l11_opy_.bstack1ll1ll1l_opy_(CONFIG)
  if len(bstack1lll11111_opy_) > 0:
    sys.exit(len(bstack1lll11111_opy_))
def bstack11ll1lll11_opy_(bstack11111l11l_opy_, frame):
  global bstack1111111l_opy_
  logger.error(bstack1l1ll1l1l_opy_)
  bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ଎"), bstack11111l11l_opy_)
  if hasattr(signal, bstack11llll_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫଏ")):
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫଐ"), signal.Signals(bstack11111l11l_opy_).name)
  else:
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ଑"), bstack11llll_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪ଒"))
  bstack1l1l1lllll_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨଓ"))
  if bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨଔ"):
    bstack1ll11ll1_opy_.stop(bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩକ")))
  bstack1l1llll111_opy_()
  sys.exit(1)
def bstack1111lllll_opy_(err):
  logger.critical(bstack1l1l1llll1_opy_.format(str(err)))
  bstack11l111ll1_opy_(bstack1l1l1llll1_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1llll111_opy_)
  bstack1ll111ll1l_opy_()
  sys.exit(1)
def bstack1111ll11l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l111ll1_opy_(message, True)
  atexit.unregister(bstack1l1llll111_opy_)
  bstack1ll111ll1l_opy_()
  sys.exit(1)
def bstack1l11111l11_opy_():
  global CONFIG
  global bstack1l11l1l1l1_opy_
  global bstack1lll111111_opy_
  global bstack1lll1l1ll1_opy_
  CONFIG = bstack1l1ll11111_opy_()
  load_dotenv(CONFIG.get(bstack11llll_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫଖ")))
  bstack1ll1lll111_opy_()
  bstack1l1ll11l1_opy_()
  CONFIG = bstack1lll111l11_opy_(CONFIG)
  update(CONFIG, bstack1lll111111_opy_)
  update(CONFIG, bstack1l11l1l1l1_opy_)
  CONFIG = bstack1l1lll1111_opy_(CONFIG)
  bstack1lll1l1ll1_opy_ = bstack1l1l1l1ll_opy_(CONFIG)
  os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧଗ")] = bstack1lll1l1ll1_opy_.__str__()
  bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ଘ"), bstack1lll1l1ll1_opy_)
  if (bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩଙ") in CONFIG and bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪଚ") in bstack1l11l1l1l1_opy_) or (
          bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫଛ") in CONFIG and bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬଜ") not in bstack1lll111111_opy_):
    if os.getenv(bstack11llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧଝ")):
      CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ଞ")] = os.getenv(bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩଟ"))
    else:
      bstack1l1l1lll11_opy_()
  elif (bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩଠ") not in CONFIG and bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଡ") in CONFIG) or (
          bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫଢ") in bstack1lll111111_opy_ and bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬଣ") not in bstack1l11l1l1l1_opy_):
    del (CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬତ")])
  if bstack1ll1111111_opy_(CONFIG):
    bstack1111lllll_opy_(bstack1l11ll11ll_opy_)
  bstack11l1l1l1l1_opy_()
  bstack1lll1lllll_opy_()
  if bstack11l1llllll_opy_:
    CONFIG[bstack11llll_opy_ (u"ࠫࡦࡶࡰࠨଥ")] = bstack1ll1ll1l1_opy_(CONFIG)
    logger.info(bstack1l11ll1l1l_opy_.format(CONFIG[bstack11llll_opy_ (u"ࠬࡧࡰࡱࠩଦ")]))
  if not bstack1lll1l1ll1_opy_:
    CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")] = [{}]
def bstack1l1111111l_opy_(config, bstack11lllll11_opy_):
  global CONFIG
  global bstack11l1llllll_opy_
  CONFIG = config
  bstack11l1llllll_opy_ = bstack11lllll11_opy_
def bstack1lll1lllll_opy_():
  global CONFIG
  global bstack11l1llllll_opy_
  if bstack11llll_opy_ (u"ࠧࡢࡲࡳࠫନ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack1111111ll_opy_)
    bstack11l1llllll_opy_ = True
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ଩"), True)
def bstack1ll1ll1l1_opy_(config):
  bstack1l1l111lll_opy_ = bstack11llll_opy_ (u"ࠩࠪପ")
  app = config[bstack11llll_opy_ (u"ࠪࡥࡵࡶࠧଫ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lllll1ll1_opy_:
      if os.path.exists(app):
        bstack1l1l111lll_opy_ = bstack1l1l11l111_opy_(config, app)
      elif bstack1l1lll11ll_opy_(app):
        bstack1l1l111lll_opy_ = app
      else:
        bstack1111lllll_opy_(bstack1l1l1l111_opy_.format(app))
    else:
      if bstack1l1lll11ll_opy_(app):
        bstack1l1l111lll_opy_ = app
      elif os.path.exists(app):
        bstack1l1l111lll_opy_ = bstack1l1l11l111_opy_(app)
      else:
        bstack1111lllll_opy_(bstack1l11l1ll1_opy_)
  else:
    if len(app) > 2:
      bstack1111lllll_opy_(bstack1ll1l111l1_opy_)
    elif len(app) == 2:
      if bstack11llll_opy_ (u"ࠫࡵࡧࡴࡩࠩବ") in app and bstack11llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨଭ") in app:
        if os.path.exists(app[bstack11llll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫମ")]):
          bstack1l1l111lll_opy_ = bstack1l1l11l111_opy_(config, app[bstack11llll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬଯ")], app[bstack11llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫର")])
        else:
          bstack1111lllll_opy_(bstack1l1l1l111_opy_.format(app))
      else:
        bstack1111lllll_opy_(bstack1ll1l111l1_opy_)
    else:
      for key in app:
        if key in bstack1lll1lll11_opy_:
          if key == bstack11llll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ଱"):
            if os.path.exists(app[key]):
              bstack1l1l111lll_opy_ = bstack1l1l11l111_opy_(config, app[key])
            else:
              bstack1111lllll_opy_(bstack1l1l1l111_opy_.format(app))
          else:
            bstack1l1l111lll_opy_ = app[key]
        else:
          bstack1111lllll_opy_(bstack11llll1ll1_opy_)
  return bstack1l1l111lll_opy_
def bstack1l1lll11ll_opy_(bstack1l1l111lll_opy_):
  import re
  bstack1lll11l1ll_opy_ = re.compile(bstack11llll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥଲ"))
  bstack11l11l1ll_opy_ = re.compile(bstack11llll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣଳ"))
  if bstack11llll_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ଴") in bstack1l1l111lll_opy_ or re.fullmatch(bstack1lll11l1ll_opy_, bstack1l1l111lll_opy_) or re.fullmatch(bstack11l11l1ll_opy_, bstack1l1l111lll_opy_):
    return True
  else:
    return False
def bstack1l1l11l111_opy_(config, path, bstack1111ll111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11llll_opy_ (u"࠭ࡲࡣࠩଵ")).read()).hexdigest()
  bstack11l1l11ll_opy_ = bstack1ll11l111l_opy_(md5_hash)
  bstack1l1l111lll_opy_ = None
  if bstack11l1l11ll_opy_:
    logger.info(bstack1l111l11l_opy_.format(bstack11l1l11ll_opy_, md5_hash))
    return bstack11l1l11ll_opy_
  bstack11l1lll11l_opy_ = MultipartEncoder(
    fields={
      bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࠬଶ"): (os.path.basename(path), open(os.path.abspath(path), bstack11llll_opy_ (u"ࠨࡴࡥࠫଷ")), bstack11llll_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ସ")),
      bstack11llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ହ"): bstack1111ll111_opy_
    }
  )
  response = requests.post(bstack1l1l1ll111_opy_, data=bstack11l1lll11l_opy_,
                           headers={bstack11llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ଺"): bstack11l1lll11l_opy_.content_type},
                           auth=(config[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ଻")], config[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺ଼ࠩ")]))
  try:
    res = json.loads(response.text)
    bstack1l1l111lll_opy_ = res[bstack11llll_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨଽ")]
    logger.info(bstack11lll11l1_opy_.format(bstack1l1l111lll_opy_))
    bstack1llll11ll_opy_(md5_hash, bstack1l1l111lll_opy_)
  except ValueError as err:
    bstack1111lllll_opy_(bstack11ll11lll1_opy_.format(str(err)))
  return bstack1l1l111lll_opy_
def bstack11l1l1l1l1_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l11l11ll_opy_
  bstack1lllll11_opy_ = 1
  bstack1l1l1l11ll_opy_ = 1
  if bstack11llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨା") in CONFIG:
    bstack1l1l1l11ll_opy_ = CONFIG[bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩି")]
  else:
    bstack1l1l1l11ll_opy_ = bstack1l1ll1111_opy_(framework_name, args) or 1
  if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ୀ") in CONFIG:
    bstack1lllll11_opy_ = len(CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୁ")])
  bstack1l11l11ll_opy_ = int(bstack1l1l1l11ll_opy_) * int(bstack1lllll11_opy_)
def bstack1l1ll1111_opy_(framework_name, args):
  if framework_name == bstack111l1l11l_opy_ and args and bstack11llll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪୂ") in args:
      bstack11111ll1l_opy_ = args.index(bstack11llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫୃ"))
      return int(args[bstack11111ll1l_opy_ + 1]) or 1
  return 1
def bstack1ll11l111l_opy_(md5_hash):
  bstack1l111ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠧࡿࠩୄ")), bstack11llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ୅"), bstack11llll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ୆"))
  if os.path.exists(bstack1l111ll11l_opy_):
    bstack1ll111ll1_opy_ = json.load(open(bstack1l111ll11l_opy_, bstack11llll_opy_ (u"ࠪࡶࡧ࠭େ")))
    if md5_hash in bstack1ll111ll1_opy_:
      bstack1ll1ll11l_opy_ = bstack1ll111ll1_opy_[md5_hash]
      bstack1lll1l11l1_opy_ = datetime.datetime.now()
      bstack11lll1lll_opy_ = datetime.datetime.strptime(bstack1ll1ll11l_opy_[bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧୈ")], bstack11llll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ୉"))
      if (bstack1lll1l11l1_opy_ - bstack11lll1lll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1ll11l_opy_[bstack11llll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ୊")]):
        return None
      return bstack1ll1ll11l_opy_[bstack11llll_opy_ (u"ࠧࡪࡦࠪୋ")]
  else:
    return None
def bstack1llll11ll_opy_(md5_hash, bstack1l1l111lll_opy_):
  bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪୌ")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬୍ࠩ"))
  if not os.path.exists(bstack1lll1llll1_opy_):
    os.makedirs(bstack1lll1llll1_opy_)
  bstack1l111ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬ୎")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ୏"), bstack11llll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭୐"))
  bstack1llll11l1_opy_ = {
    bstack11llll_opy_ (u"࠭ࡩࡥࠩ୑"): bstack1l1l111lll_opy_,
    bstack11llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ୒"): datetime.datetime.strftime(datetime.datetime.now(), bstack11llll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ୓")),
    bstack11llll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ୔"): str(__version__)
  }
  if os.path.exists(bstack1l111ll11l_opy_):
    bstack1ll111ll1_opy_ = json.load(open(bstack1l111ll11l_opy_, bstack11llll_opy_ (u"ࠪࡶࡧ࠭୕")))
  else:
    bstack1ll111ll1_opy_ = {}
  bstack1ll111ll1_opy_[md5_hash] = bstack1llll11l1_opy_
  with open(bstack1l111ll11l_opy_, bstack11llll_opy_ (u"ࠦࡼ࠱ࠢୖ")) as outfile:
    json.dump(bstack1ll111ll1_opy_, outfile)
def bstack1llll1l11_opy_(self):
  return
def bstack1l1l11l1l1_opy_(self):
  return
def bstack111111lll_opy_(self):
  global bstack111l1l111_opy_
  bstack111l1l111_opy_(self)
def bstack1ll11l1ll_opy_():
  global bstack1l111111l1_opy_
  bstack1l111111l1_opy_ = True
def bstack111l1ll1l_opy_(self):
  global bstack1ll1ll111l_opy_
  global bstack11ll11lll_opy_
  global bstack1l1111l1l1_opy_
  try:
    if bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬୗ") in bstack1ll1ll111l_opy_ and self.session_id != None and bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ୘"), bstack11llll_opy_ (u"ࠧࠨ୙")) != bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ୚"):
      bstack1ll111lll_opy_ = bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୛") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪଡ଼")
      if bstack1ll111lll_opy_ == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫଢ଼"):
        bstack1lll1ll11l_opy_(logger)
      if self != None:
        bstack111llllll_opy_(self, bstack1ll111lll_opy_, bstack11llll_opy_ (u"ࠬ࠲ࠠࠨ୞").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11llll_opy_ (u"࠭ࠧୟ")
    if bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୠ") in bstack1ll1ll111l_opy_ and getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୡ"), None):
      bstack1111ll1l_opy_.bstack11111ll1_opy_(self, bstack1l1111l1l_opy_, logger, wait=True)
    if bstack11llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩୢ") in bstack1ll1ll111l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack111llllll_opy_(self, bstack11llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥୣ"))
      bstack1lll111ll1_opy_.bstack1ll1l1ll1_opy_(self)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ୤") + str(e))
  bstack1l1111l1l1_opy_(self)
  self.session_id = None
def bstack11lllllll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll111111_opy_
    global bstack1ll1ll111l_opy_
    command_executor = kwargs.get(bstack11llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ୥"), bstack11llll_opy_ (u"࠭ࠧ୦"))
    bstack11l111111_opy_ = False
    if type(command_executor) == str and bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ୧") in command_executor:
      bstack11l111111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ୨") in str(getattr(command_executor, bstack11llll_opy_ (u"ࠩࡢࡹࡷࡲࠧ୩"), bstack11llll_opy_ (u"ࠪࠫ୪"))):
      bstack11l111111_opy_ = True
    else:
      return bstack1l11ll111l_opy_(self, *args, **kwargs)
    if bstack11l111111_opy_:
      if kwargs.get(bstack11llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ୫")):
        kwargs[bstack11llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭୬")] = bstack1ll111111_opy_(kwargs[bstack11llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ୭")], bstack1ll1ll111l_opy_)
      elif kwargs.get(bstack11llll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ୮")):
        kwargs[bstack11llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ୯")] = bstack1ll111111_opy_(kwargs[bstack11llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ୰")], bstack1ll1ll111l_opy_)
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥୱ").format(str(e)))
  return bstack1l11ll111l_opy_(self, *args, **kwargs)
def bstack11ll1lllll_opy_(self, command_executor=bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ୲"), *args, **kwargs):
  bstack11l1lll1l_opy_ = bstack11lllllll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1ll1l111_opy_.on():
    return bstack11l1lll1l_opy_
  try:
    logger.debug(bstack11llll_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ୳").format(str(command_executor)))
    logger.debug(bstack11llll_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ୴").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ୵") in command_executor._url:
      bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ୶"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ୷") in command_executor):
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ୸"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11ll1_opy_.bstack11llllll11_opy_(self)
  return bstack11l1lll1l_opy_
def bstack11lll11111_opy_(args):
  return bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ୹") in str(args)
def bstack11l1ll11ll_opy_(self, driver_command, *args, **kwargs):
  global bstack111l111l1_opy_
  global bstack1ll1l1l1ll_opy_
  bstack1111l1l11_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ୺"), None) and bstack1lll1111_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୻"), None)
  bstack111ll111l_opy_ = getattr(self, bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ୼"), None) != None and getattr(self, bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ୽"), None) == True
  if not bstack1ll1l1l1ll_opy_ and bstack1lll1l1ll1_opy_ and bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ୾") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ୿")] == True and bstack1lll11ll11_opy_.bstack1l1l11ll1l_opy_(driver_command) and (bstack111ll111l_opy_ or bstack1111l1l11_opy_) and not bstack11lll11111_opy_(args):
    try:
      bstack1ll1l1l1ll_opy_ = True
      logger.debug(bstack11llll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭஀").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ஁").format(str(err)))
    bstack1ll1l1l1ll_opy_ = False
  response = bstack111l111l1_opy_(self, driver_command, *args, **kwargs)
  if (bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஂ") in str(bstack1ll1ll111l_opy_).lower() or bstack11llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧஃ") in str(bstack1ll1ll111l_opy_).lower()) and bstack1ll1l111_opy_.on():
    try:
      if driver_command == bstack11llll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ஄"):
        bstack1ll11ll1_opy_.bstack1lll1lll1l_opy_({
            bstack11llll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨஅ"): response[bstack11llll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩஆ")],
            bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫஇ"): bstack1ll11ll1_opy_.current_test_uuid() if bstack1ll11ll1_opy_.current_test_uuid() else bstack1ll1l111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll111llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll11lll_opy_
  global bstack11ll1l1ll1_opy_
  global bstack1l11l1111l_opy_
  global bstack11l1lllll_opy_
  global bstack11l1l1lll1_opy_
  global bstack1ll1ll111l_opy_
  global bstack1l11ll111l_opy_
  global bstack1llll1l1l_opy_
  global bstack1l111lll1l_opy_
  global bstack1l1111l1l_opy_
  CONFIG[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧஈ")] = str(bstack1ll1ll111l_opy_) + str(__version__)
  command_executor = bstack1lllll11l1_opy_()
  logger.debug(bstack11l1l1llll_opy_.format(command_executor))
  proxy = bstack1l1111lll_opy_(CONFIG, proxy)
  bstack111lll1l1_opy_ = 0 if bstack11ll1l1ll1_opy_ < 0 else bstack11ll1l1ll1_opy_
  try:
    if bstack11l1lllll_opy_ is True:
      bstack111lll1l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1l1lll1_opy_ is True:
      bstack111lll1l1_opy_ = int(threading.current_thread().name)
  except:
    bstack111lll1l1_opy_ = 0
  bstack1l11l1lll1_opy_ = bstack11llll1111_opy_(CONFIG, bstack111lll1l1_opy_)
  logger.debug(bstack11l1ll1111_opy_.format(str(bstack1l11l1lll1_opy_)))
  if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪஉ") in CONFIG and bstack11ll1llll_opy_(CONFIG[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫஊ")]):
    bstack11ll1ll11_opy_(bstack1l11l1lll1_opy_)
  if bstack111l111l_opy_.bstack111l1l1ll_opy_(CONFIG, bstack111lll1l1_opy_) and bstack111l111l_opy_.bstack1ll1lll11l_opy_(bstack1l11l1lll1_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack111l111l_opy_.set_capabilities(bstack1l11l1lll1_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1lll1_opy_ = bstack1lll111l11_opy_(desired_capabilities)
    bstack11ll1lll1_opy_[bstack11llll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ஋")] = bstack1l111llll_opy_(CONFIG)
    bstack1l11l11l11_opy_ = bstack11llll1111_opy_(bstack11ll1lll1_opy_)
    if bstack1l11l11l11_opy_:
      bstack1l11l1lll1_opy_ = update(bstack1l11l11l11_opy_, bstack1l11l1lll1_opy_)
    desired_capabilities = None
  if options:
    bstack11l1l11l11_opy_(options, bstack1l11l1lll1_opy_)
  if not options:
    options = bstack1l11lll1l_opy_(bstack1l11l1lll1_opy_)
  bstack1l1111l1l_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஌"))[bstack111lll1l1_opy_]
  if proxy and bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ஍")):
    options.proxy(proxy)
  if options and bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪஎ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l111l11ll_opy_() < version.parse(bstack11llll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫஏ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11l1lll1_opy_)
  logger.info(bstack11ll1111l_opy_)
  if bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ஐ")):
    bstack1l11ll111l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭஑")):
    bstack1l11ll111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨஒ")):
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
    bstack11llll1ll_opy_ = bstack11llll_opy_ (u"ࠩࠪஓ")
    if bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫஔ")):
      bstack11llll1ll_opy_ = self.caps.get(bstack11llll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦக"))
    else:
      bstack11llll1ll_opy_ = self.capabilities.get(bstack11llll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ஖"))
    if bstack11llll1ll_opy_:
      bstack111l1llll_opy_(bstack11llll1ll_opy_)
      if bstack1l111l11ll_opy_() <= version.parse(bstack11llll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭஗")):
        self.command_executor._url = bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ஘") + bstack1ll1l1ll1l_opy_ + bstack11llll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧங")
      else:
        self.command_executor._url = bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦச") + bstack11llll1ll_opy_ + bstack11llll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ஛")
      logger.debug(bstack1l11111111_opy_.format(bstack11llll1ll_opy_))
    else:
      logger.debug(bstack1ll11l1l1l_opy_.format(bstack11llll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧஜ")))
  except Exception as e:
    logger.debug(bstack1ll11l1l1l_opy_.format(e))
  if bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஝") in bstack1ll1ll111l_opy_:
    bstack1lll111ll_opy_(bstack11ll1l1ll1_opy_, bstack1l111lll1l_opy_)
  bstack11ll11lll_opy_ = self.session_id
  if bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ஞ") in bstack1ll1ll111l_opy_ or bstack11llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧட") in bstack1ll1ll111l_opy_ or bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஠") in bstack1ll1ll111l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1ll11ll1_opy_.bstack11llllll11_opy_(self)
  bstack1llll1l1l_opy_.append(self)
  if bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ஡") in CONFIG and bstack11llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ஢") in CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧண")][bstack111lll1l1_opy_]:
    bstack1l11l1111l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨத")][bstack111lll1l1_opy_][bstack11llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ஥")]
  logger.debug(bstack1ll111l1l_opy_.format(bstack11ll11lll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11l1lll11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1ll1l11_opy_
      if(bstack11llll_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤ஦") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪ஧")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩந"), bstack11llll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬன")), bstack11llll_opy_ (u"ࠫࡼ࠭ப")) as fp:
          fp.write(bstack11llll_opy_ (u"ࠧࠨ஫"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ஬")))):
          with open(args[1], bstack11llll_opy_ (u"ࠧࡳࠩ஭")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11llll_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧம") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11111l1l_opy_)
            lines.insert(1, bstack1l11ll1111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦய")), bstack11llll_opy_ (u"ࠪࡻࠬர")) as bstack1l1l1ll1ll_opy_:
              bstack1l1l1ll1ll_opy_.writelines(lines)
        CONFIG[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ற")] = str(bstack1ll1ll111l_opy_) + str(__version__)
        bstack111lll1l1_opy_ = 0 if bstack11ll1l1ll1_opy_ < 0 else bstack11ll1l1ll1_opy_
        try:
          if bstack11l1lllll_opy_ is True:
            bstack111lll1l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1l1lll1_opy_ is True:
            bstack111lll1l1_opy_ = int(threading.current_thread().name)
        except:
          bstack111lll1l1_opy_ = 0
        CONFIG[bstack11llll_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧல")] = False
        CONFIG[bstack11llll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧள")] = True
        bstack1l11l1lll1_opy_ = bstack11llll1111_opy_(CONFIG, bstack111lll1l1_opy_)
        logger.debug(bstack11l1ll1111_opy_.format(str(bstack1l11l1lll1_opy_)))
        if CONFIG.get(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫழ")):
          bstack11ll1ll11_opy_(bstack1l11l1lll1_opy_)
        if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫவ") in CONFIG and bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஶ") in CONFIG[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஷ")][bstack111lll1l1_opy_]:
          bstack1l11l1111l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஸ")][bstack111lll1l1_opy_][bstack11llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪஹ")]
        args.append(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"࠭ࡾࠨ஺")), bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ஻"), bstack11llll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ஼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11l1lll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ஽"))
      bstack1l1ll1l11_opy_ = True
      return bstack1l1l11l11l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1111ll11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11ll1l1ll1_opy_
    global bstack1l11l1111l_opy_
    global bstack11l1lllll_opy_
    global bstack11l1l1lll1_opy_
    global bstack1ll1ll111l_opy_
    CONFIG[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬா")] = str(bstack1ll1ll111l_opy_) + str(__version__)
    bstack111lll1l1_opy_ = 0 if bstack11ll1l1ll1_opy_ < 0 else bstack11ll1l1ll1_opy_
    try:
      if bstack11l1lllll_opy_ is True:
        bstack111lll1l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1l1lll1_opy_ is True:
        bstack111lll1l1_opy_ = int(threading.current_thread().name)
    except:
      bstack111lll1l1_opy_ = 0
    CONFIG[bstack11llll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥி")] = True
    bstack1l11l1lll1_opy_ = bstack11llll1111_opy_(CONFIG, bstack111lll1l1_opy_)
    logger.debug(bstack11l1ll1111_opy_.format(str(bstack1l11l1lll1_opy_)))
    if CONFIG.get(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩீ")):
      bstack11ll1ll11_opy_(bstack1l11l1lll1_opy_)
    if bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩு") in CONFIG and bstack11llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬூ") in CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௃")][bstack111lll1l1_opy_]:
      bstack1l11l1111l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௄")][bstack111lll1l1_opy_][bstack11llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௅")]
    import urllib
    import json
    bstack1l11lll1ll_opy_ = bstack11llll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ெ") + urllib.parse.quote(json.dumps(bstack1l11l1lll1_opy_))
    browser = self.connect(bstack1l11lll1ll_opy_)
    return browser
except Exception as e:
    pass
def bstack11l1l1l11l_opy_():
    global bstack1l1ll1l11_opy_
    global bstack1ll1ll111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111ll11l1_opy_
        if not bstack1lll1l1ll1_opy_:
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
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1lll11_opy_
      bstack1l1ll1l11_opy_ = True
    except Exception as e:
      pass
def bstack11llll111_opy_(context, bstack11ll1l1lll_opy_):
  try:
    context.page.evaluate(bstack11llll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨே"), bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪை")+ json.dumps(bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"ࠢࡾࡿࠥ௉"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨொ"), e)
def bstack1l1ll11l11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11llll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥோ"), bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨௌ") + json.dumps(message) + bstack11llll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀ்ࠧ") + json.dumps(level) + bstack11llll_opy_ (u"ࠬࢃࡽࠨ௎"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ௏"), e)
def bstack11111l111_opy_(self, url):
  global bstack1l111ll1ll_opy_
  try:
    bstack111ll1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1ll1ll1l_opy_.format(str(err)))
  try:
    bstack1l111ll1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll1l11ll_opy_ = str(e)
      if any(err_msg in bstack1lll1l11ll_opy_ for err_msg in bstack1lll11l1l_opy_):
        bstack111ll1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1ll1ll1l_opy_.format(str(err)))
    raise e
def bstack11l1l11lll_opy_(self):
  global bstack1l1111ll1_opy_
  bstack1l1111ll1_opy_ = self
  return
def bstack1l1ll111ll_opy_(self):
  global bstack1ll1lll1l1_opy_
  bstack1ll1lll1l1_opy_ = self
  return
def bstack1l1l1l1111_opy_(test_name, bstack1ll1llllll_opy_):
  global CONFIG
  if CONFIG.get(bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ௐ"), False):
    bstack11l11l1l1_opy_ = os.path.relpath(bstack1ll1llllll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l11l1l1_opy_)
    bstack111l1l1l1_opy_ = suite_name + bstack11llll_opy_ (u"ࠣ࠯ࠥ௑") + test_name
    threading.current_thread().percySessionName = bstack111l1l1l1_opy_
def bstack1l1l1l1lll_opy_(self, test, *args, **kwargs):
  global bstack1l1l11ll11_opy_
  test_name = None
  bstack1ll1llllll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1llllll_opy_ = str(test.source)
  bstack1l1l1l1111_opy_(test_name, bstack1ll1llllll_opy_)
  bstack1l1l11ll11_opy_(self, test, *args, **kwargs)
def bstack11llll1lll_opy_(driver, bstack111l1l1l1_opy_):
  if not bstack1l1l1llll_opy_ and bstack111l1l1l1_opy_:
      bstack1llll11ll1_opy_ = {
          bstack11llll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ௒"): bstack11llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ௓"),
          bstack11llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ௔"): {
              bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௕"): bstack111l1l1l1_opy_
          }
      }
      bstack11l1l1111_opy_ = bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ௖").format(json.dumps(bstack1llll11ll1_opy_))
      driver.execute_script(bstack11l1l1111_opy_)
  if bstack1llll1l1l1_opy_:
      bstack11ll11l1l1_opy_ = {
          bstack11llll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧௗ"): bstack11llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ௘"),
          bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ௙"): {
              bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨ௚"): bstack111l1l1l1_opy_ + bstack11llll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭௛"),
              bstack11llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ௜"): bstack11llll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ௝")
          }
      }
      if bstack1llll1l1l1_opy_.status == bstack11llll_opy_ (u"ࠧࡑࡃࡖࡗࠬ௞"):
          bstack1lll1l111l_opy_ = bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭௟").format(json.dumps(bstack11ll11l1l1_opy_))
          driver.execute_script(bstack1lll1l111l_opy_)
          bstack111llllll_opy_(driver, bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ௠"))
      elif bstack1llll1l1l1_opy_.status == bstack11llll_opy_ (u"ࠪࡊࡆࡏࡌࠨ௡"):
          reason = bstack11llll_opy_ (u"ࠦࠧ௢")
          bstack1111l1l1l_opy_ = bstack111l1l1l1_opy_ + bstack11llll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭௣")
          if bstack1llll1l1l1_opy_.message:
              reason = str(bstack1llll1l1l1_opy_.message)
              bstack1111l1l1l_opy_ = bstack1111l1l1l_opy_ + bstack11llll_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭௤") + reason
          bstack11ll11l1l1_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ௥")] = {
              bstack11llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ௦"): bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ௧"),
              bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨ௨"): bstack1111l1l1l_opy_
          }
          bstack1lll1l111l_opy_ = bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ௩").format(json.dumps(bstack11ll11l1l1_opy_))
          driver.execute_script(bstack1lll1l111l_opy_)
          bstack111llllll_opy_(driver, bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ௪"), reason)
          bstack1ll1lll1l_opy_(reason, str(bstack1llll1l1l1_opy_), str(bstack11ll1l1ll1_opy_), logger)
def bstack1ll111l1ll_opy_(driver, test):
  if CONFIG.get(bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ௫"), False) and CONFIG.get(bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ௬"), bstack11llll_opy_ (u"ࠣࡣࡸࡸࡴࠨ௭")) == bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ௮"):
      bstack11ll1ll1l_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭௯"), None)
      bstack11llllllll_opy_(driver, bstack11ll1ll1l_opy_, test)
  if bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ௰"), None) and bstack1lll1111_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ௱"), None):
      logger.info(bstack11llll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨ௲"))
      bstack111l111l_opy_.bstack111llll1_opy_(driver, name=test.name, path=test.source)
def bstack11ll11l1l_opy_(test, bstack111l1l1l1_opy_):
    try:
      data = {}
      if test:
        data[bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௳")] = bstack111l1l1l1_opy_
      if bstack1llll1l1l1_opy_:
        if bstack1llll1l1l1_opy_.status == bstack11llll_opy_ (u"ࠨࡒࡄࡗࡘ࠭௴"):
          data[bstack11llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ௵")] = bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ௶")
        elif bstack1llll1l1l1_opy_.status == bstack11llll_opy_ (u"ࠫࡋࡇࡉࡍࠩ௷"):
          data[bstack11llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ௸")] = bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௹")
          if bstack1llll1l1l1_opy_.message:
            data[bstack11llll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ௺")] = str(bstack1llll1l1l1_opy_.message)
      user = CONFIG[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ௻")]
      key = CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௼")]
      url = bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨ௽").format(user, key, bstack11ll11lll_opy_)
      headers = {
        bstack11llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ௾"): bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ௿"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l111ll1l1_opy_.format(str(e)))
def bstack1lllll1111_opy_(test, bstack111l1l1l1_opy_):
  global CONFIG
  global bstack1ll1lll1l1_opy_
  global bstack1l1111ll1_opy_
  global bstack11ll11lll_opy_
  global bstack1llll1l1l1_opy_
  global bstack1l11l1111l_opy_
  global bstack1l1ll11ll_opy_
  global bstack1ll1l11ll_opy_
  global bstack1l11111ll_opy_
  global bstack1l1llll11l_opy_
  global bstack1llll1l1l_opy_
  global bstack1l1111l1l_opy_
  try:
    if not bstack11ll11lll_opy_:
      with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"࠭ࡾࠨఀ")), bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఁ"), bstack11llll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪం"))) as f:
        bstack1l111111ll_opy_ = json.loads(bstack11llll_opy_ (u"ࠤࡾࠦః") + f.read().strip() + bstack11llll_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬఄ") + bstack11llll_opy_ (u"ࠦࢂࠨఅ"))
        bstack11ll11lll_opy_ = bstack1l111111ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll1l1l_opy_:
    for driver in bstack1llll1l1l_opy_:
      if bstack11ll11lll_opy_ == driver.session_id:
        if test:
          bstack1ll111l1ll_opy_(driver, test)
        bstack11llll1lll_opy_(driver, bstack111l1l1l1_opy_)
  elif bstack11ll11lll_opy_:
    bstack11ll11l1l_opy_(test, bstack111l1l1l1_opy_)
  if bstack1ll1lll1l1_opy_:
    bstack1ll1l11ll_opy_(bstack1ll1lll1l1_opy_)
  if bstack1l1111ll1_opy_:
    bstack1l11111ll_opy_(bstack1l1111ll1_opy_)
  if bstack1l111111l1_opy_:
    bstack1l1llll11l_opy_()
def bstack111l1111l_opy_(self, test, *args, **kwargs):
  bstack111l1l1l1_opy_ = None
  if test:
    bstack111l1l1l1_opy_ = str(test.name)
  bstack1lllll1111_opy_(test, bstack111l1l1l1_opy_)
  bstack1l1ll11ll_opy_(self, test, *args, **kwargs)
def bstack11ll1llll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1l1ll11_opy_
  global CONFIG
  global bstack1llll1l1l_opy_
  global bstack11ll11lll_opy_
  bstack1l1111l111_opy_ = None
  try:
    if bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫఆ"), None):
      try:
        if not bstack11ll11lll_opy_:
          with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"࠭ࡾࠨఇ")), bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఈ"), bstack11llll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪఉ"))) as f:
            bstack1l111111ll_opy_ = json.loads(bstack11llll_opy_ (u"ࠤࡾࠦఊ") + f.read().strip() + bstack11llll_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬఋ") + bstack11llll_opy_ (u"ࠦࢂࠨఌ"))
            bstack11ll11lll_opy_ = bstack1l111111ll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1llll1l1l_opy_:
        for driver in bstack1llll1l1l_opy_:
          if bstack11ll11lll_opy_ == driver.session_id:
            bstack1l1111l111_opy_ = driver
    bstack1ll11l1l11_opy_ = bstack111l111l_opy_.bstack1lll11lll_opy_(test.tags)
    if bstack1l1111l111_opy_:
      threading.current_thread().isA11yTest = bstack111l111l_opy_.bstack1l11l1l111_opy_(bstack1l1111l111_opy_, bstack1ll11l1l11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll11l1l11_opy_
  except:
    pass
  bstack11l1l1ll11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llll1l1l1_opy_
  bstack1llll1l1l1_opy_ = self._test
def bstack1l1lll111l_opy_():
  global bstack1111llll1_opy_
  try:
    if os.path.exists(bstack1111llll1_opy_):
      os.remove(bstack1111llll1_opy_)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ఍") + str(e))
def bstack1ll1ll111_opy_():
  global bstack1111llll1_opy_
  bstack11l1llll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1111llll1_opy_):
      with open(bstack1111llll1_opy_, bstack11llll_opy_ (u"࠭ࡷࠨఎ")):
        pass
      with open(bstack1111llll1_opy_, bstack11llll_opy_ (u"ࠢࡸ࠭ࠥఏ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1111llll1_opy_):
      bstack11l1llll1_opy_ = json.load(open(bstack1111llll1_opy_, bstack11llll_opy_ (u"ࠨࡴࡥࠫఐ")))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ఑") + str(e))
  finally:
    return bstack11l1llll1_opy_
def bstack1lll111ll_opy_(platform_index, item_index):
  global bstack1111llll1_opy_
  try:
    bstack11l1llll1_opy_ = bstack1ll1ll111_opy_()
    bstack11l1llll1_opy_[item_index] = platform_index
    with open(bstack1111llll1_opy_, bstack11llll_opy_ (u"ࠥࡻ࠰ࠨఒ")) as outfile:
      json.dump(bstack11l1llll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩఓ") + str(e))
def bstack111llll1l_opy_(bstack1lll1ll1l_opy_):
  global CONFIG
  bstack1llll1ll11_opy_ = bstack11llll_opy_ (u"ࠬ࠭ఔ")
  if not bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩక") in CONFIG:
    logger.info(bstack11llll_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫఖ"))
  try:
    platform = CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫగ")][bstack1lll1ll1l_opy_]
    if bstack11llll_opy_ (u"ࠩࡲࡷࠬఘ") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"ࠪࡳࡸ࠭ఙ")]) + bstack11llll_opy_ (u"ࠫ࠱ࠦࠧచ")
    if bstack11llll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨఛ") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩజ")]) + bstack11llll_opy_ (u"ࠧ࠭ࠢࠪఝ")
    if bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬఞ") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ట")]) + bstack11llll_opy_ (u"ࠪ࠰ࠥ࠭ఠ")
    if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭డ") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧఢ")]) + bstack11llll_opy_ (u"࠭ࠬࠡࠩణ")
    if bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬత") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭థ")]) + bstack11llll_opy_ (u"ࠩ࠯ࠤࠬద")
    if bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫధ") in platform:
      bstack1llll1ll11_opy_ += str(platform[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬన")]) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠨ఩")
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ప") + str(e))
  finally:
    if bstack1llll1ll11_opy_[len(bstack1llll1ll11_opy_) - 2:] == bstack11llll_opy_ (u"ࠧ࠭ࠢࠪఫ"):
      bstack1llll1ll11_opy_ = bstack1llll1ll11_opy_[:-2]
    return bstack1llll1ll11_opy_
def bstack1llll11111_opy_(path, bstack1llll1ll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1111l11ll_opy_ = ET.parse(path)
    bstack1l11l11lll_opy_ = bstack1111l11ll_opy_.getroot()
    bstack1llll11l11_opy_ = None
    for suite in bstack1l11l11lll_opy_.iter(bstack11llll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧబ")):
      if bstack11llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩభ") in suite.attrib:
        suite.attrib[bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨమ")] += bstack11llll_opy_ (u"ࠫࠥ࠭య") + bstack1llll1ll11_opy_
        bstack1llll11l11_opy_ = suite
    bstack111ll1111_opy_ = None
    for robot in bstack1l11l11lll_opy_.iter(bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫర")):
      bstack111ll1111_opy_ = robot
    bstack1ll11ll1l_opy_ = len(bstack111ll1111_opy_.findall(bstack11llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬఱ")))
    if bstack1ll11ll1l_opy_ == 1:
      bstack111ll1111_opy_.remove(bstack111ll1111_opy_.findall(bstack11llll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ల"))[0])
      bstack11llll1l1l_opy_ = ET.Element(bstack11llll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧళ"), attrib={bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧఴ"): bstack11llll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪవ"), bstack11llll_opy_ (u"ࠫ࡮ࡪࠧశ"): bstack11llll_opy_ (u"ࠬࡹ࠰ࠨష")})
      bstack111ll1111_opy_.insert(1, bstack11llll1l1l_opy_)
      bstack1ll11l11l1_opy_ = None
      for suite in bstack111ll1111_opy_.iter(bstack11llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬస")):
        bstack1ll11l11l1_opy_ = suite
      bstack1ll11l11l1_opy_.append(bstack1llll11l11_opy_)
      bstack1ll11llll1_opy_ = None
      for status in bstack1llll11l11_opy_.iter(bstack11llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧహ")):
        bstack1ll11llll1_opy_ = status
      bstack1ll11l11l1_opy_.append(bstack1ll11llll1_opy_)
    bstack1111l11ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭఺") + str(e))
def bstack1ll1l111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll1111ll1_opy_
  global CONFIG
  if bstack11llll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ఻") in options:
    del options[bstack11llll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮఼ࠢ")]
  bstack1ll1lll1ll_opy_ = bstack1ll1ll111_opy_()
  for bstack1ll1l1l11_opy_ in bstack1ll1lll1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫఽ"), str(bstack1ll1l1l11_opy_), bstack11llll_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩా"))
    bstack1llll11111_opy_(path, bstack111llll1l_opy_(bstack1ll1lll1ll_opy_[bstack1ll1l1l11_opy_]))
  bstack1l1lll111l_opy_()
  return bstack1ll1111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l11llllll_opy_(self, ff_profile_dir):
  global bstack1lll1llll_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll1llll_opy_(self, ff_profile_dir)
def bstack1111l1ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1llllll_opy_
  bstack1l11ll11l1_opy_ = []
  if bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩి") in CONFIG:
    bstack1l11ll11l1_opy_ = CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪీ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11llll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤు")],
      pabot_args[bstack11llll_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥూ")],
      argfile,
      pabot_args.get(bstack11llll_opy_ (u"ࠥ࡬࡮ࡼࡥࠣృ")),
      pabot_args[bstack11llll_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢౄ")],
      platform[0],
      bstack1l1llllll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11llll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ౅")] or [(bstack11llll_opy_ (u"ࠨࠢె"), None)]
    for platform in enumerate(bstack1l11ll11l1_opy_)
  ]
def bstack11ll111lll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l1l1l11_opy_=bstack11llll_opy_ (u"ࠧࠨే")):
  global bstack1ll1111lll_opy_
  self.platform_index = platform_index
  self.bstack1l111ll1l_opy_ = bstack11l1l1l11_opy_
  bstack1ll1111lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1111ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll111l11l_opy_
  global bstack1lllllll1l_opy_
  bstack11llll1l11_opy_ = copy.deepcopy(item)
  if not bstack11llll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪై") in item.options:
    bstack11llll1l11_opy_.options[bstack11llll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ౉")] = []
  bstack11l11111l_opy_ = bstack11llll1l11_opy_.options[bstack11llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬొ")].copy()
  for v in bstack11llll1l11_opy_.options[bstack11llll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ో")]:
    if bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫౌ") in v:
      bstack11l11111l_opy_.remove(v)
    if bstack11llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ్࠭") in v:
      bstack11l11111l_opy_.remove(v)
    if bstack11llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ౎") in v:
      bstack11l11111l_opy_.remove(v)
  bstack11l11111l_opy_.insert(0, bstack11llll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ౏").format(bstack11llll1l11_opy_.platform_index))
  bstack11l11111l_opy_.insert(0, bstack11llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩ౐").format(bstack11llll1l11_opy_.bstack1l111ll1l_opy_))
  bstack11llll1l11_opy_.options[bstack11llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౑")] = bstack11l11111l_opy_
  if bstack1lllllll1l_opy_:
    bstack11llll1l11_opy_.options[bstack11llll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭౒")].insert(0, bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ౓").format(bstack1lllllll1l_opy_))
  return bstack1ll111l11l_opy_(caller_id, datasources, is_last, bstack11llll1l11_opy_, outs_dir)
def bstack11l1lll1ll_opy_(command, item_index):
  if bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ౔")):
    os.environ[bstack11llll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨౕ")] = json.dumps(CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶౖࠫ")][item_index % bstack11ll1111ll_opy_])
  global bstack1lllllll1l_opy_
  if bstack1lllllll1l_opy_:
    command[0] = command[0].replace(bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౗"), bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧౘ") + str(
      item_index) + bstack11llll_opy_ (u"ࠫࠥ࠭ౙ") + bstack1lllllll1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫౚ"),
                                    bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ౛") + str(item_index), 1)
def bstack1ll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11ll11ll11_opy_
  bstack11l1lll1ll_opy_(command, item_index)
  return bstack11ll11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1llll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11ll11ll11_opy_
  bstack11l1lll1ll_opy_(command, item_index)
  return bstack11ll11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l111lll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11ll11ll11_opy_
  bstack11l1lll1ll_opy_(command, item_index)
  return bstack11ll11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1lll11l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1ll1111_opy_
  bstack1lllllll11_opy_ = bstack1ll1ll1111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11llll_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ౜")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11llll_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬౝ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lllllll11_opy_
def bstack1ll1111l1l_opy_(runner, hook_name, context, element, bstack11ll11111_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1lll111l1l_opy_.bstack1lll1l11_opy_(hook_name, element)
    bstack11ll11111_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1lll111l1l_opy_.bstack1lll1lll_opy_(element)
      if hook_name not in [bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭౞"), bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭౟")] and args and hasattr(args[0], bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫౠ")):
        args[0].error_message = bstack11llll_opy_ (u"ࠬ࠭ౡ")
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨౢ").format(str(e)))
def bstack11l1ll11l_opy_(runner, name, context, bstack11ll11111_opy_, *args):
    bstack1ll1111l1l_opy_(runner, name, context, runner, bstack11ll11111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l11lllll_opy_(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ౣ")) else context.browser
      runner.driver_initialised = bstack11llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ౤")
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭౥").format(str(e)))
def bstack1ll11l1l1_opy_(runner, name, context, bstack11ll11111_opy_, *args):
    bstack1ll1111l1l_opy_(runner, name, context, context.feature, bstack11ll11111_opy_, *args)
    try:
      if not bstack1l1l1llll_opy_:
        bstack1l1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lllll_opy_(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ౦")) else context.browser
        if is_driver_active(bstack1l1111l111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ౧")
          bstack11ll1l1lll_opy_ = str(runner.feature.name)
          bstack11llll111_opy_(context, bstack11ll1l1lll_opy_)
          bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ౨") + json.dumps(bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"࠭ࡽࡾࠩ౩"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ౪").format(str(e)))
def bstack111ll1lll_opy_(runner, name, context, bstack11ll11111_opy_, *args):
    bstack1lll111l1l_opy_.start_test(args[0].name, args[0])
    bstack1ll1111l1l_opy_(runner, name, context, context.scenario, bstack11ll11111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1lll111ll1_opy_.bstack1lll11111l_opy_(context, *args)
    try:
      bstack1l1111l111_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ౫"), context.browser)
      if is_driver_active(bstack1l1111l111_opy_):
        bstack1ll11ll1_opy_.bstack11llllll11_opy_(bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౬"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ౭")
        if (not bstack1l1l1llll_opy_):
          scenario_name = args[0].name
          feature_name = bstack11ll1l1lll_opy_ = str(runner.feature.name)
          bstack11ll1l1lll_opy_ = feature_name + bstack11llll_opy_ (u"ࠫࠥ࠳ࠠࠨ౮") + scenario_name
          if runner.driver_initialised == bstack11llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౯"):
            bstack11llll111_opy_(context, bstack11ll1l1lll_opy_)
            bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ౰") + json.dumps(bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"ࠧࡾࡿࠪ౱"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ౲").format(str(e)))
def bstack11ll1ll111_opy_(runner, name, context, bstack11ll11111_opy_, *args):
    bstack1ll1111l1l_opy_(runner, name, context, args[0], bstack11ll11111_opy_, *args)
    try:
      bstack1l1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lllll_opy_(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౳")) else context.browser
      if is_driver_active(bstack1l1111l111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ౴")
        bstack1lll111l1l_opy_.bstack1lll1ll1_opy_(args[0])
        if runner.driver_initialised == bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ౵"):
          feature_name = bstack11ll1l1lll_opy_ = str(runner.feature.name)
          bstack11ll1l1lll_opy_ = feature_name + bstack11llll_opy_ (u"ࠬࠦ࠭ࠡࠩ౶") + context.scenario.name
          bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ౷") + json.dumps(bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"ࠧࡾࡿࠪ౸"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ౹").format(str(e)))
def bstack1llll1l111_opy_(runner, name, context, bstack11ll11111_opy_, *args):
  bstack1lll111l1l_opy_.bstack1l1l1l11_opy_(args[0])
  try:
    bstack11ll1ll11l_opy_ = args[0].status.name
    bstack1l1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ౺") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1111l111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11llll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ౻")
        feature_name = bstack11ll1l1lll_opy_ = str(runner.feature.name)
        bstack11ll1l1lll_opy_ = feature_name + bstack11llll_opy_ (u"ࠫࠥ࠳ࠠࠨ౼") + context.scenario.name
        bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ౽") + json.dumps(bstack11ll1l1lll_opy_) + bstack11llll_opy_ (u"࠭ࡽࡾࠩ౾"))
    if str(bstack11ll1ll11l_opy_).lower() == bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౿"):
      bstack111lllll1_opy_ = bstack11llll_opy_ (u"ࠨࠩಀ")
      bstack1ll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠩࠪಁ")
      bstack11lll1ll1_opy_ = bstack11llll_opy_ (u"ࠪࠫಂ")
      try:
        import traceback
        bstack111lllll1_opy_ = runner.exception.__class__.__name__
        bstack1llll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠫࠥ࠭ಃ").join(bstack1llll111_opy_)
        bstack11lll1ll1_opy_ = bstack1llll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l1ll1l_opy_.format(str(e)))
      bstack111lllll1_opy_ += bstack11lll1ll1_opy_
      bstack1l1ll11l11_opy_(context, json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ಄") + str(bstack1ll1l1l1l_opy_)),
                          bstack11llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಅ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧಆ"):
        bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ಇ"), None), bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤಈ"), bstack111lllll1_opy_)
        bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨಉ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥಊ") + str(bstack1ll1l1l1l_opy_)) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬಋ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦಌ"):
        bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ಍"), bstack11llll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧಎ") + str(bstack111lllll1_opy_))
    else:
      bstack1l1ll11l11_opy_(context, bstack11llll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥಏ"), bstack11llll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣಐ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ಑"):
        bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠬࡶࡡࡨࡧࠪಒ"), None), bstack11llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨಓ"))
      bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬಔ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧಕ")) + bstack11llll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨಖ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣಗ"):
        bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦಘ"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫಙ").format(str(e)))
  bstack1ll1111l1l_opy_(runner, name, context, args[0], bstack11ll11111_opy_, *args)
def bstack11ll11llll_opy_(runner, name, context, bstack11ll11111_opy_, *args):
  bstack1lll111l1l_opy_.end_test(args[0])
  try:
    bstack1lll11ll1l_opy_ = args[0].status.name
    bstack1l1111l111_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬಚ"), context.browser)
    bstack1lll111ll1_opy_.bstack1ll1l1ll1_opy_(bstack1l1111l111_opy_)
    if str(bstack1lll11ll1l_opy_).lower() == bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಛ"):
      bstack111lllll1_opy_ = bstack11llll_opy_ (u"ࠨࠩಜ")
      bstack1ll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠩࠪಝ")
      bstack11lll1ll1_opy_ = bstack11llll_opy_ (u"ࠪࠫಞ")
      try:
        import traceback
        bstack111lllll1_opy_ = runner.exception.__class__.__name__
        bstack1llll111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠫࠥ࠭ಟ").join(bstack1llll111_opy_)
        bstack11lll1ll1_opy_ = bstack1llll111_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l1ll1l_opy_.format(str(e)))
      bstack111lllll1_opy_ += bstack11lll1ll1_opy_
      bstack1l1ll11l11_opy_(context, json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦಠ") + str(bstack1ll1l1l1l_opy_)),
                          bstack11llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಡ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤಢ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಣ"):
        bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧತ"), None), bstack11llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥಥ"), bstack111lllll1_opy_)
        bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩದ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦಧ") + str(bstack1ll1l1l1l_opy_)) + bstack11llll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ನ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ಩") or runner.driver_initialised == bstack11llll_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨಪ"):
        bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩಫ"), bstack11llll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢಬ") + str(bstack111lllll1_opy_))
    else:
      bstack1l1ll11l11_opy_(context, bstack11llll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧಭ"), bstack11llll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥಮ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಯ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧರ"):
        bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ಱ"), None), bstack11llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤಲ"))
      bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨಳ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ಴")) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫವ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಶ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧಷ"):
        bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಸ"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫಹ").format(str(e)))
  bstack1ll1111l1l_opy_(runner, name, context, context.scenario, bstack11ll11111_opy_, *args)
  threading.current_thread().current_test_uuid = None
def bstack111lll11l_opy_(runner, name, context, bstack11ll11111_opy_, *args):
    try:
      bstack1l1111l111_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ಺"), context.browser)
      if context.failed is True:
        bstack1111l1111_opy_ = []
        bstack11lll11lll_opy_ = []
        bstack1l11111l1_opy_ = []
        bstack1lll11l11l_opy_ = bstack11llll_opy_ (u"ࠫࠬ಻")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1111l1111_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1llll111_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1lllll_opy_ = bstack11llll_opy_ (u"಼ࠬࠦࠧ").join(bstack1llll111_opy_)
            bstack11lll11lll_opy_.append(bstack1ll1lllll_opy_)
            bstack1l11111l1_opy_.append(bstack1llll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11l1ll1l_opy_.format(str(e)))
        bstack111lllll1_opy_ = bstack11llll_opy_ (u"࠭ࠧಽ")
        for i in range(len(bstack1111l1111_opy_)):
          bstack111lllll1_opy_ += bstack1111l1111_opy_[i] + bstack1l11111l1_opy_[i] + bstack11llll_opy_ (u"ࠧ࡝ࡰࠪಾ")
        bstack1lll11l11l_opy_ = bstack11llll_opy_ (u"ࠨࠢࠪಿ").join(bstack11lll11lll_opy_)
        if runner.driver_initialised in [bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥೀ"), bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢು")]:
          bstack1l1ll11l11_opy_(context, bstack1lll11l11l_opy_, bstack11llll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥೂ"))
          bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠬࡶࡡࡨࡧࠪೃ"), None), bstack11llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨೄ"), bstack111lllll1_opy_)
          bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ೅") + json.dumps(bstack1lll11l11l_opy_) + bstack11llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨೆ"))
          bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤೇ"), bstack11llll_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣೈ") + str(bstack111lllll1_opy_))
          bstack1l1l111l1l_opy_ = bstack1l11l1l1ll_opy_(bstack1lll11l11l_opy_, runner.feature.name, logger)
          if (bstack1l1l111l1l_opy_ != None):
            bstack1lll1l11l_opy_.append(bstack1l1l111l1l_opy_)
      else:
        if runner.driver_initialised in [bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ೉"), bstack11llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤೊ")]:
          bstack1l1ll11l11_opy_(context, bstack11llll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤೋ") + str(runner.feature.name) + bstack11llll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤೌ"), bstack11llll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ್"))
          bstack1ll1ll1lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ೎"), None), bstack11llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ೏"))
          bstack1l1111l111_opy_.execute_script(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ೐") + json.dumps(bstack11llll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ೑") + str(runner.feature.name) + bstack11llll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ೒")) + bstack11llll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭೓"))
          bstack111llllll_opy_(bstack1l1111l111_opy_, bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ೔"))
          bstack1l1l111l1l_opy_ = bstack1l11l1l1ll_opy_(bstack1lll11l11l_opy_, runner.feature.name, logger)
          if (bstack1l1l111l1l_opy_ != None):
            bstack1lll1l11l_opy_.append(bstack1l1l111l1l_opy_)
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫೕ").format(str(e)))
    bstack1ll1111l1l_opy_(runner, name, context, context.feature, bstack11ll11111_opy_, *args)
def bstack11lll1l1l_opy_(self, name, context, *args):
  if bstack1lll1l1ll1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack11ll1111ll_opy_
    bstack1lll1l1l1_opy_ = CONFIG[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೖ")][platform_index]
    os.environ[bstack11llll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ೗")] = json.dumps(bstack1lll1l1l1_opy_)
  global bstack11ll11111_opy_
  if not hasattr(self, bstack11llll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࡦࠪ೘")):
    self.driver_initialised = None
  bstack1ll1ll11l1_opy_ = {
      bstack11llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ೙"): bstack11l1ll11l_opy_,
      bstack11llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ೚"): bstack1ll11l1l1_opy_,
      bstack11llll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬ೛"): lambda *args: bstack1ll1111l1l_opy_(*args, context.scenario),
      bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೜"): bstack111ll1lll_opy_,
      bstack11llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠨೝ"): bstack11ll1ll111_opy_,
      bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡹ࡫ࡰࠨೞ"): bstack1llll1l111_opy_,
      bstack11llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭೟"): bstack11ll11llll_opy_,
      bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩೠ"): lambda *args: bstack1ll1111l1l_opy_(*args, context.scenario),
      bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧೡ"): bstack111lll11l_opy_,
      bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫೢ"): lambda *args: bstack1ll1111l1l_opy_(*args, self)
  }
  handler = bstack1ll1ll11l1_opy_.get(name, bstack11ll11111_opy_)
  handler(self, name, context, bstack11ll11111_opy_, *args)
  if name in [bstack11llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩೣ"), bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೤"), bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ೥")]:
    try:
      bstack1l1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lllll_opy_(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೦")) else context.browser
      bstack1l1l111ll1_opy_ = (
        (name == bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ೧") and self.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ೨")) or
        (name == bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ೩") and self.driver_initialised == bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ೪")) or
        (name == bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೫") and self.driver_initialised in [bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ೬"), bstack11llll_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧ೭")]) or
        (name == bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪ೮") and self.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೯"))
      )
      if bstack1l1l111ll1_opy_:
        self.driver_initialised = None
        bstack1l1111l111_opy_.quit()
    except Exception:
      pass
def bstack1ll11lll1_opy_(config, startdir):
  return bstack11llll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨ೰").format(bstack11llll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣೱ"))
notset = Notset()
def bstack1llllllll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11lll1llll_opy_
  if str(name).lower() == bstack11llll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪೲ"):
    return bstack11llll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥೳ")
  else:
    return bstack11lll1llll_opy_(self, name, default, skip)
def bstack1llllll1ll_opy_(item, when):
  global bstack1l1l1111ll_opy_
  try:
    bstack1l1l1111ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1lll11l111_opy_():
  return
def bstack11ll11l11l_opy_(type, name, status, reason, bstack1l111l111l_opy_, bstack1l11l11l1l_opy_):
  bstack1llll11ll1_opy_ = {
    bstack11llll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ೴"): type,
    bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೵"): {}
  }
  if type == bstack11llll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ೶"):
    bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ೷")][bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ೸")] = bstack1l111l111l_opy_
    bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭೹")][bstack11llll_opy_ (u"ࠫࡩࡧࡴࡢࠩ೺")] = json.dumps(str(bstack1l11l11l1l_opy_))
  if type == bstack11llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭೻"):
    bstack1llll11ll1_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ೼")][bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೽")] = name
  if type == bstack11llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ೾"):
    bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ೿")][bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪഀ")] = status
    if status == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഁ"):
      bstack1llll11ll1_opy_[bstack11llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨം")][bstack11llll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ഃ")] = json.dumps(str(reason))
  bstack11l1l1111_opy_ = bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬഄ").format(json.dumps(bstack1llll11ll1_opy_))
  return bstack11l1l1111_opy_
def bstack1l11llll1_opy_(driver_command, response):
    if driver_command == bstack11llll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬഅ"):
        bstack1ll11ll1_opy_.bstack1lll1lll1l_opy_({
            bstack11llll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨആ"): response[bstack11llll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩഇ")],
            bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫഈ"): bstack1ll11ll1_opy_.current_test_uuid()
        })
def bstack11lllll1l1_opy_(item, call, rep):
  global bstack1l1ll1lll1_opy_
  global bstack1llll1l1l_opy_
  global bstack1l1l1llll_opy_
  name = bstack11llll_opy_ (u"ࠬ࠭ഉ")
  try:
    if rep.when == bstack11llll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫഊ"):
      bstack11ll11lll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1l1llll_opy_:
          name = str(rep.nodeid)
          bstack1l11lll11l_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨഋ"), name, bstack11llll_opy_ (u"ࠨࠩഌ"), bstack11llll_opy_ (u"ࠩࠪ഍"), bstack11llll_opy_ (u"ࠪࠫഎ"), bstack11llll_opy_ (u"ࠫࠬഏ"))
          threading.current_thread().bstack1ll111lll1_opy_ = name
          for driver in bstack1llll1l1l_opy_:
            if bstack11ll11lll_opy_ == driver.session_id:
              driver.execute_script(bstack1l11lll11l_opy_)
      except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬഐ").format(str(e)))
      try:
        bstack1l1l111l11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ഑"):
          status = bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഒ") if rep.outcome.lower() == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഓ") else bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩഔ")
          reason = bstack11llll_opy_ (u"ࠪࠫക")
          if status == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫഖ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11llll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪഗ") if status == bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ഘ") else bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ങ")
          data = name + bstack11llll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪച") if status == bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩഛ") else name + bstack11llll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ജ") + reason
          bstack1ll11l1111_opy_ = bstack11ll11l11l_opy_(bstack11llll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ഝ"), bstack11llll_opy_ (u"ࠬ࠭ഞ"), bstack11llll_opy_ (u"࠭ࠧട"), bstack11llll_opy_ (u"ࠧࠨഠ"), level, data)
          for driver in bstack1llll1l1l_opy_:
            if bstack11ll11lll_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11l1111_opy_)
      except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬഡ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ഢ").format(str(e)))
  bstack1l1ll1lll1_opy_(item, call, rep)
def bstack11llllllll_opy_(driver, bstack11lllll11l_opy_, test=None):
  global bstack11ll1l1ll1_opy_
  if test != None:
    bstack1l1l1ll1l1_opy_ = test.get(bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨണ"), bstack11llll_opy_ (u"ࠫࠬത"))
    bstack11ll1l1l11_opy_ = test.get(bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪഥ"), bstack11llll_opy_ (u"࠭ࠧദ"))
    PercySDK.screenshot(driver, bstack11lllll11l_opy_, bstack1l1l1ll1l1_opy_=bstack1l1l1ll1l1_opy_, bstack11ll1l1l11_opy_=bstack11ll1l1l11_opy_, bstack1ll1l11l1l_opy_=bstack11ll1l1ll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack11lllll11l_opy_)
def bstack1ll1ll1l1l_opy_(driver):
  if bstack1l1ll1l111_opy_.bstack1l1lll111_opy_() is True or bstack1l1ll1l111_opy_.capturing() is True:
    return
  bstack1l1ll1l111_opy_.bstack1ll111l11_opy_()
  while not bstack1l1ll1l111_opy_.bstack1l1lll111_opy_():
    bstack111l11l11_opy_ = bstack1l1ll1l111_opy_.bstack1l1111lll1_opy_()
    bstack11llllllll_opy_(driver, bstack111l11l11_opy_)
  bstack1l1ll1l111_opy_.bstack1ll111111l_opy_()
def bstack1l1lll1ll1_opy_(sequence, driver_command, response = None, bstack11llll1l1_opy_ = None, args = None):
    try:
      if sequence != bstack11llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧധ"):
        return
      if not CONFIG.get(bstack11llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧന"), False):
        return
      bstack111l11l11_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬഩ"), None)
      for command in bstack1l1111l11_opy_:
        if command == driver_command:
          for driver in bstack1llll1l1l_opy_:
            bstack1ll1ll1l1l_opy_(driver)
      bstack1l1llll1l_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭പ"), bstack11llll_opy_ (u"ࠦࡦࡻࡴࡰࠤഫ"))
      if driver_command in bstack1l111lllll_opy_[bstack1l1llll1l_opy_]:
        bstack1l1ll1l111_opy_.bstack11l11l11l_opy_(bstack111l11l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack11llll111l_opy_(framework_name):
  global bstack1ll1ll111l_opy_
  global bstack1l1ll1l11_opy_
  global bstack1lllll111l_opy_
  bstack1ll1ll111l_opy_ = framework_name
  logger.info(bstack111ll1l1l_opy_.format(bstack1ll1ll111l_opy_.split(bstack11llll_opy_ (u"ࠬ࠳ࠧബ"))[0]))
  bstack11l1l111l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lll1l1ll1_opy_:
      Service.start = bstack1llll1l11_opy_
      Service.stop = bstack1l1l11l1l1_opy_
      webdriver.Remote.get = bstack11111l111_opy_
      WebDriver.close = bstack111111lll_opy_
      WebDriver.quit = bstack111l1ll1l_opy_
      webdriver.Remote.__init__ = bstack1ll111llll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1lll1l1ll1_opy_:
        webdriver.Remote.__init__ = bstack11ll1lllll_opy_
    WebDriver.execute = bstack11l1ll11ll_opy_
    bstack1l1ll1l11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1lll1l1ll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1ll11l1ll_opy_
  except Exception as e:
    pass
  bstack11l1l1l11l_opy_()
  if not bstack1l1ll1l11_opy_:
    bstack1111ll11l_opy_(bstack11llll_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣഭ"), bstack11lll1ll11_opy_)
  if bstack11ll11111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11lll1111l_opy_
    except Exception as e:
      logger.error(bstack1l1ll1lll_opy_.format(str(e)))
  if bstack1lll1l1l11_opy_():
    bstack1ll1l1l1l1_opy_(CONFIG, logger)
  if (bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭മ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack11llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧയ"), False):
          bstack1l1l1l11l1_opy_(bstack1l1lll1ll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l11llllll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1ll111ll_opy_
      except Exception as e:
        logger.warn(bstack11llllll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11l1l11lll_opy_
      except Exception as e:
        logger.debug(bstack11l1l1ll1l_opy_ + str(e))
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11llllll1l_opy_)
    Output.start_test = bstack1l1l1l1lll_opy_
    Output.end_test = bstack111l1111l_opy_
    TestStatus.__init__ = bstack11ll1llll1_opy_
    QueueItem.__init__ = bstack11ll111lll_opy_
    pabot._create_items = bstack1111l1ll1_opy_
    try:
      from pabot import __version__ as bstack11ll111111_opy_
      if version.parse(bstack11ll111111_opy_) >= version.parse(bstack11llll_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩര")):
        pabot._run = bstack1l111lll11_opy_
      elif version.parse(bstack11ll111111_opy_) >= version.parse(bstack11llll_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪറ")):
        pabot._run = bstack1ll1llll1l_opy_
      else:
        pabot._run = bstack1ll1l1lll_opy_
    except Exception as e:
      pabot._run = bstack1ll1l1lll_opy_
    pabot._create_command_for_execution = bstack1lll1111ll_opy_
    pabot._report_results = bstack1ll1l111l_opy_
  if bstack11llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫല") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11lll111ll_opy_)
    Runner.run_hook = bstack11lll1l1l_opy_
    Step.run = bstack1l1lll11l1_opy_
  if bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬള") in str(framework_name).lower():
    if not bstack1lll1l1ll1_opy_:
      return
    try:
      if CONFIG.get(bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬഴ"), False):
          bstack1l1l1l11l1_opy_(bstack1l1lll1ll1_opy_)
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
def bstack111l1ll11_opy_():
  global CONFIG
  if bstack11llll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧവ") in CONFIG and int(CONFIG[bstack11llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨശ")]) > 1:
    logger.warn(bstack1ll1lll11_opy_)
def bstack11l1l11ll1_opy_(arg, bstack1111l111_opy_, bstack1ll111l1l1_opy_=None):
  global CONFIG
  global bstack1ll1l1ll1l_opy_
  global bstack11l1llllll_opy_
  global bstack1lll1l1ll1_opy_
  global bstack1111111l_opy_
  bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഷ")
  if bstack1111l111_opy_ and isinstance(bstack1111l111_opy_, str):
    bstack1111l111_opy_ = eval(bstack1111l111_opy_)
  CONFIG = bstack1111l111_opy_[bstack11llll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪസ")]
  bstack1ll1l1ll1l_opy_ = bstack1111l111_opy_[bstack11llll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഹ")]
  bstack11l1llllll_opy_ = bstack1111l111_opy_[bstack11llll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧഺ")]
  bstack1lll1l1ll1_opy_ = bstack1111l111_opy_[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏ഻ࠩ")]
  bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ഼"), bstack1lll1l1ll1_opy_)
  os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪഽ")] = bstack1l1l1lllll_opy_
  os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨാ")] = json.dumps(CONFIG)
  os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪി")] = bstack1ll1l1ll1l_opy_
  os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬീ")] = str(bstack11l1llllll_opy_)
  os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫു")] = str(True)
  if bstack1ll11l11l_opy_(arg, [bstack11llll_opy_ (u"࠭࠭࡯ࠩൂ"), bstack11llll_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨൃ")]) != -1:
    os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩൄ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11lll11l1l_opy_)
    return
  bstack1l11l11ll1_opy_()
  global bstack1l11l11ll_opy_
  global bstack11ll1l1ll1_opy_
  global bstack1l1llllll_opy_
  global bstack1lllllll1l_opy_
  global bstack1l11l111ll_opy_
  global bstack1lllll111l_opy_
  global bstack11l1lllll_opy_
  arg.append(bstack11llll_opy_ (u"ࠤ࠰࡛ࠧ൅"))
  arg.append(bstack11llll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨെ"))
  arg.append(bstack11llll_opy_ (u"ࠦ࠲࡝ࠢേ"))
  arg.append(bstack11llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦൈ"))
  global bstack1l11ll111l_opy_
  global bstack1l1111l1l1_opy_
  global bstack111l111l1_opy_
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
    bstack111l111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1l1111l_opy_(CONFIG) and bstack11l1l1l1l_opy_():
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
    logger.debug(bstack11llll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ൉"))
  bstack1l1llllll_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫൊ"), {}).get(bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪോ"))
  bstack11l1lllll_opy_ = True
  bstack11llll111l_opy_(bstack1lll111l1_opy_)
  os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪൌ")] = CONFIG[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ്ࠬ")]
  os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧൎ")] = CONFIG[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൏")]
  os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ൐")] = bstack1lll1l1ll1_opy_.__str__()
  from _pytest.config import main as bstack1llll1111_opy_
  bstack11lll111l1_opy_ = []
  try:
    bstack1ll11l111_opy_ = bstack1llll1111_opy_(arg)
    if bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ൑") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1l1ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11lll111l1_opy_.append(bstack1l1l1l1ll1_opy_)
    try:
      bstack1ll1l11lll_opy_ = (bstack11lll111l1_opy_, int(bstack1ll11l111_opy_))
      bstack1ll111l1l1_opy_.append(bstack1ll1l11lll_opy_)
    except:
      bstack1ll111l1l1_opy_.append((bstack11lll111l1_opy_, bstack1ll11l111_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11lll111l1_opy_.append({bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭൒"): bstack11llll_opy_ (u"ࠩࡓࡶࡴࡩࡥࡴࡵࠣࠫ൓") + os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪൔ")), bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪൕ"): traceback.format_exc(), bstack11llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫൖ"): int(os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ൗ")))})
    bstack1ll111l1l1_opy_.append((bstack11lll111l1_opy_, 1))
def bstack1llll1lll1_opy_(arg):
  global bstack1lll1111l_opy_
  bstack11llll111l_opy_(bstack1l1l1ll11_opy_)
  os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ൘")] = str(bstack11l1llllll_opy_)
  from behave.__main__ import main as bstack1l1l11l11_opy_
  status_code = bstack1l1l11l11_opy_(arg)
  if status_code != 0:
    bstack1lll1111l_opy_ = status_code
def bstack11ll1l1l1l_opy_():
  logger.info(bstack1ll1l1lll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൙"), help=bstack11llll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ൚"))
  parser.add_argument(bstack11llll_opy_ (u"ࠪ࠱ࡺ࠭൛"), bstack11llll_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ൜"), help=bstack11llll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ൝"))
  parser.add_argument(bstack11llll_opy_ (u"࠭࠭࡬ࠩ൞"), bstack11llll_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ൟ"), help=bstack11llll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩൠ"))
  parser.add_argument(bstack11llll_opy_ (u"ࠩ࠰ࡪࠬൡ"), bstack11llll_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨൢ"), help=bstack11llll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൣ"))
  bstack11llllll1_opy_ = parser.parse_args()
  try:
    bstack11lllll111_opy_ = bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ൤")
    if bstack11llllll1_opy_.framework and bstack11llllll1_opy_.framework not in (bstack11llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൥"), bstack11llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ൦")):
      bstack11lllll111_opy_ = bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ൧")
    bstack1l11l1lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lllll111_opy_)
    bstack11l1llll1l_opy_ = open(bstack1l11l1lll_opy_, bstack11llll_opy_ (u"ࠩࡵࠫ൨"))
    bstack1l1ll11ll1_opy_ = bstack11l1llll1l_opy_.read()
    bstack11l1llll1l_opy_.close()
    if bstack11llllll1_opy_.username:
      bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_.replace(bstack11llll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ൩"), bstack11llllll1_opy_.username)
    if bstack11llllll1_opy_.key:
      bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_.replace(bstack11llll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭൪"), bstack11llllll1_opy_.key)
    if bstack11llllll1_opy_.framework:
      bstack1l1ll11ll1_opy_ = bstack1l1ll11ll1_opy_.replace(bstack11llll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭൫"), bstack11llllll1_opy_.framework)
    file_name = bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ൬")
    file_path = os.path.abspath(file_name)
    bstack1lll1ll1ll_opy_ = open(file_path, bstack11llll_opy_ (u"ࠧࡸࠩ൭"))
    bstack1lll1ll1ll_opy_.write(bstack1l1ll11ll1_opy_)
    bstack1lll1ll1ll_opy_.close()
    logger.info(bstack11111lll1_opy_)
    try:
      os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ൮")] = bstack11llllll1_opy_.framework if bstack11llllll1_opy_.framework != None else bstack11llll_opy_ (u"ࠤࠥ൯")
      config = yaml.safe_load(bstack1l1ll11ll1_opy_)
      config[bstack11llll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൰")] = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪ൱")
      bstack111111l11_opy_(bstack11l1ll1ll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l1111l1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll111l111_opy_.format(str(e)))
def bstack111111l11_opy_(bstack11l1l1lll_opy_, config, bstack1l1lll1l1_opy_={}):
  global bstack1lll1l1ll1_opy_
  global bstack11l1111ll_opy_
  global bstack1111111l_opy_
  if not config:
    return
  bstack1llll111l1_opy_ = bstack1l11lllll_opy_ if not bstack1lll1l1ll1_opy_ else (
    bstack111l11l1l_opy_ if bstack11llll_opy_ (u"ࠬࡧࡰࡱࠩ൲") in config else bstack1l1l11l1l_opy_)
  bstack1llllll1l1_opy_ = False
  bstack1ll1l1llll_opy_ = False
  if bstack1lll1l1ll1_opy_ is True:
      if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪ൳") in config:
          bstack1llllll1l1_opy_ = True
      else:
          bstack1ll1l1llll_opy_ = True
  bstack11lllllll1_opy_ = bstack111lll111_opy_.bstack111111ll1_opy_(config, bstack11l1111ll_opy_)
  data = {
    bstack11llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ൴"): config[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ൵")],
    bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ൶"): config[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭൷")],
    bstack11llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ൸"): bstack11l1l1lll_opy_,
    bstack11llll_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൹"): os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨൺ"), bstack11l1111ll_opy_),
    bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩൻ"): bstack1l11ll11l_opy_,
    bstack11llll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪർ"): bstack1ll1111l11_opy_(),
    bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬൽ"): {
      bstack11llll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨൾ"): str(config[bstack11llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫൿ")]) if bstack11llll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ඀") in config else bstack11llll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢඁ"),
      bstack11llll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩං"): sys.version,
      bstack11llll_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪඃ"): bstack1lll1l1111_opy_(os.getenv(bstack11llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ඄"), bstack11llll_opy_ (u"ࠥࠦඅ"))),
      bstack11llll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ආ"): bstack11llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඇ"),
      bstack11llll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧඈ"): bstack1llll111l1_opy_,
      bstack11llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬඉ"): bstack11lllllll1_opy_,
      bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡸࡹ࡮ࡪࠧඊ"): os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧඋ")],
      bstack11llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ඌ"): bstack1l11111ll1_opy_(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඍ"), bstack11l1111ll_opy_)),
      bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඎ"): config[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඏ")] if config[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪඐ")] else bstack11llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤඑ"),
      bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫඒ"): str(config[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඓ")]) if bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ඔ") in config else bstack11llll_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨඕ"),
      bstack11llll_opy_ (u"࠭࡯ࡴࠩඖ"): sys.platform,
      bstack11llll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ඗"): socket.gethostname(),
      bstack11llll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ඘"): bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ඙"))
    }
  }
  if not bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪක")) is None:
    data[bstack11llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඛ")][bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨග")] = {
      bstack11llll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ඝ"): bstack11llll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬඞ"),
      bstack11llll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨඟ"): bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩච")),
      bstack11llll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩඡ"): bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧජ"))
    }
  if bstack11l1l1lll_opy_ == bstack11ll111ll_opy_:
    data[bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඣ")][bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫඤ")] = bstack1l11llll11_opy_(config)
  update(data[bstack11llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪඥ")], bstack1l1lll1l1_opy_)
  try:
    response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ඦ"), bstack1l1l11l1ll_opy_(bstack1l111l11l1_opy_), data, {
      bstack11llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧට"): (config[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬඨ")], config[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧඩ")])
    })
    if response:
      logger.debug(bstack1lll1lll1_opy_.format(bstack11l1l1lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll11111l1_opy_.format(str(e)))
def bstack1lll1l1111_opy_(framework):
  return bstack11llll_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤඪ").format(str(framework), __version__) if framework else bstack11llll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢණ").format(
    __version__)
def bstack1l11l11ll1_opy_():
  global CONFIG
  global bstack1l11ll1ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l11111l11_opy_()
    logger.debug(bstack111l11ll1_opy_.format(str(CONFIG)))
    bstack1l11ll1ll_opy_ = bstack1l1l1l1l11_opy_.bstack1111l111l_opy_(CONFIG, bstack1l11ll1ll_opy_)
    bstack11l1l111l1_opy_()
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦඬ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11llll11l_opy_
  atexit.register(bstack1l1llll111_opy_)
  signal.signal(signal.SIGINT, bstack11ll1lll11_opy_)
  signal.signal(signal.SIGTERM, bstack11ll1lll11_opy_)
def bstack11llll11l_opy_(exctype, value, traceback):
  global bstack1llll1l1l_opy_
  try:
    for driver in bstack1llll1l1l_opy_:
      bstack111llllll_opy_(driver, bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨත"), bstack11llll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧථ") + str(value))
  except Exception:
    pass
  bstack11l111ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l111ll1_opy_(message=bstack11llll_opy_ (u"ࠪࠫද"), bstack1ll1l11ll1_opy_ = False):
  global CONFIG
  bstack11ll111l1l_opy_ = bstack11llll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ධ") if bstack1ll1l11ll1_opy_ else bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫන")
  try:
    if message:
      bstack1l1lll1l1_opy_ = {
        bstack11ll111l1l_opy_ : str(message)
      }
      bstack111111l11_opy_(bstack11ll111ll_opy_, CONFIG, bstack1l1lll1l1_opy_)
    else:
      bstack111111l11_opy_(bstack11ll111ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1llll111ll_opy_.format(str(e)))
def bstack1l1lll1l11_opy_(bstack1llllll111_opy_, size):
  bstack1ll1ll1ll1_opy_ = []
  while len(bstack1llllll111_opy_) > size:
    bstack11lll11l11_opy_ = bstack1llllll111_opy_[:size]
    bstack1ll1ll1ll1_opy_.append(bstack11lll11l11_opy_)
    bstack1llllll111_opy_ = bstack1llllll111_opy_[size:]
  bstack1ll1ll1ll1_opy_.append(bstack1llllll111_opy_)
  return bstack1ll1ll1ll1_opy_
def bstack11l1ll1l11_opy_(args):
  if bstack11llll_opy_ (u"࠭࠭࡮ࠩ඲") in args and bstack11llll_opy_ (u"ࠧࡱࡦࡥࠫඳ") in args:
    return True
  return False
def run_on_browserstack(bstack11l111l11_opy_=None, bstack1ll111l1l1_opy_=None, bstack11ll1l111l_opy_=False):
  global CONFIG
  global bstack1ll1l1ll1l_opy_
  global bstack11l1llllll_opy_
  global bstack11l1111ll_opy_
  global bstack1111111l_opy_
  bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠨࠩප")
  bstack1l11l1l1l_opy_(bstack1ll1l1ll11_opy_, logger)
  if bstack11l111l11_opy_ and isinstance(bstack11l111l11_opy_, str):
    bstack11l111l11_opy_ = eval(bstack11l111l11_opy_)
  if bstack11l111l11_opy_:
    CONFIG = bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩඵ")]
    bstack1ll1l1ll1l_opy_ = bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫබ")]
    bstack11l1llllll_opy_ = bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭භ")]
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧම"), bstack11l1llllll_opy_)
    bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඹ")
  bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩය"), uuid4().__str__())
  logger.debug(bstack11llll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀࠫර") + bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ඼")))
  if not bstack11ll1l111l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11lll11l1l_opy_)
      return
    if sys.argv[1] == bstack11llll_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ල") or sys.argv[1] == bstack11llll_opy_ (u"ࠫ࠲ࡼࠧ඾"):
      logger.info(bstack11llll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ඿").format(__version__))
      return
    if sys.argv[1] == bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬව"):
      bstack11ll1l1l1l_opy_()
      return
  args = sys.argv
  bstack1l11l11ll1_opy_()
  global bstack1l11l11ll_opy_
  global bstack11ll1111ll_opy_
  global bstack11l1lllll_opy_
  global bstack11l1l1lll1_opy_
  global bstack11ll1l1ll1_opy_
  global bstack1l1llllll_opy_
  global bstack1lllllll1l_opy_
  global bstack111ll11ll_opy_
  global bstack1l11l111ll_opy_
  global bstack1lllll111l_opy_
  global bstack1l11l11l1_opy_
  bstack11ll1111ll_opy_ = len(CONFIG.get(bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪශ"), []))
  if not bstack1l1l1lllll_opy_:
    if args[1] == bstack11llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෂ") or args[1] == bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪස"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪහ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪළ"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෆ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෇"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭෈")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෉"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮්ࠪ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෌")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෍"):
      bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෎")
      args = args[2:]
    else:
      if not bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪා") in CONFIG or str(CONFIG[bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫැ")]).lower() in [bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩෑ"), bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫි")]:
        bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫී")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨු")]).lower() == bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෕"):
        bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ූ")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෗")]).lower() == bstack11llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨෘ"):
        bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩෙ")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧේ")]).lower() == bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෛ"):
        bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ො")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪෝ")]).lower() == bstack11llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨෞ"):
        bstack1l1l1lllll_opy_ = bstack11llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෟ")
        args = args[1:]
      else:
        os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ෠")] = bstack1l1l1lllll_opy_
        bstack1111lllll_opy_(bstack11lllll1ll_opy_)
  os.environ[bstack11llll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ෡")] = bstack1l1l1lllll_opy_
  bstack11l1111ll_opy_ = bstack1l1l1lllll_opy_
  global bstack1l1l11l11l_opy_
  global bstack111111l1l_opy_
  if bstack11l111l11_opy_:
    try:
      os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෢")] = bstack1l1l1lllll_opy_
      bstack111111l11_opy_(bstack11ll1lll1l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l11l1llll_opy_.format(str(e)))
  global bstack1l11ll111l_opy_
  global bstack1l1111l1l1_opy_
  global bstack1l1l11ll11_opy_
  global bstack1l1ll11ll_opy_
  global bstack1l11111ll_opy_
  global bstack1ll1l11ll_opy_
  global bstack11l1l1ll11_opy_
  global bstack1lll1llll_opy_
  global bstack11ll11ll11_opy_
  global bstack1ll1111lll_opy_
  global bstack1ll111l11l_opy_
  global bstack111l1l111_opy_
  global bstack11ll11111_opy_
  global bstack1ll1ll1111_opy_
  global bstack1l111ll1ll_opy_
  global bstack1l1l11lll_opy_
  global bstack11lll1llll_opy_
  global bstack1l1l1111ll_opy_
  global bstack1ll1111ll1_opy_
  global bstack1l1ll1lll1_opy_
  global bstack111l111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11ll111l_opy_ = webdriver.Remote.__init__
    bstack1l1111l1l1_opy_ = WebDriver.quit
    bstack111l1l111_opy_ = WebDriver.close
    bstack1l111ll1ll_opy_ = WebDriver.get
    bstack111l111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l11l11l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11ll1l1_opy_
    bstack111111l1l_opy_ = bstack1l11ll1l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1llll11l_opy_
    from QWeb.keywords import browser
    bstack1l1llll11l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1l1111l_opy_(CONFIG) and bstack11l1l1l1l_opy_():
    if bstack1l111l11ll_opy_() < version.parse(bstack1llll1111l_opy_):
      logger.error(bstack11lll1l11l_opy_.format(bstack1l111l11ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l11lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1ll1lll_opy_.format(str(e)))
  if not CONFIG.get(bstack11llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ෣"), False) and not bstack11l111l11_opy_:
    logger.info(bstack11l1ll111l_opy_)
  if bstack1l1l1lllll_opy_ != bstack11llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෤") or (bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෥") and not bstack11l111l11_opy_):
    bstack1llll1l1ll_opy_()
  if (bstack1l1l1lllll_opy_ in [bstack11llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෦"), bstack11llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෧"), bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෨")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l11llllll_opy_
        bstack1ll1l11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11llllll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11111ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1l1ll1l_opy_ + str(e))
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11llllll1l_opy_)
    if bstack1l1l1lllll_opy_ != bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෩"):
      bstack1l1lll111l_opy_()
    bstack1l1l11ll11_opy_ = Output.start_test
    bstack1l1ll11ll_opy_ = Output.end_test
    bstack11l1l1ll11_opy_ = TestStatus.__init__
    bstack11ll11ll11_opy_ = pabot._run
    bstack1ll1111lll_opy_ = QueueItem.__init__
    bstack1ll111l11l_opy_ = pabot._create_command_for_execution
    bstack1ll1111ll1_opy_ = pabot._report_results
  if bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෪"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11lll111ll_opy_)
    bstack11ll11111_opy_ = Runner.run_hook
    bstack1ll1ll1111_opy_ = Step.run
  if bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෫"):
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
      logger.debug(bstack11llll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ෬"))
  try:
    framework_name = bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ෭") if bstack1l1l1lllll_opy_ in [bstack11llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෮"), bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෯"), bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෰")] else bstack1l11l111l_opy_(bstack1l1l1lllll_opy_)
    bstack1l1l111l1_opy_ = {
      bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ෱"): bstack11llll_opy_ (u"ࠧࡼ࠲ࢀ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ෲ").format(framework_name) if bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෳ") and bstack11l1lll1l1_opy_() else framework_name,
      bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෴"): bstack1l11111ll1_opy_(framework_name),
      bstack11llll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෵"): __version__,
      bstack11llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ෶"): bstack1l1l1lllll_opy_
    }
    if bstack1l1l1lllll_opy_ in bstack1lllll1l1l_opy_:
      if bstack1lll1l1ll1_opy_ and bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ෷") in CONFIG and CONFIG[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෸")] == True:
        if bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ෹") in CONFIG:
          os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ෺")] = os.getenv(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ෻"), json.dumps(CONFIG[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ෼")]))
          CONFIG[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ෽")].pop(bstack11llll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ෾"), None)
          CONFIG[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭෿")].pop(bstack11llll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ฀"), None)
        bstack1l1l111l1_opy_[bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨก")] = {
          bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧข"): bstack11llll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬฃ"),
          bstack11llll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬค"): str(bstack1l111l11ll_opy_())
        }
    if bstack1l1l1lllll_opy_ not in [bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ฅ")]:
      bstack1l1ll1l1ll_opy_ = bstack1ll11ll1_opy_.launch(CONFIG, bstack1l1l111l1_opy_)
  except Exception as e:
    logger.debug(bstack1l111l1l1_opy_.format(bstack11llll_opy_ (u"࠭ࡔࡦࡵࡷࡌࡺࡨࠧฆ"), str(e)))
  if bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧง"):
    bstack11l1lllll_opy_ = True
    if bstack11l111l11_opy_ and bstack11ll1l111l_opy_:
      bstack1l1llllll_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬจ"), {}).get(bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫฉ"))
      bstack11llll111l_opy_(bstack1llll1l11l_opy_)
    elif bstack11l111l11_opy_:
      bstack1l1llllll_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧช"), {}).get(bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ซ"))
      global bstack1llll1l1l_opy_
      try:
        if bstack11l1ll1l11_opy_(bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฌ")]) and multiprocessing.current_process().name == bstack11llll_opy_ (u"࠭࠰ࠨญ"):
          bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪฎ")].remove(bstack11llll_opy_ (u"ࠨ࠯ࡰࠫฏ"))
          bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฐ")].remove(bstack11llll_opy_ (u"ࠪࡴࡩࡨࠧฑ"))
          bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧฒ")] = bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨณ")][0]
          with open(bstack11l111l11_opy_[bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩด")], bstack11llll_opy_ (u"ࠧࡳࠩต")) as f:
            bstack1l1ll1ll1_opy_ = f.read()
          bstack111l11111_opy_ = bstack11llll_opy_ (u"ࠣࠤࠥࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡦ࡮ࠤ࡮ࡳࡰࡰࡴࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫࠻ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠬࢀࢃࠩ࠼ࠢࡩࡶࡴࡳࠠࡱࡦࡥࠤ࡮ࡳࡰࡰࡴࡷࠤࡕࡪࡢ࠼ࠢࡲ࡫ࡤࡪࡢࠡ࠿ࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦถ").format(str(bstack11l111l11_opy_))
          bstack1ll1ll11ll_opy_ = bstack111l11111_opy_ + bstack1l1ll1ll1_opy_
          bstack1ll11111ll_opy_ = bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬท")] + bstack11llll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡹ࡫࡭ࡱ࠰ࡳࡽࠬธ")
          with open(bstack1ll11111ll_opy_, bstack11llll_opy_ (u"ࠫࡼ࠭น")):
            pass
          with open(bstack1ll11111ll_opy_, bstack11llll_opy_ (u"ࠧࡽࠫࠣบ")) as f:
            f.write(bstack1ll1ll11ll_opy_)
          import subprocess
          bstack11l11ll11_opy_ = subprocess.run([bstack11llll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨป"), bstack1ll11111ll_opy_])
          if os.path.exists(bstack1ll11111ll_opy_):
            os.unlink(bstack1ll11111ll_opy_)
          os._exit(bstack11l11ll11_opy_.returncode)
        else:
          if bstack11l1ll1l11_opy_(bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪผ")]):
            bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฝ")].remove(bstack11llll_opy_ (u"ࠩ࠰ࡱࠬพ"))
            bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฟ")].remove(bstack11llll_opy_ (u"ࠫࡵࡪࡢࠨภ"))
            bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨม")] = bstack11l111l11_opy_[bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩย")][0]
          bstack11llll111l_opy_(bstack1llll1l11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪร")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11llll_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪฤ")] = bstack11llll_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫล")
          mod_globals[bstack11llll_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬฦ")] = os.path.abspath(bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧว")])
          exec(open(bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨศ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11llll_opy_ (u"࠭ࡃࡢࡷࡪ࡬ࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂ࠭ษ").format(str(e)))
          for driver in bstack1llll1l1l_opy_:
            bstack1ll111l1l1_opy_.append({
              bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬส"): bstack11l111l11_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫห")],
              bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨฬ"): str(e),
              bstack11llll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩอ"): multiprocessing.current_process().name
            })
            bstack111llllll_opy_(driver, bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫฮ"), bstack11llll_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣฯ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llll1l1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1llllll_opy_, CONFIG, logger)
      bstack1lllll1l11_opy_()
      bstack111l1ll11_opy_()
      bstack1111l111_opy_ = {
        bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩะ"): args[0],
        bstack11llll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧั"): CONFIG,
        bstack11llll_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩา"): bstack1ll1l1ll1l_opy_,
        bstack11llll_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫำ"): bstack11l1llllll_opy_
      }
      percy.bstack1l11llll1l_opy_()
      if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ิ") in CONFIG:
        bstack111l1lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llllll1l_opy_ = manager.list()
        if bstack11l1ll1l11_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧี")]):
            if index == 0:
              bstack1111l111_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨึ")] = args
            bstack111l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111l111_opy_, bstack1llllll1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩื")]):
            bstack111l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111l111_opy_, bstack1llllll1l_opy_)))
        for t in bstack111l1lll_opy_:
          t.start()
        for t in bstack111l1lll_opy_:
          t.join()
        bstack111ll11ll_opy_ = list(bstack1llllll1l_opy_)
      else:
        if bstack11l1ll1l11_opy_(args):
          bstack1111l111_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧุࠪ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111l111_opy_,))
          test.start()
          test.join()
        else:
          bstack11llll111l_opy_(bstack1llll1l11l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11llll_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡูࠪ")] = bstack11llll_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢฺࠫ")
          mod_globals[bstack11llll_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ฻")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ฼") or bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ฽"):
    percy.init(bstack11l1llllll_opy_, CONFIG, logger)
    percy.bstack1l11llll1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11llllll1l_opy_)
    bstack1lllll1l11_opy_()
    bstack11llll111l_opy_(bstack111l1l11l_opy_)
    if bstack1lll1l1ll1_opy_:
      bstack11l1l1l1l1_opy_(bstack111l1l11l_opy_, args)
      if bstack11llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ฾") in args:
        i = args.index(bstack11llll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ฿"))
        args.pop(i)
        args.pop(i)
      if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫเ") not in CONFIG:
        CONFIG[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬแ")] = [{}]
        bstack11ll1111ll_opy_ = 1
      if bstack1l11l11ll_opy_ == 0:
        bstack1l11l11ll_opy_ = 1
      args.insert(0, str(bstack1l11l11ll_opy_))
      args.insert(0, str(bstack11llll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨโ")))
    if bstack1ll11ll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1llll111l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1ll111l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11llll_opy_ (u"ࠦࡗࡕࡂࡐࡖࡢࡓࡕ࡚ࡉࡐࡐࡖࠦใ"),
        ).parse_args(bstack1llll111l_opy_)
        bstack1l1ll1l11l_opy_ = args.index(bstack1llll111l_opy_[0]) if len(bstack1llll111l_opy_) > 0 else len(args)
        args.insert(bstack1l1ll1l11l_opy_, str(bstack11llll_opy_ (u"ࠬ࠳࠭࡭࡫ࡶࡸࡪࡴࡥࡳࠩไ")))
        args.insert(bstack1l1ll1l11l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡲࡰࡤࡲࡸࡤࡲࡩࡴࡶࡨࡲࡪࡸ࠮ࡱࡻࠪๅ"))))
        if bstack11ll1llll_opy_(os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬๆ"))) and str(os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ็"), bstack11llll_opy_ (u"ࠩࡱࡹࡱࡲ่ࠧ"))) != bstack11llll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ้"):
          for bstack1l1l1l11l_opy_ in bstack1l1ll111l1_opy_:
            args.remove(bstack1l1l1l11l_opy_)
          bstack1ll1111l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ๊")).split(bstack11llll_opy_ (u"ࠬ࠲๋ࠧ"))
          for bstack1111lll11_opy_ in bstack1ll1111l1_opy_:
            args.append(bstack1111lll11_opy_)
      except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡺࡴࡢࡥ࡫࡭ࡳ࡭ࠠ࡭࡫ࡶࡸࡪࡴࡥࡳࠢࡩࡳࡷࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࠠࡆࡴࡵࡳࡷࠦ࠭ࠡࠤ์").format(e))
    pabot.main(args)
  elif bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨํ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11llllll1l_opy_)
    for a in args:
      if bstack11llll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧ๎") in a:
        bstack11ll1l1ll1_opy_ = int(a.split(bstack11llll_opy_ (u"ࠩ࠽ࠫ๏"))[1])
      if bstack11llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ๐") in a:
        bstack1l1llllll_opy_ = str(a.split(bstack11llll_opy_ (u"ࠫ࠿࠭๑"))[1])
      if bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ๒") in a:
        bstack1lllllll1l_opy_ = str(a.split(bstack11llll_opy_ (u"࠭࠺ࠨ๓"))[1])
    bstack11l1l1l1ll_opy_ = None
    if bstack11llll_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭๔") in args:
      i = args.index(bstack11llll_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ๕"))
      args.pop(i)
      bstack11l1l1l1ll_opy_ = args.pop(i)
    if bstack11l1l1l1ll_opy_ is not None:
      global bstack1l111lll1l_opy_
      bstack1l111lll1l_opy_ = bstack11l1l1l1ll_opy_
    bstack11llll111l_opy_(bstack111l1l11l_opy_)
    run_cli(args)
    if bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭๖") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1l1ll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll111l1l1_opy_.append(bstack1l1l1l1ll1_opy_)
  elif bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ๗"):
    percy.init(bstack11l1llllll_opy_, CONFIG, logger)
    percy.bstack1l11llll1l_opy_()
    bstack1l1111l1ll_opy_ = bstack1111ll1l_opy_(args, logger, CONFIG, bstack1lll1l1ll1_opy_)
    bstack1l1111l1ll_opy_.bstack1lllllll1_opy_()
    bstack1lllll1l11_opy_()
    bstack11l1l1lll1_opy_ = True
    bstack1lllll111l_opy_ = bstack1l1111l1ll_opy_.bstack1111llll_opy_()
    bstack1l1111l1ll_opy_.bstack1111l111_opy_(bstack1l1l1llll_opy_)
    bstack1l11lll11_opy_ = bstack1l1111l1ll_opy_.bstack11111111_opy_(bstack11l1l11ll1_opy_, {
      bstack11llll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ๘"): bstack1ll1l1ll1l_opy_,
      bstack11llll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ๙"): bstack11l1llllll_opy_,
      bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ๚"): bstack1lll1l1ll1_opy_
    })
    try:
      bstack11lll111l1_opy_, bstack11l1l11111_opy_ = map(list, zip(*bstack1l11lll11_opy_))
      bstack1l11l111ll_opy_ = bstack11lll111l1_opy_[0]
      for status_code in bstack11l1l11111_opy_:
        if status_code != 0:
          bstack1l11l11l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡧࡵࡶࡴࡸࡳࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠱ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠻ࠢࡾࢁࠧ๛").format(str(e)))
  elif bstack1l1l1lllll_opy_ == bstack11llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ๜"):
    try:
      from behave.__main__ import main as bstack1l1l11l11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111ll11l_opy_(e, bstack11lll111ll_opy_)
    bstack1lllll1l11_opy_()
    bstack11l1l1lll1_opy_ = True
    bstack111lll1l_opy_ = 1
    if bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๝") in CONFIG:
      bstack111lll1l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๞")]
    if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๟") in CONFIG:
      bstack11l1l11l1_opy_ = int(bstack111lll1l_opy_) * int(len(CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๠")]))
    else:
      bstack11l1l11l1_opy_ = int(bstack111lll1l_opy_)
    config = Configuration(args)
    bstack1l1l11ll1_opy_ = config.paths
    if len(bstack1l1l11ll1_opy_) == 0:
      import glob
      pattern = bstack11llll_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ๡")
      bstack1l1ll11lll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1ll11lll_opy_)
      config = Configuration(args)
      bstack1l1l11ll1_opy_ = config.paths
    bstack111111ll_opy_ = [os.path.normpath(item) for item in bstack1l1l11ll1_opy_]
    bstack1lll1111l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1l11111l_opy_ = [item for item in bstack1lll1111l1_opy_ if item not in bstack111111ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11llll_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ๢"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111111ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1lll111_opy_)))
                    for bstack11l1lll111_opy_ in bstack111111ll_opy_]
    bstack111l1111_opy_ = []
    for spec in bstack111111ll_opy_:
      bstack1llllllll_opy_ = []
      bstack1llllllll_opy_ += bstack1l1l11111l_opy_
      bstack1llllllll_opy_.append(spec)
      bstack111l1111_opy_.append(bstack1llllllll_opy_)
    execution_items = []
    for bstack1llllllll_opy_ in bstack111l1111_opy_:
      if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๣") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๤")]):
          item = {}
          item[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࠧ๥")] = bstack11llll_opy_ (u"ࠫࠥ࠭๦").join(bstack1llllllll_opy_)
          item[bstack11llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๧")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11llll_opy_ (u"࠭ࡡࡳࡩࠪ๨")] = bstack11llll_opy_ (u"ࠧࠡࠩ๩").join(bstack1llllllll_opy_)
        item[bstack11llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ๪")] = 0
        execution_items.append(item)
    bstack1l11111lll_opy_ = bstack1l1lll1l11_opy_(execution_items, bstack11l1l11l1_opy_)
    for execution_item in bstack1l11111lll_opy_:
      bstack111l1lll_opy_ = []
      for item in execution_item:
        bstack111l1lll_opy_.append(bstack11l11111_opy_(name=str(item[bstack11llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ๫")]),
                                             target=bstack1llll1lll1_opy_,
                                             args=(item[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࠧ๬")],)))
      for t in bstack111l1lll_opy_:
        t.start()
      for t in bstack111l1lll_opy_:
        t.join()
  else:
    bstack1111lllll_opy_(bstack11lllll1ll_opy_)
  if not bstack11l111l11_opy_:
    bstack1ll111ll1l_opy_()
  bstack1l1l1l1l11_opy_.bstack1l1lll1l1l_opy_()
def browserstack_initialize(bstack1lll1ll11_opy_=None):
  run_on_browserstack(bstack1lll1ll11_opy_, None, True)
def bstack1ll111ll1l_opy_():
  global CONFIG
  global bstack11l1111ll_opy_
  global bstack1l11l11l1_opy_
  global bstack1lll1111l_opy_
  global bstack1111111l_opy_
  bstack1ll11ll1_opy_.stop()
  bstack1ll1l111_opy_.bstack1l111l1lll_opy_()
  [bstack1l11l1111_opy_, bstack11ll1l11l1_opy_] = get_build_link()
  if bstack1l11l1111_opy_ is not None and bstack1ll11111l_opy_() != -1:
    sessions = bstack1l111ll111_opy_(bstack1l11l1111_opy_)
    bstack1111ll1l1_opy_(sessions, bstack11ll1l11l1_opy_)
  if bstack11l1111ll_opy_ == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ๭") and bstack1l11l11l1_opy_ != 0:
    sys.exit(bstack1l11l11l1_opy_)
  if bstack11l1111ll_opy_ == bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ๮") and bstack1lll1111l_opy_ != 0:
    sys.exit(bstack1lll1111l_opy_)
def bstack1l11l111l_opy_(bstack11ll111l1_opy_):
  if bstack11ll111l1_opy_:
    return bstack11ll111l1_opy_.capitalize()
  else:
    return bstack11llll_opy_ (u"࠭ࠧ๯")
def bstack11ll1l11l_opy_(bstack1ll1llll1_opy_):
  if bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๰") in bstack1ll1llll1_opy_ and bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๱")] != bstack11llll_opy_ (u"ࠩࠪ๲"):
    return bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ๳")]
  else:
    bstack111l1l1l1_opy_ = bstack11llll_opy_ (u"ࠦࠧ๴")
    if bstack11llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๵") in bstack1ll1llll1_opy_ and bstack1ll1llll1_opy_[bstack11llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๶")] != None:
      bstack111l1l1l1_opy_ += bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ๷")] + bstack11llll_opy_ (u"ࠣ࠮ࠣࠦ๸")
      if bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠩࡲࡷࠬ๹")] == bstack11llll_opy_ (u"ࠥ࡭ࡴࡹࠢ๺"):
        bstack111l1l1l1_opy_ += bstack11llll_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ๻")
      bstack111l1l1l1_opy_ += (bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๼")] or bstack11llll_opy_ (u"࠭ࠧ๽"))
      return bstack111l1l1l1_opy_
    else:
      bstack111l1l1l1_opy_ += bstack1l11l111l_opy_(bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ๾")]) + bstack11llll_opy_ (u"ࠣࠢࠥ๿") + (
              bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ຀")] or bstack11llll_opy_ (u"ࠪࠫກ")) + bstack11llll_opy_ (u"ࠦ࠱ࠦࠢຂ")
      if bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠬࡵࡳࠨ຃")] == bstack11llll_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢຄ"):
        bstack111l1l1l1_opy_ += bstack11llll_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ຅")
      bstack111l1l1l1_opy_ += bstack1ll1llll1_opy_[bstack11llll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬຆ")] or bstack11llll_opy_ (u"ࠩࠪງ")
      return bstack111l1l1l1_opy_
def bstack1l1111111_opy_(bstack11l1l1ll1_opy_):
  if bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠥࡨࡴࡴࡥࠣຈ"):
    return bstack11llll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧຉ")
  elif bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧຊ"):
    return bstack11llll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ຋")
  elif bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢຌ"):
    return bstack11llll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨຍ")
  elif bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣຎ"):
    return bstack11llll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬຏ")
  elif bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧຐ"):
    return bstack11llll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪຑ")
  elif bstack11l1l1ll1_opy_ == bstack11llll_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢຒ"):
    return bstack11llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨຓ")
  else:
    return bstack11llll_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬດ") + bstack1l11l111l_opy_(
      bstack11l1l1ll1_opy_) + bstack11llll_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨຕ")
def bstack1lll11l1l1_opy_(session):
  return bstack11llll_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪຖ").format(
    session[bstack11llll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨທ")], bstack11ll1l11l_opy_(session), bstack1l1111111_opy_(session[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫຘ")]),
    bstack1l1111111_opy_(session[bstack11llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ນ")]),
    bstack1l11l111l_opy_(session[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨບ")] or session[bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨປ")] or bstack11llll_opy_ (u"ࠩࠪຜ")) + bstack11llll_opy_ (u"ࠥࠤࠧຝ") + (session[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ພ")] or bstack11llll_opy_ (u"ࠬ࠭ຟ")),
    session[bstack11llll_opy_ (u"࠭࡯ࡴࠩຠ")] + bstack11llll_opy_ (u"ࠢࠡࠤມ") + session[bstack11llll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬຢ")], session[bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫຣ")] or bstack11llll_opy_ (u"ࠪࠫ຤"),
    session[bstack11llll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨລ")] if session[bstack11llll_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ຦")] else bstack11llll_opy_ (u"࠭ࠧວ"))
def bstack1111ll1l1_opy_(sessions, bstack11ll1l11l1_opy_):
  try:
    bstack1ll11l1lll_opy_ = bstack11llll_opy_ (u"ࠢࠣຨ")
    if not os.path.exists(bstack1ll11lll11_opy_):
      os.mkdir(bstack1ll11lll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11llll_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ຩ")), bstack11llll_opy_ (u"ࠩࡵࠫສ")) as f:
      bstack1ll11l1lll_opy_ = f.read()
    bstack1ll11l1lll_opy_ = bstack1ll11l1lll_opy_.replace(bstack11llll_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧຫ"), str(len(sessions)))
    bstack1ll11l1lll_opy_ = bstack1ll11l1lll_opy_.replace(bstack11llll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫຬ"), bstack11ll1l11l1_opy_)
    bstack1ll11l1lll_opy_ = bstack1ll11l1lll_opy_.replace(bstack11llll_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ອ"),
                                              sessions[0].get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪຮ")) if sessions[0] else bstack11llll_opy_ (u"ࠧࠨຯ"))
    with open(os.path.join(bstack1ll11lll11_opy_, bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬະ")), bstack11llll_opy_ (u"ࠩࡺࠫັ")) as stream:
      stream.write(bstack1ll11l1lll_opy_.split(bstack11llll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧາ"))[0])
      for session in sessions:
        stream.write(bstack1lll11l1l1_opy_(session))
      stream.write(bstack1ll11l1lll_opy_.split(bstack11llll_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨຳ"))[1])
    logger.info(bstack11llll_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨິ").format(bstack1ll11lll11_opy_));
  except Exception as e:
    logger.debug(bstack1l1l11llll_opy_.format(str(e)))
def bstack1l111ll111_opy_(bstack1l11l1111_opy_):
  global CONFIG
  try:
    host = bstack11llll_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩີ") if bstack11llll_opy_ (u"ࠧࡢࡲࡳࠫຶ") in CONFIG else bstack11llll_opy_ (u"ࠨࡣࡳ࡭ࠬື")
    user = CONFIG[bstack11llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨຸࠫ")]
    key = CONFIG[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾູ࠭")]
    bstack11ll1l111_opy_ = bstack11llll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ຺ࠪ") if bstack11llll_opy_ (u"ࠬࡧࡰࡱࠩົ") in CONFIG else bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨຼ")
    url = bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬຽ").format(user, key, host, bstack11ll1l111_opy_,
                                                                                bstack1l11l1111_opy_)
    headers = {
      bstack11llll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ຾"): bstack11llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ຿"),
    }
    proxies = bstack1ll11ll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨເ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll1l11l1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1l11ll11l_opy_
  try:
    if bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧແ") in CONFIG:
      host = bstack11llll_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨໂ") if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪໃ") in CONFIG else bstack11llll_opy_ (u"ࠧࡢࡲ࡬ࠫໄ")
      user = CONFIG[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ໅")]
      key = CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬໆ")]
      bstack11ll1l111_opy_ = bstack11llll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ໇") if bstack11llll_opy_ (u"ࠫࡦࡶࡰࠨ່") in CONFIG else bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫້ࠧ")
      url = bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ໊࠭").format(user, key, host, bstack11ll1l111_opy_)
      headers = {
        bstack11llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ໋࠭"): bstack11llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ໌"),
      }
      if bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫໍ") in CONFIG:
        params = {bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ໎"): CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ໏")], bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໐"): CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໑")]}
      else:
        params = {bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ໒"): CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ໓")]}
      proxies = bstack1ll11ll11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll1l1l1l_opy_ = response.json()[0][bstack11llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ໔")]
        if bstack1lll1l1l1l_opy_:
          bstack11ll1l11l1_opy_ = bstack1lll1l1l1l_opy_[bstack11llll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ໕")].split(bstack11llll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ໖"))[0] + bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭໗") + bstack1lll1l1l1l_opy_[
            bstack11llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ໘")]
          logger.info(bstack11l1ll1l1_opy_.format(bstack11ll1l11l1_opy_))
          bstack1l11ll11l_opy_ = bstack1lll1l1l1l_opy_[bstack11llll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ໙")]
          bstack1l1111l11l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ໚")]
          if bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ໛") in CONFIG:
            bstack1l1111l11l_opy_ += bstack11llll_opy_ (u"ࠪࠤࠬໜ") + CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ໝ")]
          if bstack1l1111l11l_opy_ != bstack1lll1l1l1l_opy_[bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪໞ")]:
            logger.debug(bstack11ll1l1111_opy_.format(bstack1lll1l1l1l_opy_[bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫໟ")], bstack1l1111l11l_opy_))
          return [bstack1lll1l1l1l_opy_[bstack11llll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ໠")], bstack11ll1l11l1_opy_]
    else:
      logger.warn(bstack1l111llll1_opy_)
  except Exception as e:
    logger.debug(bstack11lll1l1l1_opy_.format(str(e)))
  return [None, None]
def bstack111ll1l11_opy_(url, bstack11ll1l1ll_opy_=False):
  global CONFIG
  global bstack11ll11l1ll_opy_
  if not bstack11ll11l1ll_opy_:
    hostname = bstack11lll1l11_opy_(url)
    is_private = bstack11lll11ll_opy_(hostname)
    if (bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ໡") in CONFIG and not bstack11ll1llll_opy_(CONFIG[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭໢")])) and (is_private or bstack11ll1l1ll_opy_):
      bstack11ll11l1ll_opy_ = hostname
def bstack11lll1l11_opy_(url):
  return urlparse(url).hostname
def bstack11lll11ll_opy_(hostname):
  for bstack1l111ll11_opy_ in bstack1l111l111_opy_:
    regex = re.compile(bstack1l111ll11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l11lllll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11ll1l1ll1_opy_
  bstack1lllllllll_opy_ = not (bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໣"), None) and bstack1lll1111_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໤"), None))
  bstack1ll1l11l11_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ໥"), None) != True
  if not bstack111l111l_opy_.bstack111l1l1ll_opy_(CONFIG, bstack11ll1l1ll1_opy_) or (bstack1ll1l11l11_opy_ and bstack1lllllllll_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ໦"))
    return {}
  try:
    logger.debug(bstack11llll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ໧"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1lll11ll11_opy_.bstack1l1llll1ll_opy_)
    return results
  except Exception:
    logger.error(bstack11llll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ໨"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11ll1l1ll1_opy_
  bstack1lllllllll_opy_ = not (bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໩"), None) and bstack1lll1111_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໪"), None))
  bstack1ll1l11l11_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ໫"), None) != True
  if not bstack111l111l_opy_.bstack111l1l1ll_opy_(CONFIG, bstack11ll1l1ll1_opy_) or (bstack1ll1l11l11_opy_ and bstack1lllllllll_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ໬"))
    return {}
  try:
    logger.debug(bstack11llll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫ໭"))
    logger.debug(perform_scan(driver))
    bstack1l11ll1lll_opy_ = driver.execute_async_script(bstack1lll11ll11_opy_.bstack11l11llll_opy_)
    return bstack1l11ll1lll_opy_
  except Exception:
    logger.error(bstack11llll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣ໮"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11ll1l1ll1_opy_
  bstack1lllllllll_opy_ = not (bstack1lll1111_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ໯"), None) and bstack1lll1111_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໰"), None))
  bstack1ll1l11l11_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ໱"), None) != True
  if not bstack111l111l_opy_.bstack111l1l1ll_opy_(CONFIG, bstack11ll1l1ll1_opy_) or (bstack1ll1l11l11_opy_ and bstack1lllllllll_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨ໲"))
    return {}
  try:
    bstack1llll11lll_opy_ = driver.execute_async_script(bstack1lll11ll11_opy_.perform_scan, {bstack11llll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ໳"): kwargs.get(bstack11llll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ໴"), None) or bstack11llll_opy_ (u"ࠧࠨ໵")})
    return bstack1llll11lll_opy_
  except Exception:
    logger.error(bstack11llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ໶"))
    return {}