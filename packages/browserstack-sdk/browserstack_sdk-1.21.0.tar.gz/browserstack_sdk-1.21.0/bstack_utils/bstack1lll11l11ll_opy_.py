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
bstack1lll111l11l_opy_ = 1000
bstack1lll11l1111_opy_ = 5
bstack1lll111ll11_opy_ = 30
bstack1lll111lll1_opy_ = 2
class bstack1lll11l1l11_opy_:
    def __init__(self, handler, bstack1lll111l1l1_opy_=bstack1lll111l11l_opy_, bstack1lll11l11l1_opy_=bstack1lll11l1111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll111l1l1_opy_ = bstack1lll111l1l1_opy_
        self.bstack1lll11l11l1_opy_ = bstack1lll11l11l1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lll111l1ll_opy_()
    def bstack1lll111l1ll_opy_(self):
        self.timer = threading.Timer(self.bstack1lll11l11l1_opy_, self.bstack1lll111ll1l_opy_)
        self.timer.start()
    def bstack1lll11l111l_opy_(self):
        self.timer.cancel()
    def bstack1lll111llll_opy_(self):
        self.bstack1lll11l111l_opy_()
        self.bstack1lll111l1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll111l1l1_opy_:
                t = threading.Thread(target=self.bstack1lll111ll1l_opy_)
                t.start()
                self.bstack1lll111llll_opy_()
    def bstack1lll111ll1l_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lll111l1l1_opy_]
        del self.queue[:self.bstack1lll111l1l1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lll11l111l_opy_()
        while len(self.queue) > 0:
            self.bstack1lll111ll1l_opy_()