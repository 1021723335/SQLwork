import sys
from UI import _mainUI
from UI import untitled
from UI import _Xbox
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = untitled.Ui_StudentBox()
    ui = _mainUI.Ui_MainWindow()
    #ui = _Xbox.Ui_Xbox()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())