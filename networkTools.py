'''
  You Should NOT Import This File, Which Is For Internal Use. 
  -------------------------------------
  Project Tongji-EasyAPI
  networkTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
'''

_idsheaders = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "content-type":"application/x-www-form-urlencoded",
    "origin":"https://ids.tongji.edu.cn:8443",
    "referer":"https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F%2F1.tongji.edu.cn",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

@property
def idsheaders()->dict[str:str]:
    return _idsheaders

_headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "content-type":"application/x-www-form-urlencoded",
    "origin":"https://1.tongji.edu.cn",
    "referer":"https://1.tongji.edu.cn/workbench",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

@property
def headers()->dict[str:str]:
    return _headers

