"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from typing import Any

class TJU_Session:  
    def __init__(self:TJU_Session,studentID:str|int|None=...,studentPassword:str|int|None=...,proxy:str|None=...)->bool: ...
    
    def testConnection(self:TJU_Session,url:str|None=...)->bool: ...

    def login(self:TJU_Session,studentID:str|int|None=...,studentPassword:str|int|None=...,cookie:str|None=...,online:str|None=...)->str: ...