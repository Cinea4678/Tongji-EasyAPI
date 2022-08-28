"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from __init__ import headers

class TJU_Session:  
    def __init__(self:TJU_Session,studentID:str|int=None,studentPassword:str|int=None,proxy:str=None)->bool:
        pass
    
    def login(self:TJU_Session,studentID:str|int=None,studentPassword:str|int=None,cookie:str=None)->str:
        pass