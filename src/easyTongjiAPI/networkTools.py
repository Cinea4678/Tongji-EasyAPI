"""
  Hey,don't import me! I am for internal use.
  -------------------------------------
  Project Tongji-EasyAPI
  networkTools.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""
import array
import time, math
from random import random
import base64
import fastgm
from Crypto.Cipher import AES


def _genUUID():
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
_idsHeaders = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "Authorization": "Basic MjE1Mjk1NTo4MzEwMzM=",
    "origin": "https://ids.tongji.edu.cn:8443",
    "referer": "https://ids.tongji.edu.cn:8443/nidp/app/login?id=Login&sid=0&option=credential&sid=0&target=https%3A%2F%2Fids.tongji.edu.cn%3A8443%2Fnidp%2Foauth%2Fnam%2Fauthz%3Fscope%3Dprofile%26response_type%3Dcode%26redirect_uri%3Dhttps%3A%2F%2F1.tongji.edu.cn%2Fapi%2Fssoservice%2Fsystem%2FloginIn%26client_id%3D" + _genUUID(),
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}


def idsHeaders() -> dict:
    return _idsHeaders


# noinspection SpellCheckingInspection
_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "origin": "https://1.tongji.edu.cn",
    "referer": "https://1.tongji.edu.cn/workbench",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
}


def headers() -> dict:
    return _headers


def ts() -> int:
    """Time stamp of JavaScript"""
    return int(time.time() * 1000)


def sm2Encrypt(data: str, publicKey: str):
    """
    不要在ids登录验证以外的场景使用本函数！！！
    """
    sm2c = fastgm.SM2("C1C2C3")
    data_enc = base64.b64encode(data.encode("utf-8"))
    return "04" + sm2c.encrypt(publicKey[2:], data_enc).hex()


def parseStrCookie(cookie):
    return dict([l.split("=", 1) for l in cookie.split("; ")])


def aesEncrypt(data: str, key: str, iv: str):
    """
    请不要在1系统以外场景使用本函数
    """

    def paramHandler(e: str) -> str:
        # 一系统使用的混淆函数
        t = [c for c in e]
        a = ["" for _ in range(len(t))]
        r = 0
        while r < len(t):
            if r + 1 <= len(t):
                a[r] = t[r + 1]
                a[r + 1] = t[r]
            else:
                a[r] = t[r]
            r += 2
        return "".join(a)

    def pkcs7padding(text):
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = 16 - padding_size % 16
        padding_text = chr(padding) * padding
        return text + padding_text

    key = paramHandler(key).encode('utf-8')
    iv = paramHandler(iv).encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = pkcs7padding(data)
    encrypt = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypt).decode('utf-8')



if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    print(aesEncrypt('2152955', 'Cf^mp7A1qwPKNTnj', 'aM5W2a%vI%e9$mIU'))