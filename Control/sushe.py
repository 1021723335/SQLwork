import sql

#宿管属性集
attributeListM = [
    ("Lno","楼号"),
    ("Sno","宿舍号"),
    ("L_n","入住人数"),
    ("C_n","剩余空位"),
    ("K_n","可容纳人数"),
    ("Location","位置"),
]
class SusheManager(object):
    """宿舍管理类, 单例"""

    def __init__(self):
        # 用于存储所有宿舍对象
        self.SList = []
        # 楼号+宿舍号 -> 宿舍对象
        self.SLSID = {}

        self.load()

        self.emptySushe = Sushe()

    def add(self, sushe):
        self.SList.append(sushe)
        self.SLSID[sushe.Lno+sushe.Sno] = sushe
        sql.sushe_add(sushe)

    def edit(self, sushe):
        sql.sushe_edit(sushe)
        return True

    def delete(self, sushe):
        self.SLSID.pop(sushe.Lno+sushe.Sno)
        self.SList.remove(sushe)
        sql.sushe_delete(sushe)
        return True

    def multiSearch(self, keyList):
        # print(keyList)
        searchBy = []
        keyText = []
        #print(keyList)
        for searchby, keytext in keyList:
            if keytext:
                searchBy.append(searchby)
                keyText.append(keytext)
        msg = sql.sushe_multiselect(searchBy, keyText)
        #print(searchBy)
        #print(keyText)
        result = self.tosushe(msg)
        return result

    def search(self, searchBy, keyList):
        #print(searchBy)
        result = []
        if not keyList:
            result = self.MList
            return result
        else:
            keyList = keyList.split()

            for i in keyList:
                msg = sql.sushe_select(searchBy, i)
                result = result + self.tosushe(msg)
            # print(result)
            return result

    def tosushe(self,msg):
        result = []
        for i in range(len(msg)):
            # 创建每一个数据的manager对象
            m = msg[i]
            # print(s)
            sushe = Sushe()
            sushe.Lno = m[0]
            sushe.Sno = m[1]
            sushe.L_n = m[2]
            sushe.C_n = m[3]
            sushe.K_n = m[4]
            sushe.Location = m[5]
            result.append(sushe)
        return result

    def load(self):
        SList = []
        SLSID = {}
        try:
            msg = sql.Load("m_table")
            result = self.tosushe(msg)
            for manager in result:
                MList.append(manager)
                MMID[manager.MID] = manager
            result = True
        except:
            result = False
        finally:
            self.MList = MList
            self.MMID = MMID

        #print(self.MMID)
        #print(self.MList)
        return result

class Sushe(object):
    """宿舍类, 用于存储宿管基本信息"""
    def __init__(self, Lno="", Sno="", L_n=0, C_n="", K_n="",Location=""):
        self.Lno = Lno
        self.Sno = Sno
        self.L_n = L_n
        self.C_n = C_n
        self.K_n = K_n
        self.Location = Location

    def copy(self):
        sushe = Sushe()
        self.copyTo(sushe)
        return sushe

    def copyTo(self, sushe):
        sushe.Lno = self.Lno
        sushe.Sno = self.Sno
        sushe.L_n = self.L_n
        sushe.C_n = self.C_n
        sushe.K_n = self.K_n
        sushe.Location = self.Location

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeListM:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.checkS(self.Lno,self.Sno,new)
        if check[0] ==0:
            return check

        return (True, "")
