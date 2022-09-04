"""
  Project Tongji-EasyAPI
  verifyTools.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

def genUUID() -> str: ...

def updateSM2PublicKey() -> dict: ...

def getSM2js()->str: ...

def captchaBreaker(LoginCookie)->str:...