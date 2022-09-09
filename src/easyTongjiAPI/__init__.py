"""
  易用的一系统API。requests？F12找cookie？抱歉，忘了他们吧！

  ------------------------------------------------

  使用范例/快速上手：

  >>>  s = easyTongjiapi.Session()
  >>>  s.login(2152xxx,831xxx)
  >>>  print(s.sessionID)
  >>>  s.getScore()
  >>>  s.getScore().gradePoint
  -------------------------------------------------
  Project Tongji-EasyAPI
  __init__.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from .__version__ import __65472__  # 大误
from .__version__ import __author__, __author_email__, __copyright__
from .__version__ import __title__, __description__, __url__
from .__version__ import __build__, __version__

from .session import Session
from .models import Student, Scores
from .function import *
