import sql

#宿管属性集
attributeListM = [
    ("MID","工号"),
    ("Mname","姓名"),
    ("Msex","性别"),
    ("Mage","年龄"),
    ("Mphone","联系方式"),
]
class MManager(object):
    """宿管管理类, 单例"""

    def __init__(self):
        # 用于存储所有宿管对象
        self.MList = []
        # 工号 -> 宿管对象
        self.MMID = {}

        self.load()

        self.emptyManager = Manager()

    def add(self, manager):
        self.MList.append(manager)
        self.MMID[manager.MID] = manager
        sql.manager_add(manager)

    def edit(self, manager):
        sql.manager_edit(manager)
        return True

    def delete(self, manager):
        self.MMID.pop(manager.MID)
        self.MList.remove(manager)
        sql.manager_delete(manager)
        return True

    def multiSearch(self, keyList):
        result = self.MList.copy()
        for searchBy, keyText in keyList:
            if keyText:
                result = self.search(searchBy, keyText, result)
        return result

    def search(self, searchBy, keyList, searchList=None):
        result = []
        searchList = searchList or self.MList
        if not keyList:
            return searchList.copy()
        else:
            keyList = keyList.split()
            if len(keyList) > 1:
                [keyList.pop(i) if not i else None for i in keyList]
            for manager in searchList:
                target = getattr(manager, searchBy)
                for key in keyList:
                    if key in target:
                        result.append(manager)
                        break
            return result

    def load(self):
        MList = []
        MMID = {}
        try:
            msg = sql.Load("m_table")
            for i in range(len(msg)):
                #创建每一个数据的manager对象
                m = msg[i]
                #print(s)
                manager = Manager()
                manager.MID = m[0]
                manager.Mname = m[1]
                manager.Msex = m[2]
                manager.Mage = m[3]
                manager.Mphone = m[4]
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

class Manager(object):
    """宿管类, 用于存储宿管基本信息"""
    def __init__(self, MID="", Mname="", Msex=0, Mage="", Mphone=""):
        self.MID = MID
        self.Mname = Mname
        self.Msex = Msex
        self.Mage = Mage
        self.Mphone = Mphone

    def getSex(self):
        return ["", "男", "女"][self.Msex]

    def copy(self):
        manager = Manager()
        self.copyTo(manager)
        return manager

    def copyTo(self, manager):
        manager.MID = self.MID
        manager.Mname = self.Mname
        manager.Msex = self.Msex
        manager.Mage = self.Mage
        manager.Mphone = self.Mphone

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeListM:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.checkM(self.MID,new)
        if check[0] ==0:
            return check

        return (True, "")
