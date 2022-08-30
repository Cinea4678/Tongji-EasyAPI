'''
  You Should NOT Import This File, Which Is For Internal Use. 
  -------------------------------------
  Project Tongji-EasyAPI
  networkTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
'''

import time,math
from random import random

def _genUUID():
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

_idsheaders = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "Authorization": "Basic MjE1Mjk1NTo4MzEwMzM=",
    "origin":"https://ids.tongji.edu.cn:8443",
    "referer":"https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F%2Fids.tongji.edu.cn%3A8443%2Fnidp%2Foauth%2Fnam%2Fauthz%3Fscope%3Dprofile%26response_type%3Dcode%26redirect_uri%3Dhttps%3A%2F%2F1.tongji.edu.cn%2Fapi%2Fssoservice%2Fsystem%2FloginIn%26client_id%3D5fcfb123-b94d-4f76-89b8-475f33efa194",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def idsheaders()->dict[str:str]:
    return _idsheaders

_headers = {
    "accept":"application/json, text/plain, */*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "content-type":"application/json",
    "origin":"https://1.tongji.edu.cn",
    "referer":"https://1.tongji.edu.cn/workbench",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def headers()->dict[str:str]:
    return _headers

def ts()->int:
    '''Time stamp of JavaScript'''
    return int(time.time()*1000)
