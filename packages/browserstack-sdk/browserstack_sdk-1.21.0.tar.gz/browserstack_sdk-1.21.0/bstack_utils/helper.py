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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll1l1l1_opy_, bstack1l111l111_opy_, bstack1111111l1_opy_, bstack1lll1ll111_opy_,
                                    bstack111ll11lll_opy_, bstack111ll1l111_opy_, bstack111ll1ll1l_opy_, bstack111lll11l1_opy_)
from bstack_utils.messages import bstack111llll11_opy_, bstack1l1ll1lll_opy_
from bstack_utils.proxy import bstack1ll11ll11_opy_, bstack11111ll11_opy_
bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
logger = logging.getLogger(__name__)
def bstack11l11l1l1l_opy_(config):
    return config[bstack11llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩኴ")]
def bstack11l11llll1_opy_(config):
    return config[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫኵ")]
def bstack11ll111ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111l11ll1_opy_(obj):
    values = []
    bstack111l111l1l_opy_ = re.compile(bstack11llll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ኶"), re.I)
    for key in obj.keys():
        if bstack111l111l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l11ll11_opy_(config):
    tags = []
    tags.extend(bstack1111l11ll1_opy_(os.environ))
    tags.extend(bstack1111l11ll1_opy_(config))
    return tags
def bstack1111l11l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l1ll1l_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return bstack11llll_opy_ (u"ࠪࠫ኷")
    return bstack11llll_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧኸ").format(bstack111l111ll1_opy_.name, bstack111l111ll1_opy_.email)
def bstack11l11l1l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111lll1ll_opy_ = repo.common_dir
        info = {
            bstack11llll_opy_ (u"ࠧࡹࡨࡢࠤኹ"): repo.head.commit.hexsha,
            bstack11llll_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤኺ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11llll_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢኻ"): repo.active_branch.name,
            bstack11llll_opy_ (u"ࠣࡶࡤ࡫ࠧኼ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11llll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧኽ"): bstack1111l1ll1l_opy_(repo.head.commit.committer),
            bstack11llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦኾ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11llll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦ኿"): bstack1111l1ll1l_opy_(repo.head.commit.author),
            bstack11llll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥዀ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11llll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ዁"): repo.head.commit.message,
            bstack11llll_opy_ (u"ࠢࡳࡱࡲࡸࠧዂ"): repo.git.rev_parse(bstack11llll_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥዃ")),
            bstack11llll_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥዄ"): bstack1111lll1ll_opy_,
            bstack11llll_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨዅ"): subprocess.check_output([bstack11llll_opy_ (u"ࠦ࡬࡯ࡴࠣ዆"), bstack11llll_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣ዇"), bstack11llll_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤወ")]).strip().decode(
                bstack11llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ዉ")),
            bstack11llll_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥዊ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11llll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦዋ"): repo.git.rev_list(
                bstack11llll_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥዌ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111ll11ll_opy_ = []
        for remote in remotes:
            bstack11111lll11_opy_ = {
                bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤው"): remote.name,
                bstack11llll_opy_ (u"ࠧࡻࡲ࡭ࠤዎ"): remote.url,
            }
            bstack1111ll11ll_opy_.append(bstack11111lll11_opy_)
        bstack111l1l1lll_opy_ = {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦዏ"): bstack11llll_opy_ (u"ࠢࡨ࡫ࡷࠦዐ"),
            **info,
            bstack11llll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤዑ"): bstack1111ll11ll_opy_
        }
        bstack111l1l1lll_opy_ = bstack1111ll1l1l_opy_(bstack111l1l1lll_opy_)
        return bstack111l1l1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧዒ").format(err))
        return {}
def bstack1111ll1l1l_opy_(bstack111l1l1lll_opy_):
    bstack11111ll1l1_opy_ = bstack111l1ll11l_opy_(bstack111l1l1lll_opy_)
    if bstack11111ll1l1_opy_ and bstack11111ll1l1_opy_ > bstack111ll11lll_opy_:
        bstack1111ll1lll_opy_ = bstack11111ll1l1_opy_ - bstack111ll11lll_opy_
        bstack1111l1lll1_opy_ = bstack1111ll1ll1_opy_(bstack111l1l1lll_opy_[bstack11llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦዓ")], bstack1111ll1lll_opy_)
        bstack111l1l1lll_opy_[bstack11llll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧዔ")] = bstack1111l1lll1_opy_
        logger.info(bstack11llll_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢዕ")
                    .format(bstack111l1ll11l_opy_(bstack111l1l1lll_opy_) / 1024))
    return bstack111l1l1lll_opy_
def bstack111l1ll11l_opy_(bstack1ll1lll1ll_opy_):
    try:
        if bstack1ll1lll1ll_opy_:
            bstack11111l1111_opy_ = json.dumps(bstack1ll1lll1ll_opy_)
            bstack111l11lll1_opy_ = sys.getsizeof(bstack11111l1111_opy_)
            return bstack111l11lll1_opy_
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨዖ").format(e))
    return -1
def bstack1111ll1ll1_opy_(field, bstack1111l111l1_opy_):
    try:
        bstack1111l1l11l_opy_ = len(bytes(bstack111ll1l111_opy_, bstack11llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭዗")))
        bstack111l1l1ll1_opy_ = bytes(field, bstack11llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧዘ"))
        bstack111l1ll1ll_opy_ = len(bstack111l1l1ll1_opy_)
        bstack111l1ll1l1_opy_ = ceil(bstack111l1ll1ll_opy_ - bstack1111l111l1_opy_ - bstack1111l1l11l_opy_)
        if bstack111l1ll1l1_opy_ > 0:
            bstack111l1111ll_opy_ = bstack111l1l1ll1_opy_[:bstack111l1ll1l1_opy_].decode(bstack11llll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨዙ"), errors=bstack11llll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪዚ")) + bstack111ll1l111_opy_
            return bstack111l1111ll_opy_
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤዛ").format(e))
    return field
def bstack11lll11ll1_opy_():
    env = os.environ
    if (bstack11llll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥዜ") in env and len(env[bstack11llll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦዝ")]) > 0) or (
            bstack11llll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨዞ") in env and len(env[bstack11llll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢዟ")]) > 0):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢዠ"): bstack11llll_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦዡ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢዢ"): env.get(bstack11llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣዣ")),
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣዤ"): env.get(bstack11llll_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤዥ")),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢዦ"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣዧ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠥࡇࡎࠨየ")) == bstack11llll_opy_ (u"ࠦࡹࡸࡵࡦࠤዩ") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢዪ"))):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦያ"): bstack11llll_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤዬ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦይ"): env.get(bstack11llll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧዮ")),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧዯ"): env.get(bstack11llll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣደ")),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦዱ"): env.get(bstack11llll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤዲ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠢࡄࡋࠥዳ")) == bstack11llll_opy_ (u"ࠣࡶࡵࡹࡪࠨዴ") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤድ"))):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣዶ"): bstack11llll_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢዷ"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣዸ"): env.get(bstack11llll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨዹ")),
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤዺ"): env.get(bstack11llll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥዻ")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣዼ"): env.get(bstack11llll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤዽ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡈࡏࠢዾ")) == bstack11llll_opy_ (u"ࠧࡺࡲࡶࡧࠥዿ") and env.get(bstack11llll_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢጀ")) == bstack11llll_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤጁ"):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨጂ"): bstack11llll_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦጃ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጄ"): None,
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨጅ"): None,
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦጆ"): None
        }
    if env.get(bstack11llll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤጇ")) and env.get(bstack11llll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥገ")):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨጉ"): bstack11llll_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧጊ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጋ"): env.get(bstack11llll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤጌ")),
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢግ"): None,
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጎ"): env.get(bstack11llll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤጏ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠣࡅࡌࠦጐ")) == bstack11llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ጑") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤጒ"))):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጓ"): bstack11llll_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦጔ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጕ"): env.get(bstack11llll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥ጖")),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ጗"): None,
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣጘ"): env.get(bstack11llll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣጙ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡈࡏࠢጚ")) == bstack11llll_opy_ (u"ࠧࡺࡲࡶࡧࠥጛ") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤጜ"))):
        return {
            bstack11llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጝ"): bstack11llll_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦጞ"),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧጟ"): env.get(bstack11llll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤጠ")),
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨጡ"): env.get(bstack11llll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥጢ")),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጣ"): env.get(bstack11llll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥጤ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠣࡅࡌࠦጥ")) == bstack11llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢጦ") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨጧ"))):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጨ"): bstack11llll_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧጩ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጪ"): env.get(bstack11llll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦጫ")),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥጬ"): env.get(bstack11llll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢጭ")),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጮ"): env.get(bstack11llll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢጯ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠧࡉࡉࠣጰ")) == bstack11llll_opy_ (u"ࠨࡴࡳࡷࡨࠦጱ") and bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥጲ"))):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨጳ"): bstack11llll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧጴ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጵ"): env.get(bstack11llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥጶ")),
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጷ"): env.get(bstack11llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣጸ")) or env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥጹ")),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጺ"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦጻ"))
        }
    if bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧጼ"))):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጽ"): bstack11llll_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧጾ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጿ"): bstack11llll_opy_ (u"ࠢࡼࡿࡾࢁࠧፀ").format(env.get(bstack11llll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫፁ")), env.get(bstack11llll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩፂ"))),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧፃ"): env.get(bstack11llll_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥፄ")),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦፅ"): env.get(bstack11llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨፆ"))
        }
    if bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤፇ"))):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨፈ"): bstack11llll_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦፉ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨፊ"): bstack11llll_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥፋ").format(env.get(bstack11llll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫፌ")), env.get(bstack11llll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧፍ")), env.get(bstack11llll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨፎ")), env.get(bstack11llll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬፏ"))),
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦፐ"): env.get(bstack11llll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢፑ")),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥፒ"): env.get(bstack11llll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨፓ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢፔ")) and env.get(bstack11llll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤፕ")):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨፖ"): bstack11llll_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦፗ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨፘ"): bstack11llll_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢፙ").format(env.get(bstack11llll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨፚ")), env.get(bstack11llll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫ፛")), env.get(bstack11llll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧ፜"))),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ፝"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ፞")),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ፟"): env.get(bstack11llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ፠"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ፡")), env.get(bstack11llll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ።")), env.get(bstack11llll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ፣"))]):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ፤"): bstack11llll_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤ፥"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፦"): env.get(bstack11llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ፧")),
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፨"): env.get(bstack11llll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ፩")),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፪"): env.get(bstack11llll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ፫"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ፬")):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣ፭"): bstack11llll_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦ፮"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፯"): env.get(bstack11llll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣ፰")),
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፱"): env.get(bstack11llll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢ፲")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ፳"): env.get(bstack11llll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ፴"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧ፵")) or env.get(bstack11llll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ፶")):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ፷"): bstack11llll_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ፸"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፹"): env.get(bstack11llll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ፺")),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፻"): bstack11llll_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦ፼") if env.get(bstack11llll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ፽")) else None,
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ፾"): env.get(bstack11llll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧ፿"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᎀ")), env.get(bstack11llll_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᎁ")), env.get(bstack11llll_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᎂ"))]):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᎃ"): bstack11llll_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦᎄ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᎅ"): None,
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎆ"): env.get(bstack11llll_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᎇ")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎈ"): env.get(bstack11llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᎉ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢᎊ")):
        return {
            bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎋ"): bstack11llll_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤᎌ"),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎍ"): env.get(bstack11llll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᎎ")),
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎏ"): bstack11llll_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦ᎐").format(env.get(bstack11llll_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ᎑"))) if env.get(bstack11llll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣ᎒")) else None,
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᎓"): env.get(bstack11llll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᎔"))
        }
    if bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤ᎕"))):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᎖"): bstack11llll_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦ᎗"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎘"): env.get(bstack11llll_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤ᎙")),
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᎚"): env.get(bstack11llll_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥ᎛")),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᎜"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᎝"))
        }
    if bstack11ll1llll_opy_(env.get(bstack11llll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦ᎞"))):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᎟"): bstack11llll_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨᎠ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᎡ"): bstack11llll_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣᎢ").format(env.get(bstack11llll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬᎣ")), env.get(bstack11llll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭Ꭴ")), env.get(bstack11llll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪᎥ"))),
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎦ"): env.get(bstack11llll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢᎧ")),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎨ"): env.get(bstack11llll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢᎩ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠣࡅࡌࠦᎪ")) == bstack11llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᎫ") and env.get(bstack11llll_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥᎬ")) == bstack11llll_opy_ (u"ࠦ࠶ࠨᎭ"):
        return {
            bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎮ"): bstack11llll_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨᎯ"),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎰ"): bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦᎱ").format(env.get(bstack11llll_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭Ꮂ"))),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᎳ"): None,
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎴ"): None,
        }
    if env.get(bstack11llll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣᎵ")):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎶ"): bstack11llll_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤᎷ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎸ"): None,
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎹ"): env.get(bstack11llll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦᎺ")),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎻ"): env.get(bstack11llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᎼ"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤᎽ")), env.get(bstack11llll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢᎾ")), env.get(bstack11llll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨᎿ")), env.get(bstack11llll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥᏀ"))]):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᏁ"): bstack11llll_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢᏂ"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏃ"): None,
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᏄ"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᏅ")) or None,
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏆ"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᏇ"), 0)
        }
    if env.get(bstack11llll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᏈ")):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏉ"): bstack11llll_opy_ (u"ࠧࡍ࡯ࡄࡆࠥᏊ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏋ"): None,
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏌ"): env.get(bstack11llll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᏍ")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏎ"): env.get(bstack11llll_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤᏏ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᏐ")):
        return {
            bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏑ"): bstack11llll_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤᏒ"),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏓ"): env.get(bstack11llll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᏔ")),
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏕ"): env.get(bstack11llll_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᏖ")),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏗ"): env.get(bstack11llll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᏘ"))
        }
    return {bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏙ"): None}
def get_host_info():
    return {
        bstack11llll_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤᏚ"): platform.node(),
        bstack11llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥᏛ"): platform.system(),
        bstack11llll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᏜ"): platform.machine(),
        bstack11llll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᏝ"): platform.version(),
        bstack11llll_opy_ (u"ࠦࡦࡸࡣࡩࠤᏞ"): platform.architecture()[0]
    }
def bstack11l1l1l1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l1l11l1_opy_():
    if bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭Ꮯ")):
        return bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᏠ")
    return bstack11llll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭Ꮱ")
def bstack111l11l11l_opy_(driver):
    info = {
        bstack11llll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᏢ"): driver.capabilities,
        bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭Ꮳ"): driver.session_id,
        bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᏤ"): driver.capabilities.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᏥ"), None),
        bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᏦ"): driver.capabilities.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᏧ"), None),
        bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᏨ"): driver.capabilities.get(bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᏩ"), None),
    }
    if bstack111l1l11l1_opy_() == bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᏪ"):
        info[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᏫ")] = bstack11llll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᏬ") if bstack11lllll11_opy_() else bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᏭ")
    return info
def bstack11lllll11_opy_():
    if bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᏮ")):
        return True
    if bstack11ll1llll_opy_(os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᏯ"), None)):
        return True
    return False
def bstack11lll111l_opy_(bstack11111lll1l_opy_, url, data, config):
    headers = config.get(bstack11llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᏰ"), None)
    proxies = bstack1ll11ll11_opy_(config, url)
    auth = config.get(bstack11llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᏱ"), None)
    response = requests.request(
            bstack11111lll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll1l11_opy_(bstack1llllll111_opy_, size):
    bstack1ll1ll1ll1_opy_ = []
    while len(bstack1llllll111_opy_) > size:
        bstack11lll11l11_opy_ = bstack1llllll111_opy_[:size]
        bstack1ll1ll1ll1_opy_.append(bstack11lll11l11_opy_)
        bstack1llllll111_opy_ = bstack1llllll111_opy_[size:]
    bstack1ll1ll1ll1_opy_.append(bstack1llllll111_opy_)
    return bstack1ll1ll1ll1_opy_
def bstack111l11ll1l_opy_(message, bstack11111lllll_opy_=False):
    os.write(1, bytes(message, bstack11llll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᏲ")))
    os.write(1, bytes(bstack11llll_opy_ (u"ࠫࡡࡴࠧᏳ"), bstack11llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᏴ")))
    if bstack11111lllll_opy_:
        with open(bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᏵ") + os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭᏶")] + bstack11llll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭᏷"), bstack11llll_opy_ (u"ࠩࡤࠫᏸ")) as f:
            f.write(message + bstack11llll_opy_ (u"ࠪࡠࡳ࠭ᏹ"))
def bstack111l1lllll_opy_():
    return os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᏺ")].lower() == bstack11llll_opy_ (u"ࠬࡺࡲࡶࡧࠪᏻ")
def bstack1l1l11l1ll_opy_(bstack11111ll11l_opy_):
    return bstack11llll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᏼ").format(bstack111ll1l1l1_opy_, bstack11111ll11l_opy_)
def bstack1l1lll1l_opy_():
    return bstack11ll111l_opy_().replace(tzinfo=None).isoformat() + bstack11llll_opy_ (u"࡛ࠧࠩᏽ")
def bstack1111l1ll11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11llll_opy_ (u"ࠨ࡜ࠪ᏾"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11llll_opy_ (u"ࠩ࡝ࠫ᏿")))).total_seconds() * 1000
def bstack1111l11111_opy_(timestamp):
    return bstack11111ll1ll_opy_(timestamp).isoformat() + bstack11llll_opy_ (u"ࠪ࡞ࠬ᐀")
def bstack1111l11l11_opy_(bstack111ll111ll_opy_):
    date_format = bstack11llll_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᐁ")
    bstack1111ll11l1_opy_ = datetime.datetime.strptime(bstack111ll111ll_opy_, date_format)
    return bstack1111ll11l1_opy_.isoformat() + bstack11llll_opy_ (u"ࠬࡠࠧᐂ")
def bstack111l1l111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐃ")
    else:
        return bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐄ")
def bstack11ll1llll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᐅ")
def bstack111l1ll111_opy_(val):
    return val.__str__().lower() == bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᐆ")
def bstack11l1l11l_opy_(bstack11111llll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11111llll1_opy_ as e:
                print(bstack11llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᐇ").format(func.__name__, bstack11111llll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111lllll1_opy_(bstack11111l1l1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l1l1l_opy_(cls, *args, **kwargs)
            except bstack11111llll1_opy_ as e:
                print(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᐈ").format(bstack11111l1l1l_opy_.__name__, bstack11111llll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111lllll1_opy_
    else:
        return decorator
def bstack1l1l1l1ll_opy_(bstack1111l1l1_opy_):
    if bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᐉ") in bstack1111l1l1_opy_ and bstack111l1ll111_opy_(bstack1111l1l1_opy_[bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᐊ")]):
        return False
    if bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᐋ") in bstack1111l1l1_opy_ and bstack111l1ll111_opy_(bstack1111l1l1_opy_[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᐌ")]):
        return False
    return True
def bstack11l1lll1l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lllll11l1_opy_(hub_url):
    if bstack1l111l11ll_opy_() <= version.parse(bstack11llll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᐍ")):
        if hub_url != bstack11llll_opy_ (u"ࠪࠫᐎ"):
            return bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᐏ") + hub_url + bstack11llll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᐐ")
        return bstack1111111l1_opy_
    if hub_url != bstack11llll_opy_ (u"࠭ࠧᐑ"):
        return bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᐒ") + hub_url + bstack11llll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᐓ")
    return bstack1lll1ll111_opy_
def bstack111l1l1l1l_opy_():
    return isinstance(os.getenv(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᐔ")), str)
def bstack11lll1l11_opy_(url):
    return urlparse(url).hostname
def bstack11lll11ll_opy_(hostname):
    for bstack1l111ll11_opy_ in bstack1l111l111_opy_:
        regex = re.compile(bstack1l111ll11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111l1111l_opy_(bstack1111l1l1ll_opy_, file_name, logger):
    bstack1lll1llll1_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬᐕ")), bstack1111l1l1ll_opy_)
    try:
        if not os.path.exists(bstack1lll1llll1_opy_):
            os.makedirs(bstack1lll1llll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠫࢃ࠭ᐖ")), bstack1111l1l1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11llll_opy_ (u"ࠬࡽࠧᐗ")):
                pass
            with open(file_path, bstack11llll_opy_ (u"ࠨࡷࠬࠤᐘ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111llll11_opy_.format(str(e)))
def bstack111l1l1l11_opy_(file_name, key, value, logger):
    file_path = bstack1111l1111l_opy_(bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᐙ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1llll1_opy_ = json.load(open(file_path, bstack11llll_opy_ (u"ࠨࡴࡥࠫᐚ")))
        else:
            bstack11l1llll1_opy_ = {}
        bstack11l1llll1_opy_[key] = value
        with open(file_path, bstack11llll_opy_ (u"ࠤࡺ࠯ࠧᐛ")) as outfile:
            json.dump(bstack11l1llll1_opy_, outfile)
def bstack1l1l1ll11l_opy_(file_name, logger):
    file_path = bstack1111l1111l_opy_(bstack11llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᐜ"), file_name, logger)
    bstack11l1llll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11llll_opy_ (u"ࠫࡷ࠭ᐝ")) as bstack1ll1l11111_opy_:
            bstack11l1llll1_opy_ = json.load(bstack1ll1l11111_opy_)
    return bstack11l1llll1_opy_
def bstack1l11l1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᐞ") + file_path + bstack11llll_opy_ (u"࠭ࠠࠨᐟ") + str(e))
def bstack1l111l11ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11llll_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᐠ")
def bstack1l111llll_opy_(config):
    if bstack11llll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᐡ") in config:
        del (config[bstack11llll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᐢ")])
        return False
    if bstack1l111l11ll_opy_() < version.parse(bstack11llll_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᐣ")):
        return False
    if bstack1l111l11ll_opy_() >= version.parse(bstack11llll_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᐤ")):
        return True
    if bstack11llll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᐥ") in config and config[bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᐦ")] is False:
        return False
    else:
        return True
def bstack1ll11l11l_opy_(args_list, bstack11111l1l11_opy_):
    index = -1
    for value in bstack11111l1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1ll111ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1ll111ll_opy_ = bstack1ll111ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐧ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐨ"), exception=exception)
    def bstack1lllll111_opy_(self):
        if self.result != bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐩ"):
            return None
        if isinstance(self.exception_type, str) and bstack11llll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᐪ") in self.exception_type:
            return bstack11llll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᐫ")
        return bstack11llll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᐬ")
    def bstack1111l1l1l1_opy_(self):
        if self.result != bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐭ"):
            return None
        if self.bstack1ll111ll_opy_:
            return self.bstack1ll111ll_opy_
        return bstack111111llll_opy_(self.exception)
def bstack111111llll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l11lll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll1111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1l1l1l1_opy_(config, logger):
    try:
        import playwright
        bstack1111llllll_opy_ = playwright.__file__
        bstack11111l11ll_opy_ = os.path.split(bstack1111llllll_opy_)
        bstack111l11llll_opy_ = bstack11111l11ll_opy_[0] + bstack11llll_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᐮ")
        os.environ[bstack11llll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᐯ")] = bstack11111ll11_opy_(config)
        with open(bstack111l11llll_opy_, bstack11llll_opy_ (u"ࠩࡵࠫᐰ")) as f:
            bstack1l1ll1ll1_opy_ = f.read()
            bstack111l1lll1l_opy_ = bstack11llll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᐱ")
            bstack111l1llll1_opy_ = bstack1l1ll1ll1_opy_.find(bstack111l1lll1l_opy_)
            if bstack111l1llll1_opy_ == -1:
              process = subprocess.Popen(bstack11llll_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᐲ"), shell=True, cwd=bstack11111l11ll_opy_[0])
              process.wait()
              bstack111l111111_opy_ = bstack11llll_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᐳ")
              bstack111l1111l1_opy_ = bstack11llll_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᐴ")
              bstack1111l111ll_opy_ = bstack1l1ll1ll1_opy_.replace(bstack111l111111_opy_, bstack111l1111l1_opy_)
              with open(bstack111l11llll_opy_, bstack11llll_opy_ (u"ࠧࡸࠩᐵ")) as f:
                f.write(bstack1111l111ll_opy_)
    except Exception as e:
        logger.error(bstack1l1ll1lll_opy_.format(str(e)))
def bstack1ll1111l11_opy_():
  try:
    bstack111l11111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᐶ"))
    bstack111l1l11ll_opy_ = []
    if os.path.exists(bstack111l11111l_opy_):
      with open(bstack111l11111l_opy_) as f:
        bstack111l1l11ll_opy_ = json.load(f)
      os.remove(bstack111l11111l_opy_)
    return bstack111l1l11ll_opy_
  except:
    pass
  return []
def bstack111l1llll_opy_(bstack11llll1ll_opy_):
  try:
    bstack111l1l11ll_opy_ = []
    bstack111l11111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᐷ"))
    if os.path.exists(bstack111l11111l_opy_):
      with open(bstack111l11111l_opy_) as f:
        bstack111l1l11ll_opy_ = json.load(f)
    bstack111l1l11ll_opy_.append(bstack11llll1ll_opy_)
    with open(bstack111l11111l_opy_, bstack11llll_opy_ (u"ࠪࡻࠬᐸ")) as f:
        json.dump(bstack111l1l11ll_opy_, f)
  except:
    pass
def bstack1lll1ll11l_opy_(logger, bstack111l111l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack11llll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᐹ"), bstack11llll_opy_ (u"ࠬ࠭ᐺ"))
    if test_name == bstack11llll_opy_ (u"࠭ࠧᐻ"):
        test_name = threading.current_thread().__dict__.get(bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᐼ"), bstack11llll_opy_ (u"ࠨࠩᐽ"))
    bstack111l111lll_opy_ = bstack11llll_opy_ (u"ࠩ࠯ࠤࠬᐾ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l111l11_opy_:
        bstack111lll1l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᐿ"), bstack11llll_opy_ (u"ࠫ࠵࠭ᑀ"))
        bstack1l1l111l1l_opy_ = {bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑁ"): test_name, bstack11llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᑂ"): bstack111l111lll_opy_, bstack11llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᑃ"): bstack111lll1l1_opy_}
        bstack1111l1llll_opy_ = []
        bstack1111lll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᑄ"))
        if os.path.exists(bstack1111lll1l1_opy_):
            with open(bstack1111lll1l1_opy_) as f:
                bstack1111l1llll_opy_ = json.load(f)
        bstack1111l1llll_opy_.append(bstack1l1l111l1l_opy_)
        with open(bstack1111lll1l1_opy_, bstack11llll_opy_ (u"ࠩࡺࠫᑅ")) as f:
            json.dump(bstack1111l1llll_opy_, f)
    else:
        bstack1l1l111l1l_opy_ = {bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᑆ"): test_name, bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᑇ"): bstack111l111lll_opy_, bstack11llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᑈ"): str(multiprocessing.current_process().name)}
        if bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᑉ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l111l1l_opy_)
  except Exception as e:
      logger.warn(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᑊ").format(e))
def bstack1ll1lll1l_opy_(error_message, test_name, index, logger):
  try:
    bstack111ll1111l_opy_ = []
    bstack1l1l111l1l_opy_ = {bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑋ"): test_name, bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᑌ"): error_message, bstack11llll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᑍ"): index}
    bstack1111llll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᑎ"))
    if os.path.exists(bstack1111llll1l_opy_):
        with open(bstack1111llll1l_opy_) as f:
            bstack111ll1111l_opy_ = json.load(f)
    bstack111ll1111l_opy_.append(bstack1l1l111l1l_opy_)
    with open(bstack1111llll1l_opy_, bstack11llll_opy_ (u"ࠬࡽࠧᑏ")) as f:
        json.dump(bstack111ll1111l_opy_, f)
  except Exception as e:
    logger.warn(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᑐ").format(e))
def bstack1l11l1l1ll_opy_(bstack1lll11l11l_opy_, name, logger):
  try:
    bstack1l1l111l1l_opy_ = {bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑑ"): name, bstack11llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᑒ"): bstack1lll11l11l_opy_, bstack11llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᑓ"): str(threading.current_thread()._name)}
    return bstack1l1l111l1l_opy_
  except Exception as e:
    logger.warn(bstack11llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᑔ").format(e))
  return
def bstack111l1lll11_opy_():
    return platform.system() == bstack11llll_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᑕ")
def bstack11l1111l1_opy_(bstack1111ll1111_opy_, config, logger):
    bstack1111ll1l11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111ll1111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᑖ").format(e))
    return bstack1111ll1l11_opy_
def bstack11111l1lll_opy_(bstack111l1l1111_opy_, bstack11111ll111_opy_):
    bstack11111l11l1_opy_ = version.parse(bstack111l1l1111_opy_)
    bstack111l11l111_opy_ = version.parse(bstack11111ll111_opy_)
    if bstack11111l11l1_opy_ > bstack111l11l111_opy_:
        return 1
    elif bstack11111l11l1_opy_ < bstack111l11l111_opy_:
        return -1
    else:
        return 0
def bstack11ll111l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111ll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111lll11l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll111111_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack11llll_opy_ (u"࠭ࡧࡦࡶࠪᑗ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1ll1l1l_opy_ = caps.get(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑘ"))
    bstack1111lll111_opy_ = True
    if bstack111l1ll111_opy_(caps.get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᑙ"))) or bstack111l1ll111_opy_(caps.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᑚ"))):
        bstack1111lll111_opy_ = False
    if bstack1l111llll_opy_({bstack11llll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᑛ"): bstack1111lll111_opy_}):
        bstack11l1ll1l1l_opy_ = bstack11l1ll1l1l_opy_ or {}
        bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑜ")] = bstack1111lll11l_opy_(framework)
        bstack11l1ll1l1l_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑝ")] = bstack111l1lllll_opy_()
        if getattr(options, bstack11llll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᑞ"), None):
            options.set_capability(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑟ"), bstack11l1ll1l1l_opy_)
        else:
            options[bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᑠ")] = bstack11l1ll1l1l_opy_
    else:
        if getattr(options, bstack11llll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᑡ"), None):
            options.set_capability(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑢ"), bstack1111lll11l_opy_(framework))
            options.set_capability(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑣ"), bstack111l1lllll_opy_())
        else:
            options[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑤ")] = bstack1111lll11l_opy_(framework)
            options[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑥ")] = bstack111l1lllll_opy_()
    return options
def bstack111l11l1ll_opy_(bstack111ll111l1_opy_, framework):
    if bstack111ll111l1_opy_ and len(bstack111ll111l1_opy_.split(bstack11llll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᑦ"))) > 1:
        ws_url = bstack111ll111l1_opy_.split(bstack11llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑧ"))[0]
        if bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᑨ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1l111_opy_ = json.loads(urllib.parse.unquote(bstack111ll111l1_opy_.split(bstack11llll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᑩ"))[1]))
            bstack1111l1l111_opy_ = bstack1111l1l111_opy_ or {}
            bstack1111l1l111_opy_[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᑪ")] = str(framework) + str(__version__)
            bstack1111l1l111_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᑫ")] = bstack111l1lllll_opy_()
            bstack111ll111l1_opy_ = bstack111ll111l1_opy_.split(bstack11llll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᑬ"))[0] + bstack11llll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᑭ") + urllib.parse.quote(json.dumps(bstack1111l1l111_opy_))
    return bstack111ll111l1_opy_
def bstack1l11ll1l1_opy_():
    global bstack111111l1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111111l1l_opy_ = BrowserType.connect
    return bstack111111l1l_opy_
def bstack1l1111llll_opy_(framework_name):
    global bstack1ll1ll111l_opy_
    bstack1ll1ll111l_opy_ = framework_name
    return framework_name
def bstack111ll11l1_opy_(self, *args, **kwargs):
    global bstack111111l1l_opy_
    try:
        global bstack1ll1ll111l_opy_
        if bstack11llll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᑮ") in kwargs:
            kwargs[bstack11llll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᑯ")] = bstack111l11l1ll_opy_(
                kwargs.get(bstack11llll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᑰ"), None),
                bstack1ll1ll111l_opy_
            )
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᑱ").format(str(e)))
    return bstack111111l1l_opy_(self, *args, **kwargs)
def bstack11111l1ll1_opy_(bstack11111l111l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll11ll11_opy_(bstack11111l111l_opy_, bstack11llll_opy_ (u"ࠧࠨᑲ"))
        if proxies and proxies.get(bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᑳ")):
            parsed_url = urlparse(proxies.get(bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᑴ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᑵ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᑶ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᑷ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᑸ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11llll11_opy_(bstack11111l111l_opy_):
    bstack111l11l1l1_opy_ = {
        bstack111lll11l1_opy_[bstack111ll11111_opy_]: bstack11111l111l_opy_[bstack111ll11111_opy_]
        for bstack111ll11111_opy_ in bstack11111l111l_opy_
        if bstack111ll11111_opy_ in bstack111lll11l1_opy_
    }
    bstack111l11l1l1_opy_[bstack11llll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᑹ")] = bstack11111l1ll1_opy_(bstack11111l111l_opy_, bstack1111111l_opy_.get_property(bstack11llll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᑺ")))
    bstack1111ll111l_opy_ = [element.lower() for element in bstack111ll1ll1l_opy_]
    bstack1111llll11_opy_(bstack111l11l1l1_opy_, bstack1111ll111l_opy_)
    return bstack111l11l1l1_opy_
def bstack1111llll11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11llll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᑻ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111llll11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111llll11_opy_(item, keys)