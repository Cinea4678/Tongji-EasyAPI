"""
  Project Tongji-EasyAPI
  session.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

try:
    from . import verifyTools,networkTools,crack,models
except:
    import verifyTools,networkTools,crack,models
import re,asyncio,time,os,json
import requests
import urllib.parse as urlparse
import execjs

#ids.tongji.edu.cn的SM2算法公钥
IDSSM2PublicKey = ""

#SM2.js文件内容
sm2jsFile = ""

class Session():
    """
    同济大学教务系统的连接会话。
    """
    def __init__(self,studentID=None,studentPassword=None,manual=False,proxy=None):
        """
        初始化连接会话，*您可以选择立即登录至一系统，也可以在创建会话后登录。*
        @param studentID: 若现在登录，则为登录学生的**学号**。
        @param studentPassword: 若现在登录，则为登录学生的**密码**（推荐密码使用str）。
        @param manual: 是否手动输入验证码。若自动输入不成功，请尝试使用手动输入。
        @param proxy: 若需使用HTTP代理，请在此填入代理地址。
        @return: 构造函数无返回值
        """
        self._iflogin = False
        self._studentID = None
        self._studentPassword = None
        self._token = None
        self._uid = None
        self._sessionID = None
        self._session = requests.session()
        self._studentData = models.Student(name="对象创建成功")

        self._loginTime = 0
        

        if proxy:
            if not re.match(r"^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$",proxy):
                raise ValueError("代理地址格式错误，必须匹配^(https?|socks5?)://([^:]*(:[^@]*)?@)?([^:]+|\[[:0-9a-fA-F]+\])(:\d+)?/?$|^$")
            proxy = re.findall("(https?|socks5?)://(.*)")
            try:
                self._session.proxies = {proxy[0]:proxy[1]}
            except:
                raise ValueError("代理地址不能被程序解析")

        #初始化：获取SM2.js
        def initMetaFiles():
            global sm2jsFile
            if sm2jsFile=="":
                sm2jsFile=verifyTools.getSM2js()
        initMetaFiles()

        #登录
        if studentID or studentPassword:
            self.login(studentID,studentPassword,manual=manual)

    def testConnection(self,url=None):
        """
        测试连接会话是否已经成功建立。
        @params url: 你可以自定义测试连接时所前往连接的Url（请求方式为get，敬请注意）
        @return: 连接成功与否
        """
        if not self._iflogin:
            return False  #此处为假会导致绝大多数功能异常，不能允许用户测试
        if not self._studentID:
            return False
        if not url:
            url = f"https://1.tongji.edu.cn/api/studentservice/studentDetailInfo/getStatusInfoByStudentId?studentId={self._studentID}&_t={networkTools.ts()}"

        #开始测试连接
        try:
            response = self._session.get(url)
            if response.status_code!=200:
                return False
            res = json.loads(response.text)
            if "code" not in res or res["code"]!=200:
                return False
            else:
                return True
        except json.JSONDecodeError:
            return False
        except Exception as e:
            raise e

    def login(self,studentID=None,studentPassword=None,cookie=None,manual=False):
        """
        登录至一系统。
        **学号密码登录**：传入学号与密码即可。studentID: 学号; studentPassword: 密码。
        @params manual:  参数manual用来确认使用自动通过验证码或手动通过验证码。如果您不能成功使用自动模式，请使用手动模式。手动模式仍然存在bug。
        **学号cookie登录**：传入cookie与studentID即可。**请注意：学号是不可省略的。**
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
        
        #使用cookie登录
        if cookie:
            if isinstance(studentID,int):
                studentID = str(studentID)
            if not re.match("^[1|2|3|4][0-9]{6}$",studentID):
                raise ValueError("学号格式错误，必须匹配^[1|2|3|4][0-9]{6}$。")
            self._session.cookies = cookie
            self._session.headers = networkTools.headers()
            self.studentID=studentID
            if self.testConnection():
                return cookie
            else:
                raise ValueError("您提供的cookie不能正确使用！")

        #学号与密码效验
        if isinstance(studentID,int):
            studentID = str(studentID)
        if isinstance(studentPassword,int):
            studentPassword = "%06d" % studentPassword  #补齐零
        if not re.match("^[1|2|3|4][0-9]{6}$",studentID):
            raise ValueError("学号格式错误，必须匹配^[1|2|3|4][0-9]{6}$。")
        if not re.match("^[0-9]{6}$",studentPassword):
            raise ValueError("密码格式错误，必须匹配^[0-9]{6}$。")

        #初始化Session
        self._session.headers = networkTools.idsheaders()

        #加密密码
        #【开发者注释】此处未能逆向或找到替代模块代替SM2Encrypt，长期有偿(50-100r)招募专家逆向SM2
        IDSSM2PublicKey = verifyTools.updateSM2PublicKey(self._session)
        old_execjsrt = ""
        if "EXECJS_RUNTIME" in os.environ:
            old_execjsrt = os.environ["EXECJS_RUNTIME"]
        os.environ["EXECJS_RUNTIME"] = "PhantomJS"
        javaScript = execjs.compile(sm2jsFile)
        encryptData = javaScript.call('sm2Encrypt',studentPassword,IDSSM2PublicKey,0)
        os.environ["EXECJS_RUNTIME"] = old_execjsrt
        # encryptData = "04"+networkTools.sm2Encrypt(studentPassword,IDSSM2PublicKey)

        #完成验证码验证
        if manual:
            #手动完成验证
            captchaRes = verifyTools.captchaBreaker(self._session,False)
            if not captchaRes[0]:
                return {"message":"Operation aborted."}
            captchaVerification = captchaRes[1]

        for _ in range(1 if manual else 10):

            if not manual:
                #自动验证
                captchaVerification = crack.getCode()

            #提交验证，开始登录
            #第一跳：向ids取得访问权限
            dataToSend = {
                "option":"credential",
                "Ecom_Captche":captchaVerification,
                "Ecom_User_ID":studentID,
                "Ecom_Password":encryptData
            }
            dataToSend = urlparse.urlencode(dataToSend)
            self._session.headers["content-type"]="application/x-www-form-urlencoded"
            loginResp1 = self._session.post("https://ids.tongji.edu.cn:8443/nidp/app/login?sid=0&sid=0",data=dataToSend)
            urls = re.findall(r"window\.location\.href=\'(.*?)\'",loginResp1.text)
            if len(urls)>0:
                href = urls[0]
            else:
                raise ValueError("登录失败，请检查学号，密码是否正确！")

            #第二三四跳：由ids前往1系统
            loginResp2 = self._session.get(href,headers=networkTools.idsheaders())

            #第五跳：向1系统取得cookies
            try:
                self._session.headers = networkTools.headers()
                self._session.headers["x-token"] = ""
                tokenForm= urlparse.parse_qs(urlparse.urlparse(loginResp2.url).query)
                self._token = tokenForm["token"][0]
                self._uid = tokenForm["uid"][0]
                FuckTheFakeTS = tokenForm["ts"][0]
                loginResp3 = self._session.post(f"https://1.tongji.edu.cn/api/sessionservice/session/login",data=json.dumps({
                    "uid":self._uid,
                    "token":self._token,
                    "ts":FuckTheFakeTS
                }).replace(' ',''))
            except Exception as e:
                if not manual:
                    continue
                else:
                    raise e   #手动登录是不会出现这种问题滴！

            try:
                loginResult = json.loads(loginResp3.text)
                if "code" not in loginResult or loginResult["code"]!=200:
                    raise SystemError(f"登录失败，1系统返回了不正常的凭据。这通常是由于访问人数过多造成的。频繁出现此错误，则请联系开发者。（notes: json loads succeed but not code 200. The text is '{loginResp3.text}'）")
                loginResult = loginResult["data"]
                self._sessionID = loginResult["sessionid"]
                self._aesIv = loginResult["aesIv"]
                self._aesKey = loginResult["aesKey"]
                self._studentDataSourceObj = loginResult["user"]
                self._studentData = models.Student(studentDataObject=self._studentDataSourceObj)
            except:
                raise SystemError(f"登录失败，1系统返回了不正常的凭据。这通常是由于访问人数过多造成的。频繁出现此错误，则请联系开发者。（notes: json loads failed while text is '{loginResp3.text}'）")

            #测试连接
            self._iflogin = True
            self._studentID = studentID
            self._studentPassword = studentPassword
            if self.testConnection():
                self._loginTime = time.time()
                return self._session.cookies.get_dict()
            else:
                self._iflogin = False
                raise SystemError("登录失败，1系统未正常运行")
        
        if not manual:
            raise SystemError("自动验证失效，这真是不可思议。请使用手动模式通过验证码。")

    def __str__(self) -> str:
        return f"<TJU 1-Session, User:{str(self._studentData)}, Last Login Time:{time.asctime( time.localtime(self._loginTime))}, sessionID:{self._sessionID}>"

    def __repr__(self) -> str:
        return f"<TJU 1-Session, User:{str(self._studentData)}, Last Login Time:{time.asctime( time.localtime(self._loginTime))}, sessionID:{self._sessionID}>"

    """
    以下是参数函数的实现
    """
    @property
    def sessionID(self) -> str:
        return self._sessionID

    @property
    def studentID(self) -> str:
        return self._studentID

if __name__ == "__main__":
    print(Session("2152955","831033"))




