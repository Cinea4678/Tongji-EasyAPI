"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from typing import Any
from requests import Response

class Session:  
    def __init__(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,proxy:str|None=...)->bool: ...
    
    def testConnection(self:Session,url:str|None=...)->bool: ...

    def login(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,cookie:str|None=...,manual:bool|None=...)->str: ...

    def request(self:Session,method:str,url:str,data:bytes|str|None=...,json:dict|list|None=...,params:dict|None=...)->Response:...
    