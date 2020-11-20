from mainUI import MainWindow
import sys
import public
from PyQt5 import QtWidgets
from student import StudentManager

if __name__ == "__main__":
    argv = sys.argv
    FILEPATH = argv[0]
    app = QtWidgets.QApplication(sys.argv)
    app.addLibraryPath(".")

    public.studentManager = StudentManager()

    public.mainDialog = MainWindow()
    public.mainDialog.show()

    sys.exit(app.exec_())
