"""
  Project Tongji-EasyAPI
  verifyTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import json,base64
from typing import Any
import networkTools
import math,time
from random import random
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import Crypto.Util.Padding as Padding

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
        html = requests.get("https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F%2F1.tongji.edu.cn",headers=networkTools.idsheaders()).text
        soup = BeautifulSoup(html,"lxml")
        secretId = soup.find(id="secretId")["value"]
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

BaseUrl = "https://ids.tongji.edu.cn:8443/nidp/app/login?sid=0&sid=0"

def aesEncrypt(data:str,key:str)->str:
    """
    内部函数。调用时，key的有效性自理。
    """
    BLOCK_SIZE = 16  # 补齐位数
    key = key.encode("utf-8")
    data = Padding.pad(data.encode("utf-8"),16)
    aes = AES.new(key,AES.MODE_ECB)
    result = aes.encrypt(data)
    result = base64.b64encode(result)
    result = result.decode("utf-8")
    return result

def captchaBreaker()->str:
    """
    开发者说明：
    限于个人水平，目前使用了某云平台的打码服务（惭愧）
    计划是既准备本地浏览器用户点选，又使用云平台，在云平台欠费时使用本地点选
    未来仍需要本地打码：有偿(300-500r)招募计算机视觉、人工智能领域专家参与编写本地打码
    """

    newHeader = networkTools.idsheaders()
    newHeader["content-type"]="application/json;charset=UTF-8"

    #阶段一：获取图片验证码
    def getcaptchaOnce(uuid:str):
        res = requests.post(BaseUrl+"/getCaptcha=1", json= {"captchaType":"clickWord", "clientUid": uuid, "ts": networkTools.ts()},headers=newHeader).text
        try:
            res = json.loads(res)
        except:
            raise SystemError("1系统拒绝了我们的请求。")
        if res["repCode"]=="0000":
            image = res["repData"]["originalImageBase64"]
            secretKey = res["repData"]["secretKey"]
            token = res["repData"]["token"]
            wordList = res["repData"]["wordList"]
            return {"image":image,"secretKey":secretKey,"token":token,"wordList":wordList}
        else:
            raise SystemError("1系统拒绝了我们的请求："+res["repMsg"])

    #阶段三：验证图片验证码
    def verifycaptcha(pointData:list[int],captchaMeta:dict,uuid:str) -> bool:
        res = requests.post(BaseUrl+"/checkCaptcha=1",json={
                "captchaType": "clickWord",
                "clientUid": uuid,
                "pointJson": aesEncrypt(json.dumps(pointData).replace(' ',''),captchaMeta["secretKey"]) if captchaMeta["secretKey"] else json.dumps(pointData),
                "token": captchaMeta["token"],
                "ts":networkTools.ts()
            },headers=newHeader)
        try:
            vRes = json.loads(res.text)
        except:
            raise SystemError("1系统拒绝了我们的请求。")
        if vRes["repCode"]=="0000":
            return True  #已通过验证，无需处理返回内容
        else:
            return False

    #阶段二：提交打码平台打码
    #为便于日后维护，将由作者的服务器代理代码请求
    success = False
    for _ in range(30):
        uuid = "point-"+genUUID()
        captchaMeta = getcaptchaOnce(uuid)
        try:
            res = requests.get("https://www.cinea.com.cn/api/sqp/captchaBroke",json={
                "imageBase64":captchaMeta["image"],
                "wordList":captchaMeta["wordList"]
            })
            if res.status_code!=200:
                pass
            else:
                resData = json.loads(res.text)
                if resData["success"]:
                    pointList = []
                    for word in captchaMeta["wordList"]:
                        pointList.append({"x":resData["dataList"][word][0],"y":resData["dataList"][word][1]})
                    if verifycaptcha(pointList,captchaMeta,uuid):
                        success = True
                        break
                    else:
                        requests.get(f'https://www.cinea.com.cn/api/sqp/reportWrongCaptcha?picId={resData["picId"]}')
        except:
            pass
    if not success:
        raise SystemError("很抱歉，验证码识别失败！在失败前已重试30次。")
    
    #阶段四：制作验证码密钥
    captchaVerification = aesEncrypt(captchaMeta["token"]+'---'+json.dumps(pointList),captchaMeta["secretKey"]) if captchaMeta["secretKey"] else captchaMeta["token"]+'---'+json.dumps(pointList)
    
    return captchaVerification