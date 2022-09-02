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
import json,requests


def sessionIdToUserData(sessionId = None,cookies = None) -> models.Student:
    """
    通过已知的sessionId或cookie反查学生信息
    @params: 在sessionId与cookie中任选一项传入即可。
    @return: 返回Student对象。若sessionId无效，则返回None
    """

    if not sessionId and not cookies:
        raise ValueError("请至少提供一项参数")
    if not cookies:
        cookies = {"sessionid":sessionId,"language":"cn"}
    
    try:
        res = requests.get(f"https://1.tongji.edu.cn/api/sessionservice/session/getSessionUser?_t={networkTools.ts()}",headers=networkTools.headers(),cookies=cookies)
    except Exception as e:
        raise SystemError("网络错误，原异常："+str(e))
    try:
        res= json.loads(res)
    except:
        raise SystemError("1系统返回了异常的信息")
    if "data" not in res or "code" not in res or res["code"]!=200:
        return None
    else:
        res = res["data"]
        return models.Student(res["user"]["name"],res["uid"],res["user"]["sex"],res["user"]["faculty"],res["user"]["facultyName"],res["user"]["grade"])
