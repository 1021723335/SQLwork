from PyQt5 import QtWidgets, QtCore, QtGui
from UI._Mbox import Ui_Mbox
from manager import Manager

class MBox(object):
    """管理员信息编辑盒 - 基类"""

    def __init__(self):

        self.dialog = QtWidgets.QDialog()
        window = Ui_Mbox()
        window.setupUi(self.dialog)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../收藏夹/iCloud Photos/Downloads/2019/IMG_0574.PNG"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        self.MIDEdit= window.MnoEdit        #工号编辑
        self.MnameEdit = window.MnameEdit  #姓名编辑
        self.MageEdit = window.MageEdit  #年龄编辑
        self.MphoneEdit = window.MphonEdit   #楼管电话编辑
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

    def applyToManager(self, manager):
        manager.MID = self.MIDEdit.text()
        manager.Mname = self.MnameEdit.text()
        manager.Msex = self.getSex()
        manager.Mage = self.MageEdit.text()
        manager.Mphone = self.MphoneEdit.text()

    def onFinished(self):
        return False


class EditBox(MBox):
    """编辑宿管信息 - 继承MBox"""

    def __init__(self, manager, callback):
        super(EditBox, self).__init__()
        self.callback = callback

        self.setTitle("修改信息...")
        self.setMsg("")
        self.setButton("修改")

        self.MIDEdit.setText(manager.MID)
        self.MnameEdit.setText(manager.Mname)
        self.setSex(str(manager.Msex))
        self.MageEdit.setText(str(manager.Mage))
        self.MphoneEdit.setText(manager.Mphone)

        self._manager = Manager()
    def show(self):
        self.MIDEdit.setEnabled(False)
        self.MnameEdit.setEnabled(False)
        self.MnameEdit.setClearButtonEnabled(False)
        self.MIDEdit.setClearButtonEnabled(False)
        self.dialog.show()

    def onFinished(self):
        self.applyToManager(self._manager)
        check, info = self._manager.checkInfo()
        if check:
            self.callback(self._manager)
        else:
            self.setMsg(info)
        return check


class NewBox(MBox):
    """新建宿管档案 - 继承MBox"""

    def __init__(self, callback):
        super(NewBox, self).__init__()
        self.callback = callback

        self.setTitle("新建档案...")
        self.setMsg("")
        self.setButton("新建")

        self.manager = Manager()

    def onFinished(self):
        manager = self.manager
        self.applyToManager(manager)
        check, info = manager.checkInfo(True)
        self.callback(self.manager) if check else self.setMsg(info)
        return check


class SearchBox(MBox):
    """高级搜索框 - 继承MBox"""

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
            ("MID", ' '.join(self.MIDEdit.text().split())),
            ("Mname", ' '.join(self.MnameEdit.text().split())),
            ("Mage", ' '.join(self.MageEdit.text().split())),
            ("Mphone", ' '.join(self.MphoneEdit.text().split())),
        ]
        self.callback(keyList)
        return True
