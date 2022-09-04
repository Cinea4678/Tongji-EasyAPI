"""
  Project Tongji-EasyAPI
  verifyTools.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import requests

def genUUID() -> str: ...

def updateSM2PublicKey(session:requests.Session) -> dict: ...

def getSM2js()->str: ...

def captchaBreaker(session: requests.Session, online: bool = False)-> tuple[bool,str]:...

def aesEncrypt(data: str, key: str) -> str:...

