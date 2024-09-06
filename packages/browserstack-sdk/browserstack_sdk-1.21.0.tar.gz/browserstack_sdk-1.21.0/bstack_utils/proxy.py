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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll1ll1l_opy_
bstack1111111l_opy_ = Config.bstack111l11ll_opy_()
def bstack1lll1l11l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l111ll_opy_(bstack1lll1l11l1l_opy_, bstack1lll1l11ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1l11l1l_opy_):
        with open(bstack1lll1l11l1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1l11l11_opy_(bstack1lll1l11l1l_opy_):
        pac = get_pac(url=bstack1lll1l11l1l_opy_)
    else:
        raise Exception(bstack11llll_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᕾ").format(bstack1lll1l11l1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11llll_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᕿ"), 80))
        bstack1lll1l11lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1l11lll_opy_ = bstack11llll_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᖀ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l11ll1_opy_, bstack1lll1l11lll_opy_)
    return proxy_url
def bstack1l1l1111l_opy_(config):
    return bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᖁ") in config or bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᖂ") in config
def bstack11111ll11_opy_(config):
    if not bstack1l1l1111l_opy_(config):
        return
    if config.get(bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖃ")):
        return config.get(bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᖄ"))
    if config.get(bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᖅ")):
        return config.get(bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᖆ"))
def bstack1ll11ll11_opy_(config, bstack1lll1l11ll1_opy_):
    proxy = bstack11111ll11_opy_(config)
    proxies = {}
    if config.get(bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᖇ")) or config.get(bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖈ")):
        if proxy.endswith(bstack11llll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᖉ")):
            proxies = bstack11lll1lll1_opy_(proxy, bstack1lll1l11ll1_opy_)
        else:
            proxies = {
                bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᖊ"): proxy
            }
    bstack1111111l_opy_.bstack1ll1l1l111_opy_(bstack11llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᖋ"), proxies)
    return proxies
def bstack11lll1lll1_opy_(bstack1lll1l11l1l_opy_, bstack1lll1l11ll1_opy_):
    proxies = {}
    global bstack1lll1l1l111_opy_
    if bstack11llll_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᖌ") in globals():
        return bstack1lll1l1l111_opy_
    try:
        proxy = bstack1lll1l111ll_opy_(bstack1lll1l11l1l_opy_, bstack1lll1l11ll1_opy_)
        if bstack11llll_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᖍ") in proxy:
            proxies = {}
        elif bstack11llll_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᖎ") in proxy or bstack11llll_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᖏ") in proxy or bstack11llll_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᖐ") in proxy:
            bstack1lll1l1l11l_opy_ = proxy.split(bstack11llll_opy_ (u"ࠧࠦࠢᖑ"))
            if bstack11llll_opy_ (u"ࠨ࠺࠰࠱ࠥᖒ") in bstack11llll_opy_ (u"ࠢࠣᖓ").join(bstack1lll1l1l11l_opy_[1:]):
                proxies = {
                    bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): bstack11llll_opy_ (u"ࠤࠥᖕ").join(bstack1lll1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖖ"): str(bstack1lll1l1l11l_opy_[0]).lower() + bstack11llll_opy_ (u"ࠦ࠿࠵࠯ࠣᖗ") + bstack11llll_opy_ (u"ࠧࠨᖘ").join(bstack1lll1l1l11l_opy_[1:])
                }
        elif bstack11llll_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᖙ") in proxy:
            bstack1lll1l1l11l_opy_ = proxy.split(bstack11llll_opy_ (u"ࠢࠡࠤᖚ"))
            if bstack11llll_opy_ (u"ࠣ࠼࠲࠳ࠧᖛ") in bstack11llll_opy_ (u"ࠤࠥᖜ").join(bstack1lll1l1l11l_opy_[1:]):
                proxies = {
                    bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖝ"): bstack11llll_opy_ (u"ࠦࠧᖞ").join(bstack1lll1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᖟ"): bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᖠ") + bstack11llll_opy_ (u"ࠢࠣᖡ").join(bstack1lll1l1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖢ"): proxy
            }
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᖣ"), bstack1lllll1ll1l_opy_.format(bstack1lll1l11l1l_opy_, str(e)))
    bstack1lll1l1l111_opy_ = proxies
    return proxies