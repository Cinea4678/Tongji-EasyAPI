"""
  Project Tongji-EasyAPI
  models.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from collections import namedtuple


Student = namedtuple('Student', ['name', 'studentId', 'sex', 'faculty', 'facultyName', 'grade'])

electRound = namedtuple("electRound", ["id", "name", "isOpen", "beginTime", "endTime", "createdTime", "updateTime",
                                       "remark", "calendarId", "calendarName"])

class Scores:

    gradePoint: float = ...  #学生总寄点
    earnedCredits: float = ...  #已修读学分
    failedCredits: float = ...  #不及格学分
    failedNum: int = ...  #不及格门数
    termNum: int = ...  #学期数量
    coursesList: list = ...  #课程列表

    courseNum: int = ...  #已修读课程数量
    gradeExcellence: int  = ... #获优课程门数
    gradeGood: int = ...  #获良课程门数
    gradeMedium: int = ...  #获中课程门数
    gradePass: int = ...  #获及格课程门数
    gradeFailed: int  = ... #获不及格课程门数
    
    def __init__(self:Scores, sourceData:dict):
        ...

    def __str__(self:Scores) -> str:...

    def __repr__(self:Scores) -> str:...