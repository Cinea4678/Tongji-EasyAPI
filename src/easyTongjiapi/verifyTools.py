"""
  Project Tongji-EasyAPI
  verifyTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import base64
import json

try:
    from . import networkTools, offlineCaptcha
except ImportError or ModuleNotFoundError:
    import networkTools
    import offlineCaptcha
import math
from random import random
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import Crypto.Util.Padding as Padding


# noinspection DuplicatedCode,SpellCheckingInspection
def genUUID():
    """
    本函数可以生成一个在登录验证中使用的UUID。如果你需要手动写通过验证码的过程，那么你可能会需要它。
    @return: 生成的UUID
    """
    s = []
    hexDigits = "0123456789abcdef"
    for i in range(36):
        s.append(hexDigits[math.floor(random() * 0x10)])
    s[14] = '4'
    s[19] = hexDigits[(int(s[19], base=16) & 0x3) | 0x8]
    s[8] = s[13] = s[18] = s[23] = "-"
    return "".join(s)


# noinspection SpellCheckingInspection
def updateSM2PublicKey(session: requests.Session = None):
    """
    本函数用于从ids.tongji.edu.cn获取最新的SM2公钥及其对应的cookie。如果你需要手动写通过验证码的过程，那么你可能会需要它。
    @return: 字典。secretId为公钥，cookie为对应的cookie（request.RequestCookieJar格式）。请注意，每个公钥都对应唯一的JSESSIONID。
    """
    if session:
        res = session.get(
            "https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F"
            "%2Fids.tongji.edu.cn%3A8443%2Fnidp%2Foauth%2Fnam%2Fauthz%3Fscope%3Dprofile%26response_type%3Dcode"
            "%26redirect_uri%3Dhttps%3A%2F%2F1.tongji.edu.cn%2Fapi%2Fssoservice%2Fsystem%2FloginIn%26client_id"
            "%3D5fcfb123-b94d-4f76-89b8-475f33efa194",
            headers=networkTools.idsHeaders())
        soup = BeautifulSoup(res.text, "lxml")
        secretId = soup.find(id="secretId")["value"]
    else:
        res = requests.get(
            "https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F"
            "%2Fids.tongji.edu.cn%3A8443%2Fnidp%2Foauth%2Fnam%2Fauthz%3Fscope%3Dprofile%26response_type%3Dcode"
            "%26redirect_uri%3Dhttps%3A%2F%2F1.tongji.edu.cn%2Fapi%2Fssoservice%2Fsystem%2FloginIn%26client_id"
            "%3D5fcfb123-b94d-4f76-89b8-475f33efa194",
            headers=networkTools.idsHeaders())
        soup = BeautifulSoup(res.text, "lxml")
        secretId = soup.find(id="secretId")["value"]
    return {"secretId": secretId, "cookie": res.cookies}


# noinspection PyBroadException
def getSM2js():
    try:
        res = requests.get("https://www.cinea.com.cn/static/sm2.js")
        if res.status_code == 200:
            return res.text
    except:
        pass
    try:
        res = requests.get("https://blogsources-1305284863.file.myqcloud.com/static/sm2.js")
        if res.status_code == 200:
            return res.text
    except:
        raise SystemError("无法获取运行必须的文件，请检查你的互联网连接")


BaseUrl = "https://ids.tongji.edu.cn:8443/nidp/app/login?sid=0&sid=0"


def aesEncrypt(data: str, key: str) -> str:
    """
    内部函数。调用时，key的有效性自理。
    """
    key = key.encode("utf-8")
    data = Padding.pad(data.encode("utf-8"), 16)
    aes = AES.new(key, AES.MODE_ECB)
    result = aes.encrypt(data)
    result = base64.b64encode(result)
    result = result.decode("utf-8")
    return result


def captchaBreaker(session: requests.Session, online: bool = False) -> tuple:
    """
    开发者说明：

    限于个人水平，目前无法完成自动打码
    """

    session.headers["content-type"] = "application/json;charset=UTF-8"
    pointList = []
    captchaMeta = {}

    # 阶段一：获取图片验证码
    def getCaptchaOnce(_uuid: str):
        result = session.post(BaseUrl + "/getCaptcha=1",
                              json={"captchaType": "clickWord", "clientUid": _uuid, "ts": networkTools.ts()}).text
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            raise SystemError("1系统拒绝了我们的请求。")
        if result["repCode"] == "0000":
            image = result["repData"]["originalImageBase64"]
            secretKey = result["repData"]["secretKey"]
            token = result["repData"]["token"]
            wordList = result["repData"]["wordList"]
            return {"image": image, "secretKey": secretKey, "token": token, "wordList": wordList}
        else:
            raise SystemError("1系统拒绝了我们的请求：" + result["repMsg"])

    # 阶段三：验证图片验证码
    def verifyCaptcha(pointData: list, _captchaMeta: dict, _uuid: str) -> bool:
        result = session.post(BaseUrl + "/checkCaptcha=1", json={
            "captchaType": "clickWord",
            "clientUid": _uuid,
            "pointJson": aesEncrypt(json.dumps(pointData).replace(' ', ''), _captchaMeta["secretKey"]) if _captchaMeta[
                "secretKey"] else json.dumps(pointData),
            "token": _captchaMeta["token"],
            "ts": networkTools.ts()
        })
        try:
            vRes = json.loads(result.text)
        except json.JSONDecodeError:
            raise SystemError("1系统拒绝了我们的请求。")
        if vRes["repCode"] == "0000":
            return True  # 已通过验证，无需处理返回内容
        else:
            return False

    # 阶段二：提交打码平台打码
    # 为便于日后维护，将由作者的服务器代理代码请求
    if online:
        # 在线打码
        success = False
        for _ in range(30):
            uuid = "point-" + genUUID()
            captchaMeta = getCaptchaOnce(uuid)
            try:
                res = requests.get("https://www.cinea.com.cn/api/sqp/captchaBroke", json={
                    "imageBase64": captchaMeta["image"],
                    "wordList": captchaMeta["wordList"]
                })
                if res.status_code != 200:
                    pass
                else:
                    resData = json.loads(res.text)
                    if resData["success"]:
                        pointList = []
                        for word in captchaMeta["wordList"]:
                            pointList.append({"x": resData["dataList"][word][0], "y": resData["dataList"][word][1]})
                        if verifyCaptcha(pointList, captchaMeta, uuid):
                            success = True
                            break
                        else:
                            requests.get(
                                f'https://www.cinea.com.cn/api/sqp/reportWrongCaptcha?picId={resData["picId"]}')
            except Exception as e:
                print("单次在线打码失败，原因：" + str(e))
                pass
        if not success:
            raise SystemError("很抱歉，验证码识别失败！在失败前已重试30次。")
    else:
        # 本地JavaScript打码（推荐）
        while True:
            uuid = "point-" + genUUID()
            captchaMeta = getCaptchaOnce(uuid)
            offlineResult = offlineCaptcha.captchaOfflineBreaker(captchaMeta["image"], captchaMeta["wordList"])
            if offlineResult["reason"] == 1:
                return False, ""
            pointList = offlineResult["result"]
            if verifyCaptcha(pointList, captchaMeta, uuid):
                break

    # 阶段四：制作验证码密钥
    captchaVerification = aesEncrypt(captchaMeta["token"] + '---' + json.dumps(pointList).replace(' ', ''),
                                     captchaMeta["secretKey"]) if captchaMeta["secretKey"] else captchaMeta["token"] + '---' + json.dumps(pointList).replace(' ', '')

    return True, captchaVerification
