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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111ll11l11_opy_, bstack111ll1ll1l_opy_
import tempfile
import json
bstack1llllll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᒧ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11llll_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᒨ"),
      datefmt=bstack11llll_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᒩ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllllll111_opy_():
  global bstack1llllll11ll_opy_
  if os.path.exists(bstack1llllll11ll_opy_):
    os.remove(bstack1llllll11ll_opy_)
def bstack1l1lll1l1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1111l111l_opy_(config, log_level):
  bstack1llllllll1l_opy_ = log_level
  if bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᒪ") in config and config[bstack11llll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᒫ")] in bstack111ll11l11_opy_:
    bstack1llllllll1l_opy_ = bstack111ll11l11_opy_[config[bstack11llll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᒬ")]]
  if config.get(bstack11llll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᒭ"), False):
    logging.getLogger().setLevel(bstack1llllllll1l_opy_)
    return bstack1llllllll1l_opy_
  global bstack1llllll11ll_opy_
  bstack1l1lll1l1l_opy_()
  bstack1llllllllll_opy_ = logging.Formatter(
    fmt=bstack11llll_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᒮ"),
    datefmt=bstack11llll_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᒯ")
  )
  bstack1lllllllll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llllll11ll_opy_)
  file_handler.setFormatter(bstack1llllllllll_opy_)
  bstack1lllllllll1_opy_.setFormatter(bstack1llllllllll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllllllll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᒰ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllllllll1_opy_.setLevel(bstack1llllllll1l_opy_)
  logging.getLogger().addHandler(bstack1lllllllll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llllllll1l_opy_
def bstack1llllllll11_opy_(config):
  try:
    bstack1lllllll1ll_opy_ = set(bstack111ll1ll1l_opy_)
    bstack1llllll11l1_opy_ = bstack11llll_opy_ (u"ࠬ࠭ᒱ")
    with open(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᒲ")) as bstack1llllll1lll_opy_:
      bstack1llllll1ll1_opy_ = bstack1llllll1lll_opy_.read()
      bstack1llllll11l1_opy_ = re.sub(bstack11llll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᒳ"), bstack11llll_opy_ (u"ࠨࠩᒴ"), bstack1llllll1ll1_opy_, flags=re.M)
      bstack1llllll11l1_opy_ = re.sub(
        bstack11llll_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᒵ") + bstack11llll_opy_ (u"ࠪࢀࠬᒶ").join(bstack1lllllll1ll_opy_) + bstack11llll_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᒷ"),
        bstack11llll_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᒸ"),
        bstack1llllll11l1_opy_, flags=re.M | re.I
      )
    def bstack1lllllll11l_opy_(dic):
      bstack1lllllll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllllll1ll_opy_:
          bstack1lllllll1l1_opy_[key] = bstack11llll_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᒹ")
        else:
          if isinstance(value, dict):
            bstack1lllllll1l1_opy_[key] = bstack1lllllll11l_opy_(value)
          else:
            bstack1lllllll1l1_opy_[key] = value
      return bstack1lllllll1l1_opy_
    bstack1lllllll1l1_opy_ = bstack1lllllll11l_opy_(config)
    return {
      bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᒺ"): bstack1llllll11l1_opy_,
      bstack11llll_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒻ"): json.dumps(bstack1lllllll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1ll1l_opy_(config):
  global bstack1llllll11ll_opy_
  try:
    if config.get(bstack11llll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᒼ"), False):
      return
    uuid = os.getenv(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᒽ"))
    if not uuid or uuid == bstack11llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᒾ"):
      return
    bstack1llllll1l11_opy_ = [bstack11llll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᒿ"), bstack11llll_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᓀ"), bstack11llll_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᓁ"), bstack1llllll11ll_opy_]
    bstack1l1lll1l1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᓂ") + uuid + bstack11llll_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᓃ"))
    with tarfile.open(output_file, bstack11llll_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᓄ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llllll1l11_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llllllll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll1l1l_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll1l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll1l1l_opy_))
    bstack11l1lll11l_opy_ = MultipartEncoder(
      fields= {
        bstack11llll_opy_ (u"ࠫࡩࡧࡴࡢࠩᓅ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11llll_opy_ (u"ࠬࡸࡢࠨᓆ")), bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᓇ")),
        bstack11llll_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᓈ"): uuid
      }
    )
    response = requests.post(
      bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᓉ"),
      data=bstack11l1lll11l_opy_,
      headers={bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᓊ"): bstack11l1lll11l_opy_.content_type},
      auth=(config[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᓋ")], config[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᓌ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᓍ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᓎ") + str(e))
  finally:
    try:
      bstack1lllllll111_opy_()
    except:
      pass