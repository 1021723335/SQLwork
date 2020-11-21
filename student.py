import os
import public
import pickle
import sql

#学生属性集
attributeListX = [
    ("SID","学号"),
    ("Sname","姓名"),
    ("Ssex","性别"),
    ("Lno","楼号"),
    ("Sno","宿舍号"),
    ("MID","宿管ID"),
    ("Mname","宿管"),
]
class StudentManager(object):
    """学生管理类, 单例"""

    def __init__(self):
        # 用于存储所有学生对象
        self.studentList = []
        # 学号 -> 学生对象
        self.studentSID = {}

        self.load()

        self.emptyStudent = Student()

    def add(self, student):
        self.studentList.append(student)
        self.studentSID[student.SID] = student
        sql.student_add(student)

    def edit(self, student):
        self.studentSID.pop(student.SID)
        self.studentList.remove(student)
        sql.student_delete(student)
        return True

    def delete(self, student):
        self.studentSID.pop(student.SID)
        self.studentList.remove(student)
        sql.student_delete(student)
        return True

    def multiSearch(self, keyList):
        result = self.studentList.copy()
        for searchBy, keyText in keyList:
            if keyText:
                result = self.search(searchBy, keyText, result)
        return result

    def search(self, searchBy, keyList, searchList=None):
        result = []
        searchList = searchList or self.studentList
        if not keyList:
            return searchList.copy()
        else:
            keyList = keyList.split()
            if len(keyList) > 1:
                [keyList.pop(i) if not i else None for i in keyList]
            for student in searchList:
                target = getattr(student, searchBy)
                for key in keyList:
                    if key in target:
                        result.append(student)
                        break
            return result

    def load(self):
        studentList = []
        studentSID = {}
        try:
            msg = sql.studentLoad("x_table")
            for i in range(len(msg)):
                #创建每一个数据的student对象
                s = msg[i]
                #print(s)
                student = Student()
                student.SID = s[0]
                student.Sname = s[1]
                student.Ssex = s[2]
                student.Lno = s[3]
                student.Sno = s[4]
                student.MID = s[5]
                student.Mname = s[6]
                studentList.append(student)
                studentSID[student.SID] = student
            result = True
        except:
            result = False
        finally:
            self.studentList = studentList
            self.studentSID = studentSID

        #print(self.studentSID)
        #print(self.studentList)
        return result

class Student(object):
    """学生类, 用于存储学生基本信息"""
    def __init__(self, SID="", Sname="", Ssex=0, Lno="", Sno="", MID="", Mname=""):
        self.SID = SID
        self.Sname = Sname
        self.Ssex = Ssex
        self.Lno = Lno
        self.Sno = Sno
        self.MID = MID
        self.Mname = Mname

    def getSex(self):
        return ["", "男", "女"][self.Ssex]

    def copy(self):
        student = Student()
        self.copyTo(student)
        return student

    def copyTo(self, student):
        student.SID = self.SID
        student.Sname = self.Sname
        student.Ssex = self.Ssex
        student.Lno = self.Lno
        student.Sno = self.Sno
        student.MID = self.MID
        student.Mname = self.Mname

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeListX:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.checkX(self.SID,self.Lno,self.Sno,self.MID,new)
        if check[0] ==0:
            return check

        return (True, "")