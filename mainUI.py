from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from UI._mainUI import Ui_MainWindow
import XboxUI
import MboxUI
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

        #高级搜索学生
        self.searchButtonX = window.SearchButton_1
        self.searchButtonX.clicked.connect(self.onSearchX)
        # 高级搜索宿管
        self.searchButtonM = window.SearchButton_3
        self.searchButtonM.clicked.connect(self.onSearchM)
        #新建学生档案
        self.actionAddX = window.actionEdit_1
        self.actionAddX.clicked.connect(self.onAddStudentX)
        # 新建宿管档案
        self.actionAddM = window.actionEdit_3
        self.actionAddM.clicked.connect(self.onAddStudentM)
        # 学生"快速检索信息, 使用空格分隔多个条件"
        self.searchEditX = window.SearchEdit_1
        self.searchEditX.textChanged['QString'].connect(self.onQuickSearchX)
        # 宿管"快速检索信息, 使用空格分隔多个条件"
        self.searchEditM = window.SearchEdit_3
        self.searchEditM.textChanged['QString'].connect(self.onQuickSearchM)
        #修改学生信息
        self.editButtonX = window.editButton_1
        self.editButtonX.clicked.connect(self.onEditX)
        # 修改宿管信息
        self.editButtonM = window.editButton_3
        self.editButtonM.clicked.connect(self.onEditM)
        # 删除学生信息
        self.deleteButtonX = window.DeleteButton_1
        self.deleteButtonX.clicked.connect(self.onDeleteX)
        # 删除宿管信息
        self.deleteButtonM = window.DeleteButton_3
        self.deleteButtonM.clicked.connect(self.onDeleteM)
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

        window.SearchBox_1.currentTextChanged['QString'].connect(self.onSearchByM)

        self.onSearchByM("工号")
        self.onSearchByX("学号")

    def onSearchByX(self, searchByX):
        from student import attributeListX as attrs
        for attr, translate in attrs:
            if searchByX == translate:
                self.quickSearchByX = attr
        self.onQuickSearchX()
    def onSearchByM(self, searchByM):
        from manager import attributeListM as attrs
        for attr, translate in attrs:
            if searchByM == translate:
                self.quickSearchByM = attr
        self.onQuickSearchM()

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
            public.suguangManager.delete(manager)
            _manager.copyTo(manager)
            public.suguangManager.add(manager)

            if manager in self.tableIndexM:
                self.tableSetM(manager, self.tableIndexM[manager])

        self._editBox = MboxUI.EditBox(manager, _onEditM)
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

    def tableClearX(self):
        self.studentTable.clear()
        self.tableListX.clear()
        self.tableIndexX.clear()
    def tableClearM(self):
        self.managerTable.clear()
        self.tableListM.clear()
        self.tableIndexM.clear()

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
