"""
  Project Tongji-EasyAPI
  session.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from email import header
import verifyTools,networkTools
import re,asyncio,time,os
import requests
from urllib.parse import urlencode
import execjs

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
        @param studentPassword: 若现在登录，则为登录学生的**密码**（推荐密码使用str）。
        @param proxy: 若需使用HTTP代理，请在此填入代理地址。
        @return: 默认返回真，若现在登录至一系统，则为登录的成功与否。
        """
        self.iflogin = False
        self.cookies = ""
        self.studentID = None
        self.studentPassword = None
        if proxy:
            if not re.match("^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$",proxy):
                raise ValueError("代理地址格式错误，必须匹配^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$")
        self.proxy = proxy

        #初始化：获取公钥和SM2.js
        def initMetaFiles():
            global IDSSM2PublicKey,sm2jsFile
            if IDSSM2PublicKey == "":
                IDSSM2PublicKey=verifyTools.updateSM2PublicKey()
            if sm2jsFile=="":
                sm2jsFile=verifyTools.getSM2js()
        initMetaFiles()

        #登录
        if studentID or studentPassword:
            self.login(studentID,studentPassword)
    
    def testConnection(self,url=None):
        """
        测试连接会话是否已经成功建立。
        @params url: 你可以自定义测试连接时所前往连接的Url（请求方式为get，敬请注意）
        @return: 连接成功与否
        """
        if not self.iflogin:
            return False  #此处为假会导致绝大多数功能异常，不能允许用户测试
        if not self.studentID:
            return False
        if not url:
            url = f"https://1.tongji.edu.cn/api/studentservice/studentDetailInfo/getStatusInfoByStudentId?studentId={self.studentID}&_t={networkTools.ts()}"
        
        #开始测试连接
        try:
            response = requests.get(url,headers=networkTools.headers(),cookies=self.cookies)
            if response.status_code==200:
                return True
            else:
                return False
        except Exception as e:
            raise e
    
    def login(self,studentID=None,studentPassword=None,cookie=None):
        """
        登录至一系统。
        **自动登录**：传入学号与密码即可。studentID: 学号; studentPassword: 密码（推荐密码使用str）
        **手动登录**：传入cookie与studentID即可。**请注意：学号是不可省略的。**
        @return: 函数会返回cookie，但是会话对象会自动登录，你无需额外操作。
        """
        
        #参数完整性检查
        if cookie:
            #优先使用cookie
            if not studentID:
                raise ValueError("未提供studentID")
        else:
            if not studentID or not studentPassword:
                raise ValueError("未完整提供studentID与studentPassword")

        #学号与密码效验
        if isinstance(studentID,int):
            studentID = int(studentID)
        if isinstance(studentPassword,int):
            studentPassword = "%06d" % studentPassword  #补齐零
        if not re.match("^[1|2|3|4][0-9]{6}$",studentID):
            raise ValueError("学号格式错误，必须匹配^[1|2|3|4][0-9]{6}$。")
        if not re.match("^[0-9]{6}$",studentPassword):
            raise ValueError("密码格式错误，必须匹配^[0-9]{6}$。")
        
        #加密密码
        #【开发者注释】此处未能逆向或找到替代模块代替SM2Encrypt，长期有偿(50-100r)招募专家逆向SM2
        old_execjsrt = ""
        if "EXECJS_RUNTIME" in os.environ:
            old_execjsrt = os.environ["EXECJS_RUNTIME"]
        os.environ["EXECJS_RUNTIME"] = "PhantomJS"
        javaScript = execjs.compile(sm2jsFile)
        encryptData = javaScript.call('sm2Encrypt',studentPassword,IDSSM2PublicKey)

        print(encryptData)
        os.environ["EXECJS_RUNTIME"] = old_execjsrt
        
        #完成验证码验证
        captchaVerification = verifyTools.captchaBreaker()

        #提交验证，开始登录
        dataToSend = {
            "option":"credential",
            "Ecom_Captche":captchaVerification,
            "Ecom_User_ID":studentID,
            "Ecom_Password":encryptData
        }
        dataToSend = urlencode(dataToSend)
        newHeader = networkTools.idsheaders()
        newHeader["content-type"]="application/x-www-form-urlencoded"
        loginResp1 = requests.post("https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0",data=dataToSend,headers=newHeader)
        cookie1 = loginResp1.cookies
        urls = re.findall(r"^window\.location\.href=\'.*\'$",loginResp1.text)
        if len(urls)>0:
            href = urls[0]
        else:
            raise SystemError("登录失败，请检查学号，密码是否正确！")
        loginResp2 = requests.get(href,headers=networkTools.idsheaders(),cookies=cookie1)
        print(loginResp2.cookies.get_dict())
        print(loginResp2.status_code)

#tjus = TJU_Session("2152955","831033")

sm2jsFile = verifyTools.getSM2js()
IDSSM2PublicKey = "04fa689d8f36b175f519e167a97b5c3d06965f2ca1a28f9e45ce63af29ddb6913814ce76d1edb44f83034e63f0e0a4e365f443f0eaa0d4278e367744461de0d467"
old_execjsrt = ""
if "EXECJS_RUNTIME" in os.environ:
    old_execjsrt = os.environ["EXECJS_RUNTIME"]
os.environ["EXECJS_RUNTIME"] = "PhantomJS"
javaScript = execjs.compile(sm2jsFile)
encryptData = javaScript.call('sm2Encrypt',"831033",IDSSM2PublicKey,0)
print(encryptData)

        

    




