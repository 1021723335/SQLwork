from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from UI._mainUI import Ui_MainWindow
import XboxUI
import public


class MainWindow(object):
    """主窗口封装类"""

    def __init__(self):

        self.dialog = QtWidgets.QMainWindow()
        window = Ui_MainWindow()
        window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.SIDLabel = window.SID
        self.SnameLabel = window.Sname
        self.SsexLabel = window.Ssex
        self.LnoLable = window.Lno
        self.SnoLable = window.Sno
        self.MnameLable = window.Mname
        self.MIDLable = window.MID
        #高级搜索
        self.searchButton = window.SearchButton_1
        self.searchButton.clicked.connect(self.onSearchX)
        #新建学生档案
        self.actionAdd = window.actionEdit_1
        self.actionAdd.clicked.connect(self.onAddStudentX)
        # "快速检索信息, 使用空格分隔多个条件"
        self.searchEdit = window.SearchEdit_1
        self.searchEdit.textChanged['QString'].connect(self.onQuickSearchX)
        #修改学生信息
        self.editButton = window.editButton_1
        self.editButton.clicked.connect(self.onEditX)
        # 删除学生信息
        self.deleteButton = window.DeleteButton_1
        self.deleteButton.clicked.connect(self.onDeleteX)
        #学生表
        self.studentTable = window.studentTable
        self.tableList = []  # Student
        self.tableIndex = {}  # Student -> Item
        self.studentTable.itemSelectionChanged.connect(self.onSelectStudent)
        self.studentTable.activated.connect(self.onEditX)

        width = [150, 102, 70, 70, 70, 70,70,150]
        [self.studentTable.setColumnWidth(i, width[i]) for i in range(7)]
        self.searchModeX = 0  # 0不搜索 1快速搜索 2高级搜索

        window.SearchBox_1.currentTextChanged['QString'].connect(self.onSearchByX)

        self.onSearchByX("学号")

    def onSearchByX(self, searchByX):
        from student import attributeListX as attrs
        for attr, translate in attrs:
            if searchByX == translate:
                self.quickSearchBy = attr
        self.onQuickSearchX()

    def onQuickSearchX(self):
        key = self.searchEdit.text()
        key = ' '.join(key.split())
        result = public.studentManager.search(self.quickSearchBy, key)
        self.tableShow(result)

    def onSearchX(self):
        def _onSaerch(keyList):
            result = public.studentManager.multiSearch(keyList)
            self.tableShow(result)
        self._saerchBox = XboxUI.SearchBox(_onSaerch)
        self._saerchBox.show()

    def onAddStudentX(self):
        def _onAddStudentX(_student):
            student = _student.copy()
            public.studentManager.add(student)
            self.tableSet(student)
        self._newBox = XboxUI.NewBox(_onAddStudentX)
        self._newBox.show()

    def onDeleteX(self):
        student = self.selection
        if not student:
            return
        confirm = QMessageBox.warning(QtWidgets.QWidget(),
                                      "删除档案", "确认删除此档案?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            item = self.tableIndex[student]
            n = self.studentTable.topLevelItemCount()
            for i in range(0, n):
                if self.studentTable.topLevelItem(i) == item:
                    self.studentTable.takeTopLevelItem(i)
                    self.tableList.remove(student)
                    self.tableIndex.pop(student)
                    break
            public.studentManager.delete(student)

    def onEditX(self):
        student = self.selection
        if not student:
            return
        def _onEditX(_student):
            public.studentManager.delete(student)
            _student.copyTo(student)
            public.studentManager.add(student)
            
            if student in self.tableIndex:
                self.tableSet(student, self.tableIndex[student])
        self._editBox = XboxUI.EditBox(student, _onEditX)
        self._editBox.show()

    def setStudentInfo(self, student=None):
        student = student or public.studentManager.emptyStudent
        self.SIDLabel.setText(student.SID)
        self.SnameLabel.setText(student.Sname)
        self.SsexLabel.setText(student.getSex())
        self.LnoLable.setText(str(student.Lno))
        self.SnoLable.setText(str(student.Sno))
        self.MIDLable.setText(student.MID)
        self.MnameLable.setText(student.Mname)

    def show(self):
        self.dialog.show()

    def tableShow(self, studentList):
        self.tableClear()
        for student in studentList:
            self.tableAdd(student)
        self.onSelectStudent()

    def tableAdd(self, student):
        item = QtWidgets.QTreeWidgetItem(self.studentTable)
        self.tableSet(student, item)
        self.tableList.append(student)
        self.tableIndex[student] = item

    def tableSet(self, student, item=None):
        if item:
            item.setText(0, str(student.SID).zfill(9))
            item.setText(1, student.Sname)
            item.setText(2, student.getSex())
            item.setText(3, str(student.Lno))
            item.setText(4, str(student.Sno))
            item.setText(5, str(student.MID).zfill(3))
            item.setText(6, student.Mname)
        elif self.searchModeX == 0:
            self.tableAdd(student)

    def tableClear(self):
        self.studentTable.clear()
        self.tableList.clear()
        self.tableIndex.clear()

    def onSelectStudent(self):
        item = self.studentTable.selectedItems()
        selected = True if item else False
        selection = None
        if selected:
            for k, v in self.tableIndex.items():
                if v == item[0]:
                    selection = k
                    break
            else:
                selected = False
        self.selection = selection
        self.setStudentInfo(selection)
        self.editButton.setEnabled(selected)
        #self.actionAdd.setEnabled(selected)
        self.deleteButton.setEnabled(selected)
        #self.actionDelete.setEnabled(selected)
