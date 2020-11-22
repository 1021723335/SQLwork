from PyQt5 import QtWidgets, QtCore, QtGui
from UI._Sbox import Ui_Sbox
from Control.sushe import Sushe

class SBox(object):
    """宿舍信息编辑盒 - 基类"""

    def __init__(self):

        self.dialog = QtWidgets.QDialog()
        window = Ui_Sbox()
        window.setupUi(self.dialog)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../收藏夹/iCloud Photos/Downloads/2019/IMG_0574.PNG"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        self.LnoEdit= window.Lnodit      #楼号编辑
        self.SnoEdit = window.SnoEdit  #宿舍号编辑
        self.L_nEdit = window.L_nEdit  #入住人数编辑
        self.C_nEdit = window.C_nEdit   #剩余空位编辑
        self.K_nEdit = window.K_nEdit   #可容纳数编辑
        self.LocationEdit = window.LocationEdit #位置编辑
        self.msgLabel = window.msg          #提示信息

        self.okButton = window.okButton
        self.cancelButton = window.cancelButton
        self.okButton.clicked.connect(self.onOkButtonClicked)
        self.cancelButton.clicked.connect(self.dialog.close)

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

    def applyToSushe(self, sushe):
        sushe.Lno = self.LnoEdit.text()
        sushe.Sno = self.SnoEdit.text()
        sushe.L_n = self.L_nEdit().text()
        sushe.C_n = self.C_nEdit.text()
        sushe.K_n = self.K_nEdit.text()
        sushe.Location = self.LocationEdit.text()

    def onFinished(self):
        return False


class EditBox(SBox):
    """编辑宿舍信息 - 继承SBox"""

    def __init__(self, sushe, callback):
        super(EditBox, self).__init__()
        self.callback = callback

        self.setTitle("修改信息...")
        self.setMsg("")
        self.setButton("修改")

        self.LnoEdit.setText(sushe.Lno)
        self.SnoEdit.setText(sushe.Sno)
        self.C_nEdit.setText(str(sushe.C_n))
        self.K_nEdit.setText(str(sushe.K_n))
        self.L_nEdit.setText(str(sushe.L_n))
        self.LocationEdit.setText(sushe.Location)

        self._sushe = Sushe()
    def show(self):
        self.LnoEdit.setEnabled(False)
        self.SnoEdit.setEnabled(False)
        self.LnoEdit.setClearButtonEnabled(False)
        self.SnoEdit.setClearButtonEnabled(False)
        self.dialog.show()

    def onFinished(self):
        self.applyToSushe(self._sushe)
        check, info = self._sushe.checkInfo()
        if check:
            self.callback(self._sushe)
        else:
            self.setMsg(info)
        return check


class NewBox(SBox):
    """新建宿舍档案 - 继承SBox"""

    def __init__(self, callback):
        super(NewBox, self).__init__()
        self.callback = callback

        self.setTitle("新建档案...")
        self.setMsg("")
        self.setButton("新建")

        self.sushe = Sushe()

    def onFinished(self):
        sushe = self.sushe
        self.applyToSushe(sushe)
        check, info = sushe.checkInfo(True)
        self.callback(self.sushe) if check else self.setMsg(info)
        return check


class SearchBox(SBox):
    """高级搜索框 - 继承SBox"""

    def __init__(self, callback):
        super(SearchBox, self).__init__()
        self.callback = callback

        self.setTitle("高级搜索...")
        self.setMsg("请输入检索关键词")
        self.setButton("搜索")

    def show(self):
        #self.MageEdit.setEnabled(False)
        #self.MageEdit.setClearButtonEnabled(False)
        self.dialog.show()

    def onFinished(self):
        keyList = [
            ("Lno", ' '.join(self.LnoEdit.text().split())),
            ("Sno", ' '.join(self.SnoEdit.text().split())),
            ("L_n", ' '.join(self.L_nEdit.text().split())),
            ("C_n", ' '.join(self.C_nEdit.text().split())),
            ("K_n", ' '.join(self.K_nEdit.text().split())),
            ("Location", ' '.join(self.LocationEdit.text().split())),
        ]
        self.callback(keyList)
        return True
