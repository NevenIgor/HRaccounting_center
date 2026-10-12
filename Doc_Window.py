from PyQt5 import QtCore, QtWidgets, QtGui
import os

from db_API import Database as DB
import doc_API as Doc

class DocWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        db = parent.db
        self.db = db
        
        w = QtWidgets.QWidget()
        self.h_layout = QtWidgets.QHBoxLayout()
        self.v_layout = QtWidgets.QVBoxLayout()
        find_layout = QtWidgets.QHBoxLayout()
        
        self.template_list = QtWidgets.QListWidget()
        self.person_list = QtWidgets.QListWidget()
        self.template_list.clicked.connect(self.person_chose)
        self.person_list.clicked.connect(self.person_chose)
        self.list_items = {}
        
        self.find_edit = QtWidgets.QLineEdit()
        self.chosed_edit = QtWidgets.QTextEdit()
        self.generate_btn = QtWidgets.QPushButton('Сгенерировать')
        
        self.generate_btn.clicked.connect(self.generate)        
        self.find_edit.textChanged.connect(self.find)
        
        self.template_list.setSelectionMode(2)
        self.person_list.setSelectionMode(2)

        
        find_layout.addWidget(QtWidgets.QLabel('Поиск:'))
        find_layout.addWidget(self.find_edit)
        self.h_layout.addWidget(self.template_list)
        self.h_layout.addWidget(self.person_list)
        
        self.v_layout.addLayout(find_layout)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.chosed_edit)
        self.v_layout.addWidget(self.generate_btn)
        
        w.setLayout(self.v_layout)
        self.setCentralWidget(w)
        
        for root, dirs, files in os.walk('templates'):
            for file in files:
                self.template_list.addItem(QtWidgets.QListWidgetItem(file))
        
        self.find()
        
        self.resize(900, 600)
        
    def person_chose(self):
        self.chosed_edit.clear()
        self.chosed_edit.append('Сотрудники: ')
        for index in self.person_list.selectedIndexes():
            self.chosed_edit.insertPlainText(index.data() + ', ')
        self.chosed_edit.append('\nДокументы: ')
        for index in self.template_list.selectedIndexes():
            self.chosed_edit.insertPlainText(index.data() + ', ')
        
    def find(self):
        self.person_list.clear()
        self.list_items.clear()
        
        search = self.find_edit.text().capitalize()
        
        query = """
        SELECT 
        lnum, second_name, first_name, patr
        FROM 
        persons
        WHERE second_name LIKE '{}%'
        ORDER BY
        second_name ASC;
        """.format(search)  
        persons = self.db.select(query)     
        
        if persons:
            for line in persons:
                text = '{} {}.{}.'.format(line[1], line[2][0], line[3][0])
                self.list_items[text] = line[0]
                self.person_list.addItem(QtWidgets.QListWidgetItem(text))
                
    def generate(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(parent=self, directory=os.environ.get('HOME', ''))
        for template in self.template_list.selectedIndexes():
            for person in self.person_list.selectedIndexes():
                Doc.generate(directory, template.data(), self.list_items[person.data()])



