#宿舍属性集
attributeListS = [
    ("Lno","楼号"),
    ("Sno","宿舍号"),
    ("K_n","可容纳人数"),
    ("L_n","入住人数"),
    ("C_n","剩余空位"),
    ("Location","位置"),
]
#宿管属性集
attributeListM = [
    ("MID","工号"),
    ("Mname","姓名"),
    ("Msex","性别"),
    ("Mage","年龄"),
    ("Mphone","联系方式"),
]

class Sushe(object):
    """宿舍类, 用于存储宿舍基本信息"""
    def __init__(self, Lno="", Sno="", K_n=0, L_n="", C_n="", Location=""):
        self.Lno = Lno
        self.Sno = Sno
        self.K_n = L_n
        self.C_n = C_n
        self.L_n = L_n
        self.Location = Location

    def copy(self):
        sushe = Sushe()
        self.copyTo(sushe)
        return sushe

    def copyTo(self, Sushe):
        Sushe.Lno = self.Lno
        Sushe.Sno = self.Sno
        Sushe.K_n = self.L_n
        Sushe.C_n = self.C_n
        Sushe.L_n = self.L_n
        Sushe.Location = self.Location

class SuGuang(object):
    """宿管类, 用于存储宿管基本信息"""
    def __init__(self, MID="", Mname="", Msex=0,Mage="", Mphone=""):
        self.MID = MID
        self.Mname = Mname
        self.Msex = Msex
        self.Mage = Mage
        self.Mphone = Mphone

    def copy(self):
        suGuang = SuGuang()
        self.copyTo(suGuang)
        return suGuang

    def copyTo(self, SuGuang):
        SuGuang.MID = self.MID
        SuGuang.Mname = self.Mname
        SuGuang.Msex = self.Msex
        SuGuang.Mage = self.Mage
        SuGuang.Mphone = self.Mphone
