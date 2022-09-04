"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import threading
import requests

try:
    from . import models
except ImportError and ModuleNotFoundError:
    import models

class Session:  
    def __init__(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,proxy:str|None=...)->bool:
        self.keepAlive:Session.keepAliveThread = None
        self.studentID:str = None
        self.islogin:bool = None
        self.id:int = None
        self.studentData:models.Student = None
        self.session:requests.Session = None
        self.keepaliveDestroy:threading.Event = None
        ...
    
    def testConnection(self:Session,url:str|None=...)->bool: ...

    def login(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,cookie:str|None=...,manual:bool|None=...)->str: ...

    def request(self:Session,method:str,url:str,data:bytes|str|None=...,json:dict|list|None=...,params:dict|None=...)->requests.Response:...

    class keepAliveThread(threading.Thread):
        def __init__(self:Session.keepAliveThread, fatherName: str, waitTime: int, session:requests.Session, needDestroy: threading.Event)->None:
            self.session:requests.Session = None
            self.waitTime:int = None
            self.needDestroy:threading.Event = None
            self.id:int = None
            ...
        def run(self:Session.keepAliveThread)->None: ...