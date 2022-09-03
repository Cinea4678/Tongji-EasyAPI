'''
  Hey,don't import me! I am for internal use. 

  主要是用到的几个结构，包括学生信息、课程信息、成绩信息等等
  -------------------------------------
  Project Tongji-EasyAPI
  models.py
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
'''

class Student:
    """
    学生信息类型，推荐用户使用
    """
    def __init__(self,name="",studentId="",sex=0,faculty="",facultyName="",grade="",studentDataObject=None) -> None:
        if studentDataObject:
            try:
                name = studentDataObject["name"]
                studentId = studentDataObject["uid"]
                sex = studentDataObject["sex"]
                faculty = studentDataObject["faculty"]
                facultyName = studentDataObject["facultyName"]
                grade = studentDataObject["grade"]
            except:
                raise ValueError("您传入的数据不正确，若您没有来自1系统的user对象，则请您不要传入此参数。")
        self.name = name
        self.studentId = studentId
        self.sex = sex
        self.faculty = faculty
        self.facultyName = facultyName
        self.grade = grade
    
    def __str__(self) -> str:
        return f"<{self.name},{self.studentId},{self.facultyName},{self.grade}级>"

    def __repr__(self) -> str:
        return str(self)

class Scores:
    """
    集中存储查询到的成绩的类。既可以存储原始字典，又能自动计算丰富的元数据。

    我们相信，这些元数据可以帮助你省去不必要的代码。

    请查阅文档获取详细的属性信息。
    """
    def __init__(self, sourceData:dict):
        """
        集中存储查询到的成绩的类。既可以存储原始字典，又能自动计算丰富的元数据。

        我们相信，这些元数据可以帮助你省去不必要的代码。

        请查阅文档获取详细的属性信息。

        请注意：你需要传入的是`data`字段的内容
        """
        sd = sourceData  #节省代码量
        self.data = sourceData

        try:
            self.gradePoint = sd["totalGradePoint"]  #学生总寄点
            self.earnedCredits = sd["actualCredit"]  #已修读学分
            self.failedCredits = sd["failingCredits"]  #不及格学分
            self.failedNum = sd["failingCourseCount"]  #不及格门数
            self.termNum = len(sd["term"])   #学期数量
            self.coursesList = []     #课程列表

            courseNum = 0
            gradesNum = [0,0,0,0,0,0]
            for term in sd["term"]:
                courseNum+=len(term["creditInfo"])
                for courses in term["creditInfo"]:
                    gradesNum[int(courses["gradePoint"])]+=1
                    self.coursesList.append(courses)

            self.courseNum = courseNum   #已修读课程数量
            self.gradeExcellence = gradesNum[5]   #获优课程门数
            self.gradeGood = gradesNum[4]   #获良课程门数
            self.gradeMedium = gradesNum[3]   #获中课程门数
            self.gradePass = gradesNum[2]   #获及格课程门数
            self.gradeFailed = gradesNum[0]   #获不及格课程门数

            #更多功能，发issue，都可以加！

        except KeyError as e:
            raise ValueError("传入的内容不能被正确解析，请检查是否完整、正确传入")
    
    def __str__(self):
        return str(self.gradePoint)
    
    def __repr__(self) -> str:
        return f"<gpa:{self.gradePoint}, terms:{self.termNum}, courses:{self.courseNum}, excellence:{self.gradeExcellence}>"
