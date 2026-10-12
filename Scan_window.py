from PyQt5 import QtCore, QtWidgets, QtGui
from db_API import Database as DB
import os


class ScanWindow(QtWidgets.QMainWindow):
    def __init__(self, pid, parent=None):
        super().__init__(parent=parent)
        
        db = parent.db
        self.db = db
        self.pid = pid
        self.parent = parent
        
        main_w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        self.name_edit = QtWidgets.QLineEdit()
        self.path_edit = QtWidgets.QLineEdit()
        search_btn = QtWidgets.QPushButton(QtGui.QIcon(r'.\data\folder.png'), '')
        search_btn.clicked.connect(self.open_doc)
        add_btn = QtWidgets.QPushButton('Добавить')
        add_btn.clicked.connect(self.add_doc)
        
        name_box = QtWidgets.QHBoxLayout()
        name_box.addWidget(QtWidgets.QLabel('Наименование: '))
        name_box.addWidget(self.name_edit)
        
        path_box = QtWidgets.QHBoxLayout()
        path_box.addWidget(QtWidgets.QLabel('Путь к файлу: '))
        path_box.addWidget(self.path_edit)
        path_box.addWidget(search_btn)
        
        layout.addLayout(name_box)
        layout.addLayout(path_box)
        layout.addWidget(add_btn)
        
        main_w.setLayout(layout)
        self.setCentralWidget(main_w)
        
    def open_doc(self):
        dialog = QtWidgets.QFileDialog(self, '', '', filter="Images (*.png *.jpg)")
        res = dialog.exec_()
        if res:
            file = dialog.selectedFiles()[0]
            self.path_edit.setText(file)
            
    def add_doc(self):
        if self.name_edit.text() != '':
            if self.path_edit.text() != '':
                file = self.path_edit.text()
                if os.path.exists(file):
                    with open(file, 'rb') as f:
                        data = f.read()
                    query = """
                    INSERT INTO scans(
                    "PID", name, scan)
                    VALUES ({}, '{}', ?);
                    """.format(self.pid, self.name_edit.text())
                    self.db.execute_n(query, (data,))
                    w = QtWidgets.QMessageBox.information(self, 'Сообщение', 'Приложение добавлено', defaultButton=QtWidgets.QMessageBox.Ok)
                    self.parent.find()
                else:
                    self.error('Файл не существует')
            else:
                self.error('Укажите путь к файлу')
        else:
            self.error('Укажите наименование документа')
                
            
    def error(self, text):
        w = QtWidgets.QMessageBox.critical(self, 'Ошибка!', text, defaultButton=QtWidgets.QMessageBox.Ok)
        


