from PyQt5 import QtCore, QtWidgets, QtGui
import openpyxl


from db_API import Database as DB
from Data_window import DataWindow
from Doc_Window import DocWindow
from Scan_window import ScanWindow
from InsertWindow import InsertWindow, ChangeWindow
from Fizo_window import FizoWindow
import Tab_widgets2
import datetime


class MainTab(QtWidgets.QTabWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        
        self.db = parent.db

        if data:
            data = self.db.get_data(data)[0]
            person_id = data[0]

            person_w = Tab_widgets2.PersonWidget(self, data)
            document_w = Tab_widgets2.DocsWidget(self, person_id)
            family_w = Tab_widgets2.FamilyWidget(self, person_id)
            fizo_w = Tab_widgets2.FIZOWidget(self, person_id)


            self.addTab(person_w, 'Главная')
            self.addTab(document_w, 'Документы')
            self.addTab(family_w, 'Члены семьи')

            if data[12] == 'True':
                self.addTab(fizo_w, 'ФИЗО')            

        else:
            main_layout = QtWidgets.QVBoxLayout()
            logo_w = QtWidgets.QLabel('')
            pixmap = QtGui.QPixmap('./data/logo.png')
            logo_w.setPixmap(pixmap)
            logo_w.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
            main_layout.addWidget(logo_w)
            logo_label = QtWidgets.QLabel('<center>СПО учета личного состава</center>')
            logo_label.setStyleSheet('font-size: 24pt;font')
            main_layout.addWidget(logo_label)
            main_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            self.setLayout(main_layout)

        
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)
        
        self.db = DB(db)

        self.setStyleSheet('''
        QTabWidget{
            font-size: 14pt;
        }
        ''')
        
        self.tool_bar = QtWidgets.QToolBar()

        insert_profile = QtWidgets.QAction(QtGui.QIcon('./data/add.png'), 'Добавить', self)
        insert_profile.triggered.connect(self.insert)

        delete_profile = QtWidgets.QAction(QtGui.QIcon('./data/delete.png'), 'Удалить', self)
        delete_profile.triggered.connect(self.delete_profile)

        update_profile = QtWidgets.QAction(QtGui.QIcon('./data/edit.png'), 'Редактировать', self)
        update_profile.triggered.connect(self.change_data)

        add_scan = QtWidgets.QAction(QtGui.QIcon('./data/folder.png'), 'Прикрепить\nдокумент', self)
        add_scan.triggered.connect(self.add_scan)
        
        data_menu = QtWidgets.QAction(QtGui.QIcon('./data/addressbook.png'), 'Cловарь', self)
        data_menu.triggered.connect(self.data_change)

        fizo_menu = QtWidgets.QAction(QtGui.QIcon('./data/sport.png'), 'ФИЗО', self)
        fizo_menu.triggered.connect(self.fizo_open)
        
        im_export_menu = QtWidgets.QAction(QtGui.QIcon('./data/export.png'), 'Экспорт', self)
        im_export_menu.triggered.connect(self.export)

        docs_menu = QtWidgets.QAction(QtGui.QIcon('./data/data.png'), 'Формы\nдокументов', self)
        docs_menu.triggered.connect(self.create_documents)

        self.tool_bar.addAction(insert_profile)
        self.tool_bar.addAction(update_profile)
        self.tool_bar.addAction(add_scan)
        self.tool_bar.addAction(delete_profile)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(data_menu)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(docs_menu)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(fizo_menu)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(im_export_menu)
        
        self.tool_bar.setMovable(False)
        self.tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tool_bar.setIconSize(QtCore.QSize(50, 50))

        self.central_widget = QtWidgets.QWidget()
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.hbox = QtWidgets.QHBoxLayout()
        self.person_widget = MainTab(None, parent=self)

        self.list = QtWidgets.QListWidget()
        self.list_items = dict()
        persons = self.db.select("""
            SELECT 
            persons."ID",
            persons.second_name, 
            persons.first_name, 
            persons.patr
            FROM 
            persons
            ORDER BY
            persons.second_name ASC;
            """)
        if persons:
            for line in persons:
                if line[1] and line[2] and line[3]:
                    text = '{} {}.{}.'.format(line[1], line[2][0], line[3][0])
                self.list_items[text] = line[0]
                self.list.addItem(QtWidgets.QListWidgetItem(text))

        self.list.currentRowChanged.connect(self.row_changed)
        
        self.search_area = QtWidgets.QVBoxLayout()
        
        search_spec = QtWidgets.QGroupBox('Параметры поиска')

        self.current_check = QtWidgets.QCheckBox('Действующий')
        self.archive_check = QtWidgets.QCheckBox('Резерв')
        self.current_check.setChecked(True)
        self.h_slider = QtWidgets.QSlider()
        self.h_slider.setMaximum(1)
        self.h_slider.setPageStep(1)
        self.h_slider.setOrientation(QtCore.Qt.Horizontal)
        self.current_check.stateChanged.connect(self.search_spec_changed)
        self.archive_check.stateChanged.connect(self.search_spec_changed)
        self.h_slider.valueChanged.connect(self.search_spec_changed)
        
        chose_box = QtWidgets.QHBoxLayout()
        chose_box.addWidget(QtWidgets.QLabel('ГП ВС РФ'))
        chose_box.addWidget(self.h_slider)
        chose_box.addWidget(QtWidgets.QLabel('Военносл.'))
        
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.current_check)
        h_box.addWidget(self.archive_check)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(chose_box)
        v_box.addLayout(h_box)

        search_spec.setLayout(v_box)
        
        self.search_row = QtWidgets.QHBoxLayout()
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.textChanged.connect(self.find)
        self.search_btn = QtWidgets.QPushButton(QtGui.QIcon('./data/find.png'), '')
        self.search_btn.clicked.connect(self.find)
        self.search_row.addWidget(self.search_field)
        self.search_row.addWidget(self.search_btn)
        
        self.search_update_btn = QtWidgets.QPushButton(QtGui.QIcon('./data/refresh.png'), '')
        self.search_update_btn.clicked.connect(self.find)
        
        self.search_area.addWidget(search_spec)
        self.search_area.addLayout(self.search_row)
        self.search_area.addWidget(self.list)
        self.search_area.addWidget(self.search_update_btn)
        self.search_w = QtWidgets.QWidget()
        self.search_w.setLayout(self.search_area)
        self.search_w.setMaximumWidth(250)

        self.splitter.addWidget(self.search_w)
        self.splitter.addWidget(self.person_widget)
        #self.splitter.addWidget(self.scroll_area)
        self.hbox.addWidget(self.splitter)
        self.central_widget.setLayout(self.hbox)

        self.splitter.setHandleWidth(15)

        self.statusbar = QtWidgets.QStatusBar()

        self.setCentralWidget(self.central_widget)
        self.addToolBar(self.tool_bar)
        self.setStatusBar(self.statusbar)
        
        self.search_spec_query = ''
        self.search_spec_changed()
        
        self.h_slider.setValue(1)
        
    def search_spec_changed(self):
        self.search_spec_query = ''
        if self.h_slider.value() == 1:
            self.search_spec_query += "AND persons.mil = 'True' "
        else:
            self.search_spec_query += "AND persons.mil = 'False' "
        if self.current_check.isChecked() and not self.archive_check.isChecked():
            self.search_spec_query += "AND persons.active = 'True' "
        elif not self.current_check.isChecked() and self.archive_check.isChecked():
            self.search_spec_query += "AND persons.active = 'False' "
        elif not self.current_check.isChecked() and not self.archive_check.isChecked():
            self.search_spec_query += "AND persons.active = 'Null' "
        self.find()

        
    def row_changed(self):
        if self.list.currentItem():
            self.chose_person(self.list_items[self.list.currentItem().text()])
        
    def find(self):
        self.list.clear()
        self.list_items.clear()
        
        search = self.search_field.text().capitalize()
        
        query = """
        SELECT 
        persons."ID",
        persons.second_name, 
        persons.first_name, 
        persons.patr
        FROM 
        persons
        WHERE persons.second_name LIKE '{}%' {}
        ORDER BY
        persons.second_name ASC;        
        """.format(search, self.search_spec_query)  
        persons = self.db.select(query)     
        
        if persons:
            for line in persons:
                text = '{} {}.{}.'.format(line[1], line[2][0], line[3][0])
                self.list_items[text] = line[0]
                self.list.addItem(QtWidgets.QListWidgetItem(text))

    def insert(self):
        self.w = InsertWindow(self)
        self.w.setWindowTitle('Добавить')
        self.w.show()
        self.w.showMaximized()
        
    def change_data(self):
        if self.list.currentItem():
            data = self.db.get_data(self.list_items[self.list.currentItem().text()])[0]
            self.w = ChangeWindow(data, self)
            self.w.setWindowTitle('Редактировать')
            self.w.show()
            self.w.showMaximized()

    def delete_profile(self):
        if self.list.currentItem():
            data = self.db.get_data(self.list_items[self.list.currentItem().text()])[0]
            result = QtWidgets.QMessageBox.question(self,
                                                    'Удаление учетной записи',
                                                    'Удалить учетную запись {} {}.{}.?'.format(data[2], data[3][0], data[4][0]),
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                query = """
                DELETE FROM persons
                WHERE persons."ID" = '{}';
                """.format(data[0])
                self.db.execute(query)
                self.find()
                self.splitter.replaceWidget(1, MainTab(None, parent=self))

    def chose_person(self, idx):
        self.splitter.replaceWidget(1, MainTab(idx, parent=self))
        

    def data_change(self):
        self.w = DataWindow(self)
        self.w.setWindowTitle('Справочник')
        self.w.show()

    def fizo_open(self):
        self.w = FizoWindow(self)
        self.w.setWindowTitle('ФИЗО')
        self.w.show()
        
    def add_scan(self):
        if self.list.currentItem():
            data = self.db.get_data(self.list_items[self.list.currentItem().text()])[0][0]
            self.w = ScanWindow(data, self)
            self.w.setWindowTitle('Прикрепить документ')
            self.w.show()

    def create_documents(self):
        self.doc_w = DocWindow(self)
        self.doc_w.setWindowTitle('Документы')
        self.doc_w.show()

    def export(self):
        f = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить как', 'Сотрудники.xlsx')
        file_name = f[0]

        if file_name:
            wb = openpyxl.Workbook()
            wb.create_sheet('Персональные данные')
            sheet = wb['Персональные данные']
            query = f'''
            SELECT 
            persons.lnum, 
            persons.second_name, 
            persons.first_name, 
            persons.patr, 
            persons.person_buisness,
            persons.family_status,
            persons."rank",
            persons.division,
            persons.position,
            persons.order_by,
            persons.order_date,
            persons.place_of_birth, 
            persons.date_of_birth, 
            persons.gender, 
            persons.nation, 
            persons.phone_num1,
            persons.phone_num2,
            persons.address_reg,
            persons.address_living,
            persons.allowance_num,
            persons.allowance_by,
            persons.allowance_date,
            snils,
            inn,
            fizo_num,
            "ID"
            FROM persons
            WHERE persons.second_name LIKE '%' {self.search_spec_query}
            ORDER BY persons.second_name
            '''
            res = self.db.select(query)
            sheet.append(('Личный номер', 'ФИО', 'Фамилия', 'Имя', 'Отчество', 'Номер личного дела', 'Семейное положение', 'Звание', 'Подразделение',
                          'Должность', 'Приказ', 'Дата приказа',
                          'Место рождения', 'Дата рождения', 'Пол', 'Национальность',
                          'Телефон1', 'Телефон2', 'Адрес регистрации', 'Адрес проживания', 'Номер допуска', 'Кем допущен',
                          'Дата допуска', 'СНИЛС', 'ИНН', 'Номерок', 'Возрастная гр'))
            if res:
                for row in res:

                    years = datetime.datetime.now().year - row[12].year
                    if datetime.datetime.now().month < row[12].month:
                        years -= 1
                    elif datetime.datetime.now().month == row[12].month:
                        if datetime.datetime.now().day < row[12].day:
                            years -= 1

                    if years < 25:
                        group = '1'
                    elif years < 30:
                        group = '2'
                    elif years < 35:
                        group = '3'
                    elif years < 40:
                        group = '4'
                    elif years < 45:
                        group = '5'
                    elif years < 50:
                        group = '6'
                    elif years < 55:
                        group = '7'
                    else:
                        group = '8'

                    name = f'{row[1]} {row[2][0]}.{row[3][0]}.'
                    sheet.append((row[0], name,) + row[1:] + (group, ))

                wb.create_sheet('Классность')
                sheet = wb['Классность']
                for row in res:
                    idx = row[-1]
                    query = f'''
                    SELECT 
                    persons.lnum, 
                    persons.second_name, 
                    persons.first_name, 
                    persons.patr, 
                    class.level,
                    class.order_date,
                    class.order_by,
                    class.date_passing,
                    class.actual_from,
                    class.actual_to,
                    class.vus
                    FROM persons, class
                    WHERE persons.ID = class.PID AND
                    persons.ID = {idx}
                    ORDER BY class.order_date DESC
                    '''
                    res = self.db.select(query)
                    if res:
                        row = res[0]
                        sheet.append(row)

            wb.create_sheet('Документы')
            sheet = wb['Документы']
            query = '''
                    SELECT 
                    persons.lnum, 
                    persons.second_name, 
                    persons.first_name, 
                    persons.patr, 
                    documents."type",
                    documents.serial,
                    documents.num,
                    documents.given_by,
                    documents.code,
                    documents.doc_date
                    FROM persons, documents
                    WHERE persons.ID = documents.PID
                    ORDER BY persons.second_name
                    '''
            res = self.db.select(query)
            if res:
                for row in res:
                    sheet.append(row)

            wb.create_sheet('Члены семьи')
            sheet = wb['Члены семьи']
            query = '''
                    SELECT 
                    persons.lnum, 
                    persons.second_name, 
                    persons.first_name, 
                    persons.patr, 
                    family."type",
                    family.second_name,
                    family.first_name,
                    family.patr,
                    family.birthday
                    FROM persons, family
                    WHERE persons.ID = family.PID
                    ORDER BY persons.second_name
                    '''
            res = self.db.select(query)
            if res:
                for row in res:
                    sheet.append(row)

            wb.create_sheet('Ипотека')
            sheet = wb['Ипотека']
            query = '''
                SELECT 
                persons.lnum, 
                persons.second_name, 
                persons.first_name, 
                persons.patr, 
                ipoteka."user",
                ipoteka.finished,
                ipoteka.number,
                ipoteka.date_joining
                FROM persons, ipoteka
                WHERE persons.ID = ipoteka.PID
                ORDER BY persons.second_name
                '''
            res = self.db.select(query)
            if res:
                for row in res:
                    sheet.append(row)

            wb.create_sheet('Кредиты')
            sheet = wb['Кредиты']
            query = '''
                SELECT 
                persons.lnum, 
                persons.second_name, 
                persons.first_name, 
                persons.patr, 
                dolg.credit_org,
                dolg.credit_type,
                dolg.summ
                FROM persons, dolg
                WHERE persons.ID = dolg.PID
                ORDER BY persons.second_name
                '''
            res = self.db.select(query)
            if res:
                for row in res:
                    sheet.append(row)

            wb.create_sheet('Авто')
            sheet = wb['Авто']
            query = '''
                    SELECT 
                    persons.lnum, 
                    persons.second_name, 
                    persons.first_name, 
                    persons.patr, 
                    auto.model,
                    auto.gos_num,
                    auto.agency_name,
                    auto.agency_num,
                    auto.agency_from,
                    auto.agency_to
                    FROM persons, auto
                    WHERE persons.ID = auto.PID
                    ORDER BY persons.second_name
    
                    '''
            res = self.db.select(query)
            if res:
                for row in res:
                    sheet.append(row)

            wb.save(file_name)



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow('employees_center')
    window.resize(1200, 600)
    ico = QtGui.QIcon('./data.logo.png')
    window.setWindowTitle('СПО учёта личного состава')
    window.setWindowIcon(ico)
    window.showMaximized()
    window.show()
    
    app.setWindowIcon(ico)

    sys.exit(app.exec_())
    
    
