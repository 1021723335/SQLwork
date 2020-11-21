from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
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
        self.searchButtonX = window.SearchButton_1
        self.searchButtonX.clicked.connect(self.onSearchX)
        #新建学生档案
        self.actionAddX = window.actionEdit_1
        self.actionAddX.clicked.connect(self.onAddStudentX)
        # "快速检索信息, 使用空格分隔多个条件"
        self.searchEditX = window.SearchEdit_1
        self.searchEditX.textChanged['QString'].connect(self.onQuickSearchX)
        #修改学生信息
        self.editButtonX = window.editButton_1
        self.editButtonX.clicked.connect(self.onEditX)
        # 删除学生信息
        self.deleteButtonX = window.DeleteButton_1
        self.deleteButtonX.clicked.connect(self.onDeleteX)
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

        self.onSearchByX("学号")

    def onSearchByX(self, searchByX):
        from student import attributeListX as attrs
        for attr, translate in attrs:
            if searchByX == translate:
                self.quickSearchBy = attr
        self.onQuickSearchX()

    def onQuickSearchX(self):
        key = self.searchEditX.text()
        key = ' '.join(key.split())
        result = public.studentManager.search(self.quickSearchBy, key)
        self.tableShowX(result)

    def onSearchX(self):
        def _onSaerch(keyList):
            result = public.studentManager.multiSearch(keyList)
            self.tableShowX(result)
        self._saerchBox = XboxUI.SearchBox(_onSaerch)
        self._saerchBox.show()

    def onAddStudentX(self):
        def _onAddStudentX(_student):
            student = _student.copy()
            public.studentManager.add(student)
            self.tableSetX(student)
        self._newBox = XboxUI.NewBox(_onAddStudentX)
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

    def tableShowX(self, studentList):
        self.tableClearX()
        for student in studentList:
            self.tableAddX(student)
        self.onSelectStudent()

    def tableAddX(self, student):
        item = QtWidgets.QTreeWidgetItem(self.studentTable)
        self.tableSetX(student, item)
        self.tableListX.append(student)
        self.tableIndexX[student] = item

    def tableSetX(self, student, item=None):
        if item:
            item.setText(0, str(student.SID).zfill(9))
            item.setText(1, student.Sname)
            item.setText(2, student.getSex())
            item.setText(3, str(student.Lno))
            item.setText(4, str(student.Sno))
            item.setText(5, str(student.MID).zfill(3))
            item.setText(6, student.Mname)
        elif self.searchModeX == 0:
            self.tableAddX(student)

    def tableClearX(self):
        self.studentTable.clear()
        self.tableListX.clear()
        self.tableIndexX.clear()

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
        #self.actionAdd.setEnabled(selected)
        self.deleteButtonX.setEnabled(selected)
        #self.actionDelete.setEnabled(selected)
