'''
  Hey,don't import me! I am for internal use. 
  -------------------------------------
  Project Tongji-EasyAPI
  offlineCaptcha.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
'''

#ids系统captcha的js验证法

import time
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import os,multiprocessing
import requests,json
try:
    from . import verifyTools,networkTools
except:
    import verifyTools,networkTools

#去除Flask的输出    
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#web文件路径
httpfilepath = os.path.dirname(os.path.abspath(__file__))+"/web/"

app = Flask(__name__,static_folder=httpfilepath,static_url_path="/static/")

imageb64 = ""
clickword = ""
finished = False

#提交点击验证码结果
@app.route("/api/submit")
def submitRes():
    tokenForm= urlparse.parse_qs(urlparse.urlparse(request.url).query)
    try:
        jsonData = tokenForm["json"][0]
        submitData = json.loads(jsonData)
    except:
        return "Bad Request",400
    

@app.route("/api/abort")
def abort():
    global finished
    finished = True
    raise KeyboardInterrupt
    return "ok",200

#送出验证码图片和验证文字
@app.route("/api/getdata")
def getData():
    return make_response(json.dumps({
        "imageBase64Data" : imageb64,
        "clickWords":clickword
    }),200)

# #取静态资源
# @app.route("/file/<filename>")
# def getStatic(filename):
#     try:
#         with open(httpfilepath+filename,"rb") as f:
#             content = f.read()
#         return make_response(content,200)
#     except:
#         return make_response("ERROR",404)

def startServer(port):
    app.run(port=port)


#初始化/重新初始化app
def captchaOfflineBreaker(imagebs64:str,clickwords:list[str]):
    global imageb64,clickword
    imageb64 = imagebs64
    clickword = ",".join(clickwords)
    flask_process = multiprocessing.Process(target=startServer,args=[810])
    flask_process.start()
    while True:
        if finished == True:
            print(flask_process.is_alive())
            flask_process.kill()
            print(flask_process.is_alive())
            break
        time.sleep(1)

if __name__ == "__main__":
    captchaOfflineBreaker("1234",["2",'2','3','4'])