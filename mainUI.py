from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from UI._mainUI import Ui_MainWindow
from Control import XboxUI, MboxUI,SboxUI
import public


class MainWindow(object):
    """主窗口封装类"""

    def __init__(self):

        self.dialog = QtWidgets.QMainWindow()
        window = Ui_MainWindow()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        #学生label
        self.SIDLabel = window.SID
        self.SnameLabel = window.Sname
        self.SsexLabel = window.Ssex
        self.LnoLabel = window.Lno
        self.SnoLabel = window.Sno
        self.MnameLabel = window.Mname
        self.MIDLabel = window.MID

        # 宿管label
        self.MIDLabel_1 = window.Mno
        self.MnameLabel_1 = window.Mname_2
        self.MsexLabel = window.MSex
        self.MageLabel = window.Mage
        self.MphoneLabel = window.MPhone

        # 宿舍label
        self.LnoLabel_1 = window.Lno_2
        self.SnoLabel_2 = window.Sno_2
        self.K_nLabel = window.K_n
        self.C_nlabel = window.C_n
        self.L_nlabel = window.L_n
        self.Locationlabel = window.Location


        #高级搜索学生
        self.searchButtonX = window.SearchButton_1
        self.searchButtonX.clicked.connect(self.onSearchX)
        # 高级搜索宿管
        self.searchButtonM = window.SearchButton_3
        self.searchButtonM.clicked.connect(self.onSearchM)
        # 高级搜索宿舍
        self.searchButtonS = window.SearchButton_2
        self.searchButtonS.clicked.connect(self.onSearchS)
        #新建学生档案
        self.actionAddX = window.actionEdit_1
        self.actionAddX.clicked.connect(self.onAddStudentX)
        # 新建宿管档案
        self.actionAddM = window.actionEdit_3
        self.actionAddM.clicked.connect(self.onAddStudentM)
        # 新建宿舍档案
        self.actionAddS = window.actionEdit_2
        self.actionAddS.clicked.connect(self.onAddStudentS)
        # 学生"快速检索信息, 使用"|"分隔多个条件"
        self.searchEditX = window.SearchEdit_1
        self.searchEditX.textChanged['QString'].connect(self.onQuickSearchX)
        # 宿管"快速检索信息, 使用"|"分隔多个条件"
        self.searchEditM = window.SearchEdit_3
        self.searchEditM.textChanged['QString'].connect(self.onQuickSearchM)
        # 宿舍"快速检索信息, 使用"|"分隔多个条件"
        self.searchEditS = window.SearchEdit_2
        self.searchEditS.textChanged['QString'].connect(self.onQuickSearchS)
        #修改学生信息
        self.editButtonX = window.editButton_1
        self.editButtonX.clicked.connect(self.onEditX)
        # 修改宿管信息
        self.editButtonM = window.editButton_3
        self.editButtonM.clicked.connect(self.onEditM)
        # 修改宿舍信息
        self.editButtonS = window.editButton_2
        self.editButtonS.clicked.connect(self.onEditS)
        # 删除学生信息
        self.deleteButtonX = window.DeleteButton_1
        self.deleteButtonX.clicked.connect(self.onDeleteX)
        # 删除宿管信息
        self.deleteButtonM = window.DeleteButton_3
        self.deleteButtonM.clicked.connect(self.onDeleteM)
        # 删除宿舍信息
        self.deleteButtonS = window.DeleteButton_2
        self.deleteButtonS.clicked.connect(self.onDeleteS)
        #学生表
        self.studentTable = window.studentTable
        self.tableListX = []  # Student
        self.tableIndexX = {}  # Student -> Item
        self.studentTable.itemSelectionChanged.connect(self.onSelectStudent)
        self.studentTable.activated.connect(self.onEditX)

        width = [150, 102, 70, 70, 70, 70,70,150]
        [self.studentTable.setColumnWidth(i, width[i]) for i in range(7)]
        self.searchModeX = 0  # 0不搜索 1快速搜索 2高级搜索

        window.SearchBox_1.currentTextChanged['QString'].connect(self.onSearchByX)

        # 宿管表
        self.managerTable = window.Mtable
        self.tableListM = []  # Manager
        self.tableIndexM = {}  # Manager -> Item
        self.managerTable.itemSelectionChanged.connect(self.onSelectManager)
        self.managerTable.activated.connect(self.onEditM)

        width = [125,125,125,125,125]
        [self.managerTable.setColumnWidth(i, width[i]) for i in range(5)]
        self.searchModeM = 0  # 0不搜索 1快速搜索 2高级搜索

        window.SearchBox_3.currentTextChanged['QString'].connect(self.onSearchByM)

        # 宿舍表
        self.susheTable = window.ShusheTable
        self.tableListS = []  # Sushe
        self.tableIndexS = {}  # Sushe -> Item
        self.susheTable.itemSelectionChanged.connect(self.onSelectSushe)
        self.susheTable.activated.connect(self.onEditS)

        width = [92,92,92,92,92,200]
        [self.susheTable.setColumnWidth(i, width[i]) for i in range(6)]
        self.searchModeS = 0  # 0不搜索 1快速搜索 2高级搜索

        window.SearchBox_2.currentTextChanged['QString'].connect(self.onSearchByS)

        self.onSearchByM("工号")
        self.onSearchByS("楼号")
        self.onSearchByX("学号")

    def onSearchByX(self, searchByX):
        from Control.student import attributeListX as attrs
        for attr, translate in attrs:
            if searchByX == translate:
                self.quickSearchByX = attr
        self.onQuickSearchX()
    def onSearchByM(self, searchByM):
        from Control.manager import attributeListM as attrs
        for attr, translate in attrs:
            if searchByM == translate:
                self.quickSearchByM = attr
        self.onQuickSearchM()
    def onSearchByS(self, searchByS):
        from Control.sushe import attributeListS as attrs
        for attr, translate in attrs:
            if searchByS == translate:
                self.quickSearchByS = attr
        self.onQuickSearchS()

    def onQuickSearchX(self):
        key = self.searchEditX.text()
        key = ' '.join(key.split())
        result = public.studentManager.search(self.quickSearchByX, key)
        self.tableShowX(result)
    def onQuickSearchM(self):
        key = self.searchEditM.text()
        key = ' '.join(key.split())
        result = public.suguangManager.search(self.quickSearchByM, key)
        self.tableShowM(result)
    def onQuickSearchS(self):
        key = self.searchEditS.text()
        key = ' '.join(key.split())
        result = public.susheManager.search(self.quickSearchByS, key)
        self.tableShowS(result)

    def onSearchX(self):
        def _onSaerch(keyList):
            result = public.studentManager.multiSearch(keyList)
            self.tableShowX(result)
        self._saerchBox = XboxUI.SearchBox(_onSaerch)
        self._saerchBox.show()
    def onSearchM(self):
        def _onSaerch(keyList):
            result = public.suguangManager.multiSearch(keyList)
            self.tableShowM(result)
        self._saerchBox = MboxUI.SearchBox(_onSaerch)
        self._saerchBox.show()
    def onSearchS(self):
        def _onSaerch(keyList):
            result = public.susheManager.multiSearch(keyList)
            self.tableShowS(result)
        self._saerchBox = SboxUI.SearchBox(_onSaerch)
        self._saerchBox.show()

    def onAddStudentX(self):
        def _onAddStudentX(_student):
            student = _student.copy()
            public.studentManager.add(student)
            self.tableSetX(student)
        self._newBox = XboxUI.NewBox(_onAddStudentX)
        self._newBox.show()
    def onAddStudentM(self):
        def _onAddManager(_manager):
            manager = _manager.copy()
            public.suguangManager.add(manager)
            self.tableSetM(manager)
        self._newBox = MboxUI.NewBox(_onAddManager)
        self._newBox.show()
    def onAddStudentS(self):
        def _onAddSusheManager(_sushe):
            sushe = _sushe.copy()
            public.susheManager.add(sushe)
            self.tableSetS(sushe)
        self._newBox = SboxUI.NewBox(_onAddSusheManager)
        self._newBox.show()

    def onDeleteX(self):
        student = self.selectionX
        if not student:
            return
        confirm = QMessageBox.warning(QtWidgets.QWidget(),
                                      "删除档案", "确认删除此档案?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            item = self.tableIndexX[student]
            n = self.studentTable.topLevelItemCount()
            for i in range(0, n):
                if self.studentTable.topLevelItem(i) == item:
                    self.studentTable.takeTopLevelItem(i)
                    self.tableListX.remove(student)
                    self.tableIndexX.pop(student)
                    break
            public.studentManager.delete(student)
    def onDeleteM(self):
        manager = self.selectionM
        if not manager:
            return
        confirm = QMessageBox.warning(QtWidgets.QWidget(),
                                      "删除档案", "确认删除此档案?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            item = self.tableIndexM[manager]
            n = self.managerTable.topLevelItemCount()
            for i in range(0, n):
                if self.managerTable.topLevelItem(i) == item:
                    self.managerTable.takeTopLevelItem(i)
                    self.tableListM.remove(manager)
                    self.tableIndexM.pop(manager)
                    break
            public.suguangManager.delete(manager)
    def onDeleteS(self):
        sushe = self.selectionS
        if not sushe:
            return
        confirm = QMessageBox.warning(QtWidgets.QWidget(),
                                      "删除档案", "确认删除此档案?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            item = self.tableIndexS[sushe]
            n = self.susheTable.topLevelItemCount()
            for i in range(0, n):
                if self.susheTable.topLevelItem(i) == item:
                    self.susheTable.takeTopLevelItem(i)
                    self.tableListS.remove(sushe)
                    self.tableIndexS.pop(sushe)
                    break
            public.susheManager.delete(sushe)

    def onEditX(self):
        student = self.selectionX
        if not student:
            return
        def _onEditX(_student):
            public.studentManager.delete(student)
            _student.copyTo(student)
            public.studentManager.add(student)
            
            if student in self.tableIndexX:
                self.tableSetX(student, self.tableIndexX[student])
        self._editBox = XboxUI.EditBox(student, _onEditX)
        self._editBox.show()
    def onEditM(self):
        manager = self.selectionM
        if not manager:
            return

        def _onEditM(_manager):
            if _manager.MID != manager.MID:
                public.suguangManager.delete(manager)
                _manager.copyTo(manager)
                public.suguangManager.add(manager)
            else:
                _manager.copyTo(manager)
                public.suguangManager.edit(manager)
            if manager in self.tableIndexM:
                self.tableSetM(manager, self.tableIndexM[manager])

        self._editBox = MboxUI.EditBox(manager, _onEditM)
        self._editBox.show()
    def onEditS(self):
        sushe = self.selectionS
        if not sushe:
            return

        def _onEditS(_sushe):
            if _sushe.Lno != sushe.Lno and _sushe.Sno != sushe.Sno :
                public.suguangManager.delete(sushe)
                _sushe.copyTo(sushe)
                public.susheManager.add(sushe)
            else:
                _sushe.copyTo(sushe)
                public.susheManager.edit(sushe)
            if sushe in self.tableIndexS:
                self.tableSetS(sushe, self.tableIndexS[sushe])

        self._editBox = SboxUI.EditBox(sushe, _onEditS)
        self._editBox.show()

    def setStudentInfo(self, student=None):
        student = student or public.studentManager.emptyStudent
        self.SIDLabel.setText(student.SID)
        self.SnameLabel.setText(student.Sname)
        self.SsexLabel.setText(student.getSex())
        self.LnoLabel.setText(str(student.Lno))
        self.SnoLabel.setText(str(student.Sno))
        self.MIDLabel.setText(student.MID)
        self.MnameLabel.setText(student.Mname)
    def setManagerInfo(self, manager=None):
        manager = manager or public.suguangManager.emptyManager
        self.MIDLabel_1.setText(manager.MID)
        self.MnameLabel_1.setText(manager.Mname)
        self.MsexLabel.setText(manager.getSex())
        self.MageLabel.setText(str(manager.Mage))
        self.MphoneLabel.setText(manager.Mphone)
    def setSusheInfo(self, sushe=None):
        sushe = sushe or public.susheManager.emptySushe
        self.LnoLabel_1.setText(sushe.Lno)
        self.SnoLabel_2.setText(sushe.Sno)
        self.K_nLabel.setText(str(sushe.K_n))
        self.C_nlabel.setText(str(sushe.C_n))
        self.L_nlabel.setText(str(sushe.L_n))
        self.Locationlabel.setText(sushe.Location)

    def show(self):
        self.dialog.show()

    def tableShowX(self, studentList):
        self.tableClearX()
        for student in studentList:
            self.tableAddX(student)
        self.onSelectStudent()
    def tableShowM(self, MList):
        self.tableClearM()
        for manager in MList:
            self.tableAddM(manager)
        self.onSelectManager()
    def tableShowS(self, SList):
        self.tableClearS()
        for sushe in SList:
            self.tableAddS(sushe)
        self.onSelectSushe()

    def tableAddX(self, student):
        item = QtWidgets.QTreeWidgetItem(self.studentTable)
        self.tableSetX(student, item)
        self.tableListX.append(student)
        self.tableIndexX[student] = item
    def tableAddM(self, manager):
        item = QtWidgets.QTreeWidgetItem(self.managerTable)
        self.tableSetM(manager, item)
        self.tableListM.append(manager)
        self.tableIndexM[manager] = item
    def tableAddS(self, sushe):
        item = QtWidgets.QTreeWidgetItem(self.susheTable)
        self.tableSetS(sushe, item)
        self.tableListS.append(sushe)
        self.tableIndexS[sushe] = item

    def tableSetX(self, student, item=None):
        if item:
            item.setText(0, student.SID)
            item.setText(1, student.Sname)
            item.setText(2, student.getSex())
            item.setText(3, str(student.Lno))
            item.setText(4, str(student.Sno))
            item.setText(5, student.MID)
            item.setText(6, student.Mname)
        elif self.searchModeX == 0:
            self.tableAddX(student)
    def tableSetM(self, manager, item=None):
        if item:
            item.setText(0, manager.MID)
            item.setText(1, manager.Mname)
            item.setText(2, manager.getSex())
            item.setText(3, str(manager.Mage))
            item.setText(4, manager.Mphone)
        elif self.searchModeM == 0:
            self.tableAddM(manager)
    def tableSetS(self, sushe, item=None):
        if item:
            item.setText(0, sushe.Lno)
            item.setText(1, sushe.Sno)
            item.setText(2, str(sushe.L_n))
            item.setText(3, str(sushe.C_n))
            item.setText(4, str(sushe.K_n))
            item.setText(5, sushe.Location)

        elif self.searchModeS == 0:
            self.tableAddS(sushe)

    def tableClearX(self):
        self.studentTable.clear()
        self.tableListX.clear()
        self.tableIndexX.clear()
    def tableClearM(self):
        self.managerTable.clear()
        self.tableListM.clear()
        self.tableIndexM.clear()
    def tableClearS(self):
        self.susheTable.clear()
        self.tableListS.clear()
        self.tableIndexS.clear()

    def onSelectStudent(self):
        item = self.studentTable.selectedItems()
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.tableIndexX.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.selectionX = selection
        self.setStudentInfo(selection)
        self.editButtonX.setEnabled(selected)
        self.deleteButtonX.setEnabled(selected)
    def onSelectManager(self):
        item = self.managerTable.selectedItems()
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.tableIndexM.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.selectionM = selection
        self.setManagerInfo(selection)
        self.editButtonM.setEnabled(selected)
        self.deleteButtonM.setEnabled(selected)
    def onSelectSushe(self):
        item = self.susheTable.selectedItems()
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.tableIndexS.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.selectionS = selection
        self.setSusheInfo(selection)
        self.editButtonS.setEnabled(selected)
        self.deleteButtonS.setEnabled(selected)
