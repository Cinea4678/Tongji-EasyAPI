"""
  Project Tongji-EasyAPI
  session.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import verifyTools,networkTools
import re,asyncio,time
import requests

#ids.tongji.edu.cn的SM2算法公钥
IDSSM2PublicKey = ""

#SM2.js文件内容
sm2jsFile = ""

class TJU_Session:
    """
    同济大学教务系统的连接会话。
    """
    def __init__(self,studentID=None,studentPassword=None,proxy=None):
        """
        初始化连接会话，*您可以选择立即登录至一系统，也可以在创建会话后登录。*
        @param studentID: 若现在登录，则为登录学生的**学号**。
        @param studentPassword: 若现在登录，则为登录学生的**密码**。
        @param proxy: 若需使用HTTP代理，请在此填入代理地址。
        @return: 默认返回真，若现在登录至一系统，则为登录的成功与否。
        """
        self.login = False
        self.cookies = ""
        self.studentID = None
        self.studentPassword = None
        if proxy:
            if not re.match("^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$",proxy):
                raise ValueError("代理地址格式错误，必须匹配^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$")
        self.proxy = proxy

        #初始化：获取公钥和SM2.js
        async def initMetaFiles():
            if IDSSM2PublicKey == "":
                IDSSM2PublicKey=verifyTools.updateSM2PublicKey()
            if sm2jsFile=="":
                sm2jsFile=verifyTools.getSM2js()
        initMetaFiles()

        #登录
        if studentID or studentPassword:
            pass
    
    def testConnection(self,url=None):
        """
        测试连接会话是否已经成功建立。
        @params url: 你可以自定义测试连接时所前往连接的Url（请求方式为get，敬请注意）
        @return: 连接成功与否
        """
        if not self.login:
            return False  #此处为假会导致绝大多数功能异常，不能允许用户测试
        if not self.studentID:
            return False
        if not url:
            url = f"https://1.tongji.edu.cn/api/studentservice/studentDetailInfo/getStatusInfoByStudentId?studentId={self.studentID}&_t={int(time.time()*1000)}"
        
        #开始测试连接
        try:
            response = requests.get(url,headers=networkTools.headers,cookies=self.cookies)
            if response.status_code==200:
                return True
            else:
                return False
        except Exception as e:
            raise e
    
    def login(self,studentID=None,studentPassword=None,cookie=None):
        """
        登录至一系统。
        **自动登录**：传入学号与密码即可。studentID: 学号; studentPassword: 密码
        **手动登录**：传入cookie与studentID即可。**请注意：学号是不可省略的。**
        @return: 函数会返回cookie，但是会话对象会自动登录，你无需额外操作。
        """
        
        #参数完整性检查
        if cookie:
            #优先使用cookie
    




