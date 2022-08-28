"""
  Project Tongji-EasyAPI
  verifyTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import networkTools
import math
from random import random
import requests
from bs4 import BeautifulSoup

def genUUID():
    """
    本函数可以生成一个在登录验证中使用的UUID。如果你需要手动写通过验证码的过程，那么你可能会需要它。
    @param: 无需任何参数
    @return: 生成的UUID
    """
    s=[]
    hexDigits = "0123456789abcdef"
    for i in range(36):
        s.append(hexDigits[math.floor(random() * 0x10)])
    s[14]='4'
    s[19]=hexDigits[(int(s[19],base=16)&0x3)|0x8]
    s[8]=s[13]=s[18]=s[23]="-"
    return "".join(s)

def updateSM2PublicKey():
    """
    本函数用于从ids.tongji.edu.cn获取最新的SM2公钥。如果你需要手动写通过验证码的过程，那么你可能会需要它。
    @param: 无需任何参数
    @return: SM2公钥
    """
    try:
        html = requests.get("https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F%2F1.tongji.edu.cn",headers=networkTools.idsheaders).text
        soup = BeautifulSoup(html,"lxml")
        secretId = soup.find("input",id="secretId")["value"]
    except Exception as e:
        raise e
    return secretId

def getSM2js():
    try:
        res =  requests.get("https://www.cinea.com.cn/static/sm2.js")
        if res.status_code==200:
            return res.text
    except:
        pass
    try:
        res = requests.get("https://blogsources-1305284863.file.myqcloud.com/static/sm2.js")
        if res.status_code==200:
            return res.text
    except:
        raise SystemError("无法获取运行必须的文件，请检查你的互联网连接")


    