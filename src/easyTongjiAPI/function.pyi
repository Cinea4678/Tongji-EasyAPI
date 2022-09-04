"""
  Project Tongji-EasyAPI
  function.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from . import models
from typing import Optional

def sessionIdToUserData(sessionId:str|None = ...,cookie:str|dict|None = ..., **kw) -> Optional[models.Student]: ...

def sessionLogout(sessionId:str|None = ...,cookie:str|dict|None = ..., **kw)->bool:...

def getSchoolCalender(sessionId:str|None = ...,cookie:str|dict|None = ..., **kw) -> Optional[dict]:...

def getHolidayByYear(sessionId:str|None = ...,cookie:str|dict|None = ...,year:int|None=...,**kw) -> Optional[dict]:...

def getScore(sessionId:str|None = ...,cookie:str|dict|None = ..., **kw)->Optional[models.Scores]:...



