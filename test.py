from PyQt5 import QtCore, QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.resize(1200, 600)
    window.setWindowTitle('Окно')
    window.show()

    ico = QtGui.QIcon('./logo.png')
    app.setWindowIcon(ico)

    sys.exit(app.exec_())
