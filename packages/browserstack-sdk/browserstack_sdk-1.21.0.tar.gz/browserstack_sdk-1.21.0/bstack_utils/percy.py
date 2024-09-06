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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1l11l1ll_opy_, bstack11lll111l_opy_
class bstack1l11l1l11l_opy_:
  working_dir = os.getcwd()
  bstack11lllll11_opy_ = False
  config = {}
  binary_path = bstack11llll_opy_ (u"ࠨࠩᔖ")
  bstack1llll11l11l_opy_ = bstack11llll_opy_ (u"ࠩࠪᔗ")
  bstack1l1ll1l111_opy_ = False
  bstack1lllll11lll_opy_ = None
  bstack1llll1lllll_opy_ = {}
  bstack1llll1lll11_opy_ = 300
  bstack1lllll1l111_opy_ = False
  logger = None
  bstack1llll1ll11l_opy_ = False
  bstack1llll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠪࠫᔘ")
  bstack1lllll11l1l_opy_ = {
    bstack11llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᔙ") : 1,
    bstack11llll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᔚ") : 2,
    bstack11llll_opy_ (u"࠭ࡥࡥࡩࡨࠫᔛ") : 3,
    bstack11llll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᔜ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll1l11l1_opy_(self):
    bstack1llll1111l1_opy_ = bstack11llll_opy_ (u"ࠨࠩᔝ")
    bstack1llll1ll1l1_opy_ = sys.platform
    bstack1lll1llllll_opy_ = bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᔞ")
    if re.match(bstack11llll_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᔟ"), bstack1llll1ll1l1_opy_) != None:
      bstack1llll1111l1_opy_ = bstack111ll1llll_opy_ + bstack11llll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᔠ")
      self.bstack1llll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠬࡳࡡࡤࠩᔡ")
    elif re.match(bstack11llll_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᔢ"), bstack1llll1ll1l1_opy_) != None:
      bstack1llll1111l1_opy_ = bstack111ll1llll_opy_ + bstack11llll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᔣ")
      bstack1lll1llllll_opy_ = bstack11llll_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᔤ")
      self.bstack1llll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠩࡺ࡭ࡳ࠭ᔥ")
    else:
      bstack1llll1111l1_opy_ = bstack111ll1llll_opy_ + bstack11llll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᔦ")
      self.bstack1llll1l1l1l_opy_ = bstack11llll_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᔧ")
    return bstack1llll1111l1_opy_, bstack1lll1llllll_opy_
  def bstack1llll111ll1_opy_(self):
    try:
      bstack1lllll111ll_opy_ = [os.path.join(expanduser(bstack11llll_opy_ (u"ࠧࢄࠢᔨ")), bstack11llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᔩ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lllll111ll_opy_:
        if(self.bstack1llll111l1l_opy_(path)):
          return path
      raise bstack11llll_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᔪ")
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᔫ").format(e))
  def bstack1llll111l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1lll1ll_opy_(self, bstack1llll1111l1_opy_, bstack1lll1llllll_opy_):
    try:
      bstack1llll1l1ll1_opy_ = self.bstack1llll111ll1_opy_()
      bstack1llll1l111l_opy_ = os.path.join(bstack1llll1l1ll1_opy_, bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᔬ"))
      bstack1llll1ll111_opy_ = os.path.join(bstack1llll1l1ll1_opy_, bstack1lll1llllll_opy_)
      if os.path.exists(bstack1llll1ll111_opy_):
        self.logger.info(bstack11llll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᔭ").format(bstack1llll1ll111_opy_))
        return bstack1llll1ll111_opy_
      if os.path.exists(bstack1llll1l111l_opy_):
        self.logger.info(bstack11llll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᔮ").format(bstack1llll1l111l_opy_))
        return self.bstack1lllll1l11l_opy_(bstack1llll1l111l_opy_, bstack1lll1llllll_opy_)
      self.logger.info(bstack11llll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᔯ").format(bstack1llll1111l1_opy_))
      response = bstack11lll111l_opy_(bstack11llll_opy_ (u"࠭ࡇࡆࡖࠪᔰ"), bstack1llll1111l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1llll1l111l_opy_, bstack11llll_opy_ (u"ࠧࡸࡤࠪᔱ")) as file:
          file.write(response.content)
        self.logger.info(bstack11llll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᔲ").format(bstack1llll1l111l_opy_))
        return self.bstack1lllll1l11l_opy_(bstack1llll1l111l_opy_, bstack1lll1llllll_opy_)
      else:
        raise(bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᔳ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᔴ").format(e))
  def bstack1llll11l1l1_opy_(self, bstack1llll1111l1_opy_, bstack1lll1llllll_opy_):
    try:
      retry = 2
      bstack1llll1ll111_opy_ = None
      bstack1llll11l111_opy_ = False
      while retry > 0:
        bstack1llll1ll111_opy_ = self.bstack1lll1lll1ll_opy_(bstack1llll1111l1_opy_, bstack1lll1llllll_opy_)
        bstack1llll11l111_opy_ = self.bstack1lllll11111_opy_(bstack1llll1111l1_opy_, bstack1lll1llllll_opy_, bstack1llll1ll111_opy_)
        if bstack1llll11l111_opy_:
          break
        retry -= 1
      return bstack1llll1ll111_opy_, bstack1llll11l111_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᔵ").format(e))
    return bstack1llll1ll111_opy_, False
  def bstack1lllll11111_opy_(self, bstack1llll1111l1_opy_, bstack1lll1llllll_opy_, bstack1llll1ll111_opy_, bstack1llll11llll_opy_ = 0):
    if bstack1llll11llll_opy_ > 1:
      return False
    if bstack1llll1ll111_opy_ == None or os.path.exists(bstack1llll1ll111_opy_) == False:
      self.logger.warn(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᔶ"))
      return False
    bstack1lll1lllll1_opy_ = bstack11llll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᔷ")
    command = bstack11llll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔸ").format(bstack1llll1ll111_opy_)
    bstack1llll1lll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1lll1lllll1_opy_, bstack1llll1lll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᔹ"))
      return False
  def bstack1lllll1l11l_opy_(self, bstack1llll1l111l_opy_, bstack1lll1llllll_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll1l111l_opy_)
      shutil.unpack_archive(bstack1llll1l111l_opy_, working_dir)
      bstack1llll1ll111_opy_ = os.path.join(working_dir, bstack1lll1llllll_opy_)
      os.chmod(bstack1llll1ll111_opy_, 0o755)
      return bstack1llll1ll111_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᔺ"))
  def bstack1lll1lll11l_opy_(self):
    try:
      percy = str(self.config.get(bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᔻ"), bstack11llll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᔼ"))).lower()
      if percy != bstack11llll_opy_ (u"ࠧࡺࡲࡶࡧࠥᔽ"):
        return False
      self.bstack1l1ll1l111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᔾ").format(e))
  def bstack1lllll111l1_opy_(self):
    try:
      bstack1lllll111l1_opy_ = str(self.config.get(bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᔿ"), bstack11llll_opy_ (u"ࠣࡣࡸࡸࡴࠨᕀ"))).lower()
      return bstack1lllll111l1_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕁ").format(e))
  def init(self, bstack11lllll11_opy_, config, logger):
    self.bstack11lllll11_opy_ = bstack11lllll11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll1lll11l_opy_():
      return
    self.bstack1llll1lllll_opy_ = config.get(bstack11llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᕂ"), {})
    self.bstack1lll1llll1l_opy_ = config.get(bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᕃ"), bstack11llll_opy_ (u"ࠧࡧࡵࡵࡱࠥᕄ"))
    try:
      bstack1llll1111l1_opy_, bstack1lll1llllll_opy_ = self.bstack1llll1l11l1_opy_()
      bstack1llll1ll111_opy_, bstack1llll11l111_opy_ = self.bstack1llll11l1l1_opy_(bstack1llll1111l1_opy_, bstack1lll1llllll_opy_)
      if bstack1llll11l111_opy_:
        self.binary_path = bstack1llll1ll111_opy_
        thread = Thread(target=self.bstack1llll11ll11_opy_)
        thread.start()
      else:
        self.bstack1llll1ll11l_opy_ = True
        self.logger.error(bstack11llll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᕅ").format(bstack1llll1ll111_opy_))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕆ").format(e))
  def bstack1lll1llll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11llll_opy_ (u"ࠨ࡮ࡲ࡫ࠬᕇ"), bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᕈ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11llll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᕉ").format(logfile))
      self.bstack1llll11l11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᕊ").format(e))
  def bstack1llll11ll11_opy_(self):
    bstack1lllll1111l_opy_ = self.bstack1llll111l11_opy_()
    if bstack1lllll1111l_opy_ == None:
      self.bstack1llll1ll11l_opy_ = True
      self.logger.error(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᕋ"))
      return False
    command_args = [bstack11llll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᕌ") if self.bstack11lllll11_opy_ else bstack11llll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᕍ")]
    bstack1lllll11l11_opy_ = self.bstack1llll1llll1_opy_()
    if bstack1lllll11l11_opy_ != None:
      command_args.append(bstack11llll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᕎ").format(bstack1lllll11l11_opy_))
    env = os.environ.copy()
    env[bstack11llll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᕏ")] = bstack1lllll1111l_opy_
    env[bstack11llll_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᕐ")] = os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᕑ"), bstack11llll_opy_ (u"ࠬ࠭ᕒ"))
    bstack1llll111lll_opy_ = [self.binary_path]
    self.bstack1lll1llll11_opy_()
    self.bstack1lllll11lll_opy_ = self.bstack1llll11l1ll_opy_(bstack1llll111lll_opy_ + command_args, env)
    self.logger.debug(bstack11llll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᕓ"))
    bstack1llll11llll_opy_ = 0
    while self.bstack1lllll11lll_opy_.poll() == None:
      bstack1llll1ll1ll_opy_ = self.bstack1llll1l1lll_opy_()
      if bstack1llll1ll1ll_opy_:
        self.logger.debug(bstack11llll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᕔ"))
        self.bstack1lllll1l111_opy_ = True
        return True
      bstack1llll11llll_opy_ += 1
      self.logger.debug(bstack11llll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᕕ").format(bstack1llll11llll_opy_))
      time.sleep(2)
    self.logger.error(bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᕖ").format(bstack1llll11llll_opy_))
    self.bstack1llll1ll11l_opy_ = True
    return False
  def bstack1llll1l1lll_opy_(self, bstack1llll11llll_opy_ = 0):
    try:
      if bstack1llll11llll_opy_ > 10:
        return False
      bstack1lllll11ll1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᕗ"), bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᕘ"))
      bstack1llll11ll1l_opy_ = bstack1lllll11ll1_opy_ + bstack111ll11l1l_opy_
      response = requests.get(bstack1llll11ll1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1llll111l11_opy_(self):
    bstack1lll1lll1l1_opy_ = bstack11llll_opy_ (u"ࠬࡧࡰࡱࠩᕙ") if self.bstack11lllll11_opy_ else bstack11llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᕚ")
    bstack11111ll11l_opy_ = bstack11llll_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠨᕛ").format(self.config[bstack11llll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᕜ")], bstack1lll1lll1l1_opy_)
    uri = bstack1l1l11l1ll_opy_(bstack11111ll11l_opy_)
    try:
      response = bstack11lll111l_opy_(bstack11llll_opy_ (u"ࠩࡊࡉ࡙࠭ᕝ"), uri, {}, {bstack11llll_opy_ (u"ࠪࡥࡺࡺࡨࠨᕞ"): (self.config[bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᕟ")], self.config[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᕠ")])})
      if response.status_code == 200:
        bstack1llll1l11ll_opy_ = response.json()
        if bstack11llll_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᕡ") in bstack1llll1l11ll_opy_:
          return bstack1llll1l11ll_opy_[bstack11llll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᕢ")]
        else:
          raise bstack11llll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᕣ").format(bstack1llll1l11ll_opy_)
      else:
        raise bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᕤ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᕥ").format(e))
  def bstack1llll1llll1_opy_(self):
    bstack1llll1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᕦ"))
    try:
      if bstack11llll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕧ") not in self.bstack1llll1lllll_opy_:
        self.bstack1llll1lllll_opy_[bstack11llll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᕨ")] = 2
      with open(bstack1llll1l1l11_opy_, bstack11llll_opy_ (u"ࠧࡸࠩᕩ")) as fp:
        json.dump(self.bstack1llll1lllll_opy_, fp)
      return bstack1llll1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕪ").format(e))
  def bstack1llll11l1ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1l1l1l_opy_ == bstack11llll_opy_ (u"ࠩࡺ࡭ࡳ࠭ᕫ"):
        bstack1lllll1ll11_opy_ = [bstack11llll_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫᕬ"), bstack11llll_opy_ (u"ࠫ࠴ࡩࠧᕭ")]
        cmd = bstack1lllll1ll11_opy_ + cmd
      cmd = bstack11llll_opy_ (u"ࠬࠦࠧᕮ").join(cmd)
      self.logger.debug(bstack11llll_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᕯ").format(cmd))
      with open(self.bstack1llll11l11l_opy_, bstack11llll_opy_ (u"ࠢࡢࠤᕰ")) as bstack1lllll1l1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lllll1l1l1_opy_, text=True, stderr=bstack1lllll1l1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll1ll11l_opy_ = True
      self.logger.error(bstack11llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᕱ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lllll1l111_opy_:
        self.logger.info(bstack11llll_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᕲ"))
        cmd = [self.binary_path, bstack11llll_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᕳ")]
        self.bstack1llll11l1ll_opy_(cmd)
        self.bstack1lllll1l111_opy_ = False
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᕴ").format(cmd, e))
  def bstack1l11llll1l_opy_(self):
    if not self.bstack1l1ll1l111_opy_:
      return
    try:
      bstack1lllll1l1ll_opy_ = 0
      while not self.bstack1lllll1l111_opy_ and bstack1lllll1l1ll_opy_ < self.bstack1llll1lll11_opy_:
        if self.bstack1llll1ll11l_opy_:
          self.logger.info(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᕵ"))
          return
        time.sleep(1)
        bstack1lllll1l1ll_opy_ += 1
      os.environ[bstack11llll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᕶ")] = str(self.bstack1llll11lll1_opy_())
      self.logger.info(bstack11llll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᕷ"))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᕸ").format(e))
  def bstack1llll11lll1_opy_(self):
    if self.bstack11lllll11_opy_:
      return
    try:
      bstack1llll111111_opy_ = [platform[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᕹ")].lower() for platform in self.config.get(bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕺ"), [])]
      bstack1llll1111ll_opy_ = sys.maxsize
      bstack1llll1l1111_opy_ = bstack11llll_opy_ (u"ࠫࠬᕻ")
      for browser in bstack1llll111111_opy_:
        if browser in self.bstack1lllll11l1l_opy_:
          bstack1llll11111l_opy_ = self.bstack1lllll11l1l_opy_[browser]
        if bstack1llll11111l_opy_ < bstack1llll1111ll_opy_:
          bstack1llll1111ll_opy_ = bstack1llll11111l_opy_
          bstack1llll1l1111_opy_ = browser
      return bstack1llll1l1111_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᕼ").format(e))