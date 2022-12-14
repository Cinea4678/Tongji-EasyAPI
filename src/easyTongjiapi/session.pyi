"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import threading
import requests

from typing import Optional

try:
    from . import models
except ImportError and ModuleNotFoundError:
    import models

class Session:

    class keepAliveThread(threading.Thread):
        session: requests.Session = ...
        waitTime: int = ...
        needDestroy: threading.Event = ...
        id: int = ...
        def __init__(self:Session.keepAliveThread, fatherName: str, waitTime: int, session:requests.Session, needDestroy: threading.Event)->None:
            ...
        def run(self:Session.keepAliveThread)->None: ...

    id: int = ...
    islogin: bool = ...
    studentID: str = ...
    token: str|None = ...
    uid: str|None = ...
    session: requests.Session = ...
    sessionID: str|None = ...
    studentData: models.Student = ...
    loginTime: float = ...
    keepAlive: Session.keepAliveThread = ...
    keepaliveDestroy: threading.Event = ...

    def __init__(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,manual:bool|None=...,proxy:str|None=...)->bool:
        ...
    
    def testConnection(self:Session,url:str|None=...)->bool: ...

    def login(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,cookie:str|None=...,manual:bool|None=...)->str: ...

    def logout(self:Session) -> bool: ...

    def request(self:Session,method:str,url:str,data:bytes|str|None=...,json:dict|list|None=...,params:dict|None=...)->requests.Response:...

    def getSchoolCalender(self:Session) -> Optional[dict]:...

    def getHolidayByYear(self:Session, year:int|None=...) -> Optional[dict] :...

    def getScore(self:Session) -> Optional[models.Scores]:...

    def getRounds(self:Session) -> Optional[tuple]:...