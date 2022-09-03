'''
  Hey,don't import me! I am for internal use. 

  API功能的具体实现
  -------------------------------------
  Project Tongji-EasyAPI
  models.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
'''

try:
    from . import models,networkTools
except:
    import models,networkTools
import json,requests,time

"""
PART.0  解析参数、相关内部工具

"""

def _processArgs(sessionId,cookie) -> tuple:
    if cookie:
        if isinstance(cookie,str):
            cookie = networkTools.parseStrCookie(cookie)
        try:
            sessionId = cookie["sessionid"]
        except:
            raise ValueError("传入的cookie有误")
    elif sessionId:
        cookie = {"sessionid":sessionId,"language":"cn"}
    else:
        raise ValueError("请至少提供一项参数")
    return sessionId,cookie


"""
PART.1  登录、会话、状态类

注释：login仅在Session类中提供
"""

def sessionIdToUserData(sessionId = None,cookie = None, **kw) -> models.Student:
    """
    通过已知的sessionId或cookie反查学生信息
    @params: 在sessionId与cookie中任选一项传入即可。
    @return: 返回Student对象。若sessionId无效，则返回None
    """

    if "session" not in kw:
        sessionId = _processArgs(sessionId,cookie)
        cookie=sessionId[1]
        sessionId = sessionId[0]

        res = requests.get(f"https://1.tongji.edu.cn/api/sessionservice/session/getSessionUser?_t={networkTools.ts()}",headers=networkTools.headers(),cookies=cookie)
    else:
        session:requests.Session = kw['session']
        res = session.get(f"https://1.tongji.edu.cn/api/sessionservice/session/getSessionUser?_t={networkTools.ts()}")
    
    try:
        res =  res.json()
        assert res["code"]==200
        res = res["data"]
        return models.Student(res["user"]["name"],res["uid"],res["user"]["sex"],res["user"]["faculty"],res["user"]["facultyName"],res["user"]["grade"])
    except:
        return None

def sessionLogout(sessionId = None,cookie = None, **kw)->bool:
    """
    注销sessionID的登录状态。如果您正在使用SessionID类，则您并不需要调用本函数。
    @params: 在sessionId与cookie中任选一项传入即可。
    @return: 返回是否成功
    """
    
    if "session" not in kw:
        sessionId = _processArgs(sessionId,cookie)
        cookie=sessionId[1]
        sessionId = sessionId[0]

        uid = sessionIdToUserData(cookies=cookie).studentId
        res = requests.post("https://1.tongji.edu.cn/api/sessionservice/session/logout",json={
            "sessionid":sessionId,
            "uid":uid
        },headers=networkTools.headers(),cookies=cookie)
    else:
        session:requests.Session = kw['session']
        uid:str = kw['uid']
        res = session.post("https://1.tongji.edu.cn/api/sessionservice/session/logout",json={
            "sessionid":sessionId,
            "uid":uid
        })

    try:
        res = res.json()
        assert res["code"]==200
        return True
    except:
        return False

"""
PART.2  各种信息类
"""

def getSchoolCalender(sessionId=None,cookie=None,**kw) -> dict:
    """
    获取当前学期的校历。返回数据格式参考文档
    @params: 在sessionId与cookie中任选一项传入即可。
    @return: 字典格式的查询结果。若失败，则返回None。
    """
    if "session" not in kw:
        sessionId = _processArgs(sessionId,cookie)[1]
        res = requests.get(f"https://1.tongji.edu.cn/api/baseresservice/schoolCalendar/currentTermCalendar?_t={networkTools.ts()}",cookies=cookie,headers=networkTools.headers())
    else:
        session:requests.Session = kw["session"]
        res = session.get(f"https://1.tongji.edu.cn/api/baseresservice/schoolCalendar/currentTermCalendar?_t={networkTools.ts()}")
    
    try:
        res=res.json()
        assert res["code"]==200
        return res["data"]
    except:
        return None

def getHolidayByYear(sessionId=None,cookie=None,year=time.localtime(time.time()).tm_year,**kw) -> dict:
    """
    获取指定年份的假期安排。返回数据格式参考文档
    @params: 在sessionId与cookie中任选一项传入即可。year不填则为本年。
    @return: 字典格式的查询结果。若失败，则返回None。
    """
    if "session" not in kw:
        cookie = _processArgs(sessionId,cookie)[1]
        res = requests.get(f"https://1.tongji.edu.cn/api/baseresservice/holiday/queryHolidayByYear?year={year}&_t={networkTools.ts()}",cookies=cookie,headers=networkTools.headers())
    else:
        session:requests.Session=kw['session']
        res = session.get(f"https://1.tongji.edu.cn/api/baseresservice/holiday/queryHolidayByYear?year={year}&_t={networkTools.ts()}")
    
    try:
        res=res.json()
        assert res["code"]==200
        return res["data"]
    except:
        return None



if __name__=="__main__":
    me = sessionIdToUserData(sessionId="61ab6104395c478b9dcadc66b94f4108")