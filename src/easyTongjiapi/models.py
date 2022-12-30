"""
  Hey,don't import me! I am for internal use.

  主要是用到的几个结构，包括学生信息、课程信息、成绩信息等等

  -------------------------------------

  Project Tongji-EasyAPI
  models.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

from collections import namedtuple


Student = namedtuple('Student', ['name', 'studentId', 'sex', 'faculty', 'facultyName', 'grade'])
"""
  学生信息具名元组。
"""

electRound = namedtuple("electRound", ["id", "name", "isOpen", "beginTime", "endTime", "createdTime", "updateTime",
                                       "remark", "calendarId", "calendarName"])
"""
  选课信息具名元组。
"""


class Scores:
    """
    集中存储查询到的成绩的类。既可以存储原始字典，又能自动计算丰富的元数据。

    我们相信，这些元数据可以帮助你省去不必要的代码。

    请查阅文档获取详细的属性信息。
    """

    def __init__(self, sourceData: dict):
        """
        集中存储查询到的成绩的类。既可以存储原始字典，又能自动计算丰富的元数据。

        我们相信，这些元数据可以帮助你省去不必要的代码。

        请查阅文档获取详细的属性信息。

        请注意：你需要传入的是`data`字段的内容
        """
        sd = sourceData  # 节省代码量
        self.data = sourceData

        try:
            self.gradePoint = sd["totalGradePoint"]  # 学生总寄点
            self.earnedCredits = sd["actualCredit"]  # 已修读学分
            self.failedCredits = sd["failingCredits"]  # 不及格学分
            self.failedNum = sd["failingCourseCount"]  # 不及格门数

            courseNum = 0
            gradesNum = [0, 0, 0, 0, 0, 0]
            self.coursesList = []  # 课程列表

            try:
                self.termNum = len(sd["term"])  # 学期数量
                for term in sd["term"]:
                    courseNum += len(term["creditInfo"])
                    for courses in term["creditInfo"]:
                        gradesNum[int(courses["gradePoint"])] += 1
                        self.coursesList.append(courses)
            except TypeError as e:
                self.termNum = 0                # 学期数量

            self.courseNum = courseNum  # 已修读课程数量
            self.gradeExcellence = gradesNum[5]  # 获优课程门数
            self.gradeGood = gradesNum[4]  # 获良课程门数
            self.gradeMedium = gradesNum[3]  # 获中课程门数
            self.gradePass = gradesNum[2]  # 获及格课程门数
            self.gradeFailed = gradesNum[0]  # 获不及格课程门数

            # 更多功能，发issue，都可以加！

        except KeyError or TypeError as e:
            raise ValueError("传入的内容不能被正确解析，请检查是否完整、正确传入, 错误信息：" + str(e))

    def __str__(self):
        return str(self.gradePoint)

    def __repr__(self) -> str:
        return f"<gpa:{self.gradePoint}, terms:{self.termNum}, courses:{self.courseNum}, excellence:{self.gradeExcellence}>"
