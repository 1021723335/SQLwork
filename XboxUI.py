from PyQt5 import QtWidgets, QtCore, QtGui
from UI._Xbox import Ui_Xbox
from student import Student

class StudentBox(object):
    """学生信息编辑盒 - 基类"""

    def __init__(self):

        self.dialog = QtWidgets.QDialog()
        window = Ui_Xbox()
        window.setupUi(self.dialog)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../收藏夹/iCloud Photos/Downloads/2019/IMG_0574.PNG"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        self.SIDEdit= window.SIDEdit        #学号编辑
        self.SnameEdit = window.SnameEdit  #姓名编辑
        self.LnoEdit = window.LnoEdit      #楼号编辑
        self.SnoEdit = window.SnoEdit      #宿舍号编辑
        self.MnameEdit = window.MnameEdit   #楼管姓名编辑
        self.MIDEdit = window.MIDEdit       #楼管ID编辑

        self.msgLabel = window.msg          #提示信息

        self.okButton = window.okButton
        self.cancelButton = window.cancelButton
        self.okButton.clicked.connect(self.onOkButtonClicked)
        self.cancelButton.clicked.connect(self.dialog.close)

        self.maleButton = window.nanButton
        self.famaleButton = window.nvButton

    def getSex(self):
        if self.maleButton.isChecked():
            return 1
        elif self.famaleButton.isChecked():
            return 2
        else:
            return 0

    def setSex(self, value):
        if value == 1:
            self.maleButton.setChecked(True)
        elif value == 2:
            self.famaleButton.setChecked(True)

    def onOkButtonClicked(self):
        if self.onFinished():
            self.dialog.close()

    def show(self):
        self.dialog.show()

    def setTitle(self, title):
        self.dialog.setWindowTitle(title)

    def setMsg(self, text):
        self.msgLabel.setText(text)

    def setButton(self, ok, cancel=None):
        self.okButton.setText(ok)
        self.cancelButton.setText(cancel) if cancel is not None else None

    def applyToStudent(self, student):
        student.SID = self.SIDEdit.text()
        student.Sname = self.SnameEdit.text()
        student.Ssex = self.getSex()
        student.Lno = self.LnoEdit.text()
        student.Sno = self.SnoEdit.text()
        student.Mname = self.MnameEdit.text()
        student.MID = self.MIDEdit.text()

    def onFinished(self):
        return False


class EditBox(StudentBox):
    """编辑学生信息 - 继承StudentBox"""

    def __init__(self, student, callback):
        super(EditBox, self).__init__()
        self.callback = callback

        self.setTitle("修改信息...")
        self.setMsg("")
        self.setButton("修改")

        self.SIDEdit.setText(student.SID)
        self.SnameEdit.setText(student.Sname)
        self.setSex(str(student.Ssex))
        self.LnoEdit.setText(student.Lno)
        self.SnoEdit.setText(student.Sno)
        self.MnameEdit.setText(student.Mname)
        self.MIDEdit.setText(student.MID)

        self._student = Student()

    def onFinished(self):
        self.applyToStudent(self._student)
        check, info = self._student.checkInfo()
        if check:
            self.callback(self._student)
        else:
            self.setMsg(info)
        return check

    def show(self):
        self.SIDEdit.setEnabled(False)
        self.SnameEdit.setEnabled(False)
        self.SnameEdit.setClearButtonEnabled(False)
        self.SIDEdit.setClearButtonEnabled(False)
        self.dialog.show()


class NewBox(StudentBox):
    """新建学生档案 - 继承StudentBox"""

    def __init__(self, callback):
        super(NewBox, self).__init__()
        self.callback = callback

        self.setTitle("新建档案...")
        self.setMsg("")
        self.setButton("新建")

        self.student = Student()

    def onFinished(self):
        student = self.student
        self.applyToStudent(student)
        check, info = student.checkInfo(True)
        self.callback(self.student) if check else self.setMsg(info)
        return check


class SearchBox(StudentBox):
    """高级搜索框 - 继承StudentBox"""

    def __init__(self, callback):
        super(SearchBox, self).__init__()
        self.callback = callback

        self.setTitle("高级搜索...")
        self.setMsg("请输入检索关键词")
        self.setButton("搜索")

        self.maleButton.setEnabled(False)
        self.famaleButton.setEnabled(False)

    def onFinished(self):
        keyList = [
            ("SID", ' '.join(self.SIDEdit.text().split())),
            ("Sname", ' '.join(self.SnameEdit.text().split())),
            ("Lno", ' '.join(self.LnoEdit.text().split())),
            ("Sno", ' '.join(self.SnoEdit.text().split())),
            ("MID", ' '.join(self.MIDEdit.text().split())),
            ("Mname", ' '.join(self.MnameEdit.text().split())),
        ]
        self.callback(keyList)
        return True
