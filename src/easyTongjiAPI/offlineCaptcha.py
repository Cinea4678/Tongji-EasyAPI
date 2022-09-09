"""
  Hey,don't import me! I am for internal use.
  -------------------------------------
  Project Tongji-EasyAPI
  offlineCaptcha.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

#  不幸的是，使用打码平台处理ids系统的验证码并不是一个明智的选择
#  因此编写了这个offlineCaptcha系统，希望能通过用户手动点选以完成1系统的验证


from http.server import HTTPServer, BaseHTTPRequestHandler
import os, threading, json, re, time, webbrowser
from typing import Union
from urllib.parse import unquote
import inspect, ctypes
import logging

logging.basicConfig(level=logging.ERROR)


# 进程停止代码

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        """
        if it returns a number greater than one, you're in trouble,
        and you should call it again with exc=NULL to revert the effect
        """
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


host = ('127.0.0.1', 810)
httpfilepath = os.path.dirname(os.path.abspath(__file__)) + "/web"  # web文件路径

# 使用全局变量通信
stopFlag = False
heartBeat = False
stopReason = 0  # 0:自动中断；1:用户中断
imageB64 = ""
wordList = ""
result = []


# 本地Server

class localCaptchaServer(BaseHTTPRequestHandler):
    finished = False

    # 禁用日志输出
    def log_request(self, code: Union[int, str] = '-', size: Union[int, str] = '-') -> None:
        return

    # GET处理文件请求
    def do_GET(self):
        path = str(self.path)
        try:
            with open(httpfilepath + path, "rb") as file:
                fileContent = file.read()
            self.send_response(200)
            self.send_header("content-type", "*/*")
            self.end_headers()
            self.wfile.write(fileContent)
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    # POST处理api请求
    def do_POST(self):
        global stopFlag, stopReason
        path = str(self.path)
        command = re.findall(r"^/api/(.*?)$", path)
        if len(command) == 0:
            self.send_error(400, "Bad Request")
        else:
            command = command[0]
            if command == "hello":
                # 开发调试用
                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Hello!".encode())
            elif command == "heartbeat":
                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Ok!".encode())
                if not self.finished:
                    stopFlag = False
            elif command == "getdata":
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"imageBase64": imageB64, "wordsList": wordList}).encode())
            elif "submit" in command:
                command = unquote(command)
                jsonData = re.findall(r"json=(.*)", command)
                try:
                    jsonData = json.loads(jsonData[0])
                    global result
                    result = jsonData["result"]
                    self.send_response(200)
                    self.send_header("content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write("ok".encode())
                    self.finished = True
                    stopFlag = True
                    stopReason = 0
                except json.JSONDecodeError or IndexError or KeyError:
                    self.send_error(400, "Bad request")
            else:
                self.send_error(404, "Command not found")


class checkFinishThread(threading.Thread):
    def __init__(self, server):
        self.server = server
        super().__init__()

    def run(self):
        global stopFlag
        time.sleep(5)  # 等待浏览器和http server启动
        while not stopFlag:
            stopFlag = True
            time.sleep(1)
        self.server.shutdown()


class openBrowserThread(threading.Thread):
    """
    使用线程打开浏览器的原因：希望能够延时几秒防止打开浏览器后后端服务未启动导致404
    """

    def __init__(self):
        self.opened = False
        super().__init__()

    def run(self):
        if not self.opened:
            time.sleep(1.5)
            webbrowser.open("http://127.0.0.1:810/index.html", new=1)
            self.opened = True


# 初始化/重新初始化app
# noinspection PyStatementEffect
def captchaOfflineBreaker(imagebs64: str, clickwords: list) -> dict:
    """
    @return: 返回一个字典。字段"result":结果，"reason"退出原因，为1时需中断验证过程并切断登陆。
    """
    # 重置全局变量
    global stopFlag, imageB64, wordList, result
    stopFlag = False
    imageB64 = imagebs64
    wordList = ",".join(clickwords)
    result = []

    server = HTTPServer(host, localCaptchaServer)
    checking = checkFinishThread(server)
    browserThread = openBrowserThread()
    browserThread.start()
    checking.start()
    server.serve_forever()

    # 检查结果有效性
    try:
        result[0]["x"], result[0]["y"]
        result[1]["x"], result[1]["y"]
        result[2]["x"], result[2]["y"]
    except IndexError or KeyError:
        result = [{"x": 0, "y": 0}, {"x": 0, "y": 0}, {"x": 0, "y": 0}]

    # stop_thread(browserThread)
    # stop_thread(checking)

    return {"result": result, "reason": stopReason}


if __name__ == "__main__":
    with open("image.jpg", "rb") as f:
        imageB64 = f.read()
    import base64

    imageB64 = base64.b64encode(imageB64).decode("utf-8")
    captchaOfflineBreaker(imageB64, ["我", "尼", "马"])
