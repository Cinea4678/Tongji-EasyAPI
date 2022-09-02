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
        self._name = name
        self._studentId = studentId
        self._sex = sex
        self._faculty = faculty
        self._facultyName = facultyName
        self._grade = grade
    
    def __str__(self) -> str:
        return f"<{self._name},{self._studentId},{self._facultyName},{self._grade}级>"

    def __repr__(self) -> str:
        return str(self)

    #无趣的属性函数
    @property
    def name(self):
        return self._name
    @property
    def studentId(self):
        return self._studentId
    @property
    def sex(self):
        return self._sex
    @property
    def faculty(self):
        return self._faculty
    @property
    def facultyName(self):
        return self._facultyName
    @property
    def grade(self):
        return self._grade
