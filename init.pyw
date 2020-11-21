from mainUI import MainWindow
import sys
import public
from PyQt5 import QtWidgets
from Control.student import StudentManager
from Control.manager import MManager

if __name__ == "__main__":
    argv = sys.argv
    FILEPATH = argv[0]
    app = QtWidgets.QApplication(sys.argv)
    app.addLibraryPath(".")

    public.studentManager = StudentManager()
    public.suguangManager = MManager()

    public.mainDialog = MainWindow()
    public.mainDialog.show()

    sys.exit(app.exec_())
