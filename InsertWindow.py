import threading

from PyQt5 import QtCore, QtWidgets, QtGui
import time
import os

from db_API import Database as DB


def f_date(date):
    dates = date.split('.')
    new_date = '-'.join(dates[::-1])
    return new_date

class UpdateWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setStyleSheet(''' 
        QLabel{
            font-size: 14pt;
        }
        
        QPushButton{
            font-size: 14pt;
        }
        
        QLineEdit{
            font-size: 14pt;
        }
        
        QTableWidget{
            font-size: 14pt;
        }
        
        QComboBox{
            font-size: 14pt;
        }
        
        QTabWidget{
            font-size: 14pt;
        }
        
        QCheckBox{
            font-size: 14pt;
        }
        
        QDateEdit{
            font-size: 14pt;
        }''')
        

        self.parent = parent
        
        self.pid = None

        self.db = self.parent.db

        central_w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget()

        self.nex_btn = QtWidgets.QPushButton('Сохранить')

        layout.addWidget(self.nex_btn)
        layout.addWidget(self.tab_widget)

        central_w.setLayout(layout)
        
        self.date_format = "%d.%m.%Y"

        # ==================================== Персональные данные ===========================

        self.person_data = QtWidgets.QWidget()

        img_l = QtWidgets.QVBoxLayout()
        self.img_label = QtWidgets.QLabel('')
        self.img_label.setStyleSheet('border: 1px solid #333')
        self.add_img_btn = QtWidgets.QPushButton('Выбрать фото')
        self.add_img_btn.clicked.connect(self.set_img)
        self.img_label.setAlignment(QtCore.Qt.AlignCenter)
        img_l.addWidget(self.img_label)
        img_l.addWidget(self.add_img_btn)

        self.labels = dict()
        self.labels['surname'] = QtWidgets.QLineEdit()
        self.labels['name'] = QtWidgets.QLineEdit()
        self.labels['patr'] = QtWidgets.QLineEdit()
        self.labels['number'] = QtWidgets.QLineEdit()
        self.labels['number'].setMaxLength(10)
        self.labels['rank'] = QtWidgets.QLineEdit()
        self.labels['buisness'] = QtWidgets.QLineEdit()
        self.labels['snils'] = QtWidgets.QLineEdit()
        self.labels['inn'] = QtWidgets.QLineEdit()
        self.labels['birthday_date'] = QtWidgets.QDateEdit()
        self.labels['birthday_date'].setCalendarPopup(True)
        self.labels['place_of_birth'] = QtWidgets.QLineEdit()
        self.labels['nation'] = QtWidgets.QLineEdit()
        self.labels['gender'] = QtWidgets.QComboBox()
        self.labels['family_status'] = QtWidgets.QComboBox()
        self.labels['mobile_number'] = QtWidgets.QLineEdit()
        self.labels['mobile_number1'] = QtWidgets.QLineEdit()
        self.labels['status'] = QtWidgets.QComboBox()
        self.labels['status'].addItem('Военнослужащий', True)
        self.labels['status'].addItem('ГП ВС РФ', False)
        self.labels['status'].currentIndexChanged.connect(self.change_type)
        self.labels['status1'] = QtWidgets.QComboBox()
        self.labels['status1'].addItem('Действующий', True)
        self.labels['status1'].addItem('Резерв', False)
        self.labels['position'] = QtWidgets.QComboBox()
        self.labels['division'] = QtWidgets.QComboBox()
        self.labels['order'] = QtWidgets.QLineEdit()
        self.labels['order_date'] = QtWidgets.QDateEdit()
        self.labels['order_date'].setCalendarPopup(True)
        self.labels['allowance'] = QtWidgets.QLineEdit()
        self.labels['allowance_by'] = QtWidgets.QLineEdit()
        self.labels['allowance_date'] = QtWidgets.QDateEdit()
        self.labels['allowance_date'].setCalendarPopup(True)
        self.labels['reg_addr'] = QtWidgets.QLineEdit()
        self.labels['liv_addr'] = QtWidgets.QLineEdit()
        self.labels['gender'].currentIndexChanged.connect(self.change_sp)
        self.labels['gender'].addItem('М')
        self.labels['gender'].addItem('Ж')
        self.labels['fizo_num'] = QtWidgets.QLineEdit()
        # вид финансового обеспечения — из словаря
        self.labels['financing'] = QtWidgets.QComboBox()
        self._load_financing()
        
        form1 = QtWidgets.QFormLayout()
        form1.addRow('Фамилия:', self.labels['surname'])
        form1.addRow('Имя:', self.labels['name'])
        form1.addRow('Отчество:', self.labels['patr'])
        form1.addRow('Пол:', self.labels['gender'])
        form1.addRow('Национальность:', self.labels['nation'])
        form1.addRow('Дата рождения:', self.labels['birthday_date'])
        form1.addRow('Место рождения:', self.labels['place_of_birth'])
        form1.addRow('Семейное положение:', self.labels['family_status'])
        form1.addRow('Адрес регистрации:', self.labels['reg_addr'])
        form1.addRow('Адрес проживания:', self.labels['liv_addr'])
        form1.addRow('Номер телефона:', self.labels['mobile_number'])
        form1.addRow('Доп. номер:', self.labels['mobile_number1'])
        form1.addRow('СНИЛС:', self.labels['snils'])
        form1.addRow('ИНН:', self.labels['inn'])

        form3 = QtWidgets.QFormLayout()
        form3.addRow('Принадлежность к ВС:', self.labels['status'])
        form3.addRow('Личный номер:', self.labels['number'])
        form3.addRow('Номер личного дела:', self.labels['buisness'])
        form3.addRow('Звание:', self.labels['rank'])
        form3.addRow('Статус:', self.labels['status1'])
        form3.addRow('Подразделение:', self.labels['division'])
        form3.addRow('Должность:', self.labels['position'])
        form3.addRow('Приказ о назначении:', self.labels['order'])
        form3.addRow('Дата приказа:', self.labels['order_date'])
        form3.addRow('Номер допуска:', self.labels['allowance'])
        form3.addRow('Допуск выдан:', self.labels['allowance_by'])
        form3.addRow('Дата выдачи:', self.labels['allowance_date'])
        form3.addRow('Номерок ФИЗО:', self.labels['fizo_num'])
        form3.addRow('Финансовое обеспечение:', self.labels['financing'])

        first_level = QtWidgets.QHBoxLayout()
        first_level.addLayout(img_l)
        first_level.addLayout(form1)
        first_level.addLayout(form3)
        first_level.setAlignment(QtCore.Qt.AlignCenter)
        self.person_data.setLayout(first_level)
        
        query = """
        SELECT 
        positions.name_full
        FROM 
        positions
        ORDER BY
        positions.name_full ASC;
        """
        res = self.db.select(query)
        if res:
            for row in res:
                self.labels['position'].addItem(row[0])
                
        query = """
        SELECT 
        divisions.name_full
        FROM 
        divisions
        ORDER BY
        divisions.name_full ASC;
        """
        res = self.db.select(query)
        if res:
            for row in res:
                self.labels['division'].addItem(row[0])

        
        #======================================== Классность ====================================
        
        
        self.class_widget = QtWidgets.QWidget()
        self.class_l = QtWidgets.QVBoxLayout()
        self.class_person_l = QtWidgets.QGridLayout()
        
        labels = []
        labels.append(QtWidgets.QLabel('Классность'))
        labels.append(QtWidgets.QLabel('Дата сдачи'))
        labels.append(QtWidgets.QLabel('Приказ'))
        labels.append(QtWidgets.QLabel('Дата приказа'))
        labels.append(QtWidgets.QLabel('ВУС'))
        labels.append(QtWidgets.QLabel('Действительна с'))
        labels.append(QtWidgets.QLabel('Действительна по'))
        
        for idx, label in enumerate(labels):
            label.setAlignment(QtCore.Qt.AlignHCenter)
            self.class_person_l.addWidget(label, 0, idx)
        
        self.class_type_edit = QtWidgets.QComboBox()
        self.class_type_edit.addItem('спец. 3 класса')
        self.class_type_edit.addItem('спец. 2 класса')
        self.class_type_edit.addItem('спец. 1 класса')
        self.class_type_edit.addItem('Мастер')
        self.class_date_passing_edit = QtWidgets.QDateEdit()
        self.class_date_passing_edit.setCalendarPopup(True)
        self.class_order_edit = QtWidgets.QLineEdit()
        self.class_order_from_edit = QtWidgets.QDateEdit()
        self.class_order_from_edit.setCalendarPopup(True)
        self.class_actual_from = QtWidgets.QDateEdit()
        self.class_actual_from.setCalendarPopup(True)
        self.class_actual_to = QtWidgets.QDateEdit()
        self.class_actual_to.setCalendarPopup(True)
        self.class_vus_edit = QtWidgets.QLineEdit()

        self.class_person_l.addWidget(self.class_type_edit, 1, 0)
        self.class_person_l.addWidget(self.class_date_passing_edit, 1, 1)
        self.class_person_l.addWidget(self.class_order_edit, 1, 2)
        self.class_person_l.addWidget(self.class_order_from_edit, 1, 3)
        self.class_person_l.addWidget(self.class_vus_edit, 1, 4)
        self.class_person_l.addWidget(self.class_actual_from, 1, 5)
        self.class_person_l.addWidget(self.class_actual_to, 1, 6)
        
        self.class_add_btn = QtWidgets.QPushButton(QtGui.QIcon(r'.\data\add.png'), '')
        self.class_add_btn.clicked.connect(self.add_class)
        self.class_person_l.addWidget(self.class_add_btn, 0, 7, 2, 1)
        
        self.class_table = Table(0,7, 0)
        self.class_table.setHorizontalHeaderLabels(('Классность', 'Дата сдачи', 'Приказ', 'Дата приказа', 'ВУС', 'Актуально с', 'Актуально по'))
        self.class_table.signal.connect(self.update_class)
        
        self.class_l.addLayout(self.class_person_l)
        self.class_l.addWidget(self.class_table)
        
        self.class_widget.setLayout(self.class_l)
        
        
        
        #======================================== ФИЗО ====================================
        
        
        self.fizo_widget = QtWidgets.QWidget()
        self.fizo_l = QtWidgets.QVBoxLayout()
        self.fizo_person_l = QtWidgets.QFormLayout()
        
        self.fizo_type_edit = QtWidgets.QComboBox()
        self.fizo_type_edit.addItem('Нет')
        self.fizo_type_edit.addItem('ВКУ')
        self.fizo_type_edit.addItem('1 КУ')
        self.fizo_type_edit.addItem('2 КУ')
        self.fizo_type_edit.addItem('3 КУ')
        self.fizo_type_edit.addItem('4')
        self.fizo_type_edit.addItem('3')
        self.fizo_type_edit.addItem('2')
        self.fizo_type_edit.addItem('ЛФК')
        self.fizo_rank_edit = QtWidgets.QComboBox()
        self.fizo_rank_edit.addItem('Нет')
        self.fizo_rank_edit.addItem('МС')
        self.fizo_rank_edit.addItem('КМС')
        self.fizo_rank_edit.addItem('1 Взрослый')
        self.fizo_rank_edit.addItem('2 Взрослый')
        self.fizo_rank_edit.addItem('3 Взрослый')
        self.fizo_rank_edit.addItem('1 Юношеский')
        self.fizo_rank_edit.addItem('2 Юношеский')
        self.fizo_rank_edit.addItem('3 Юношеский')

        self.fizo_add_btn = QtWidgets.QPushButton('Сохранить')
        self.fizo_add_btn.clicked.connect(self.add_fizo)

        self.fizo_person_l.addRow('Категория', self.fizo_type_edit)
        self.fizo_person_l.addRow('Разряд', self.fizo_rank_edit)

        self.fizo_l.addLayout(self.fizo_person_l)
        #self.fizo_l.addWidget(self.fizo_add_btn)
        
        self.fizo_widget.setLayout(self.fizo_l)
        
        
        #======================================== Документы ====================================
        
        
        self.doc_widget = QtWidgets.QWidget()
        self.doc_l = QtWidgets.QVBoxLayout()
        self.doc_person_l = QtWidgets.QGridLayout()
        
        labels = []
        labels.append(QtWidgets.QLabel('Тип документа'))
        labels.append(QtWidgets.QLabel('Член семьи'))
        labels.append(QtWidgets.QLabel('Серия'))
        labels.append(QtWidgets.QLabel('Номер'))
        labels.append(QtWidgets.QLabel('Кем выдан'))
        labels.append(QtWidgets.QLabel('Код подразделения'))
        labels.append(QtWidgets.QLabel('Дата выдачи'))
        
        for idx, label in enumerate(labels):
            label.setAlignment(QtCore.Qt.AlignHCenter)
            self.doc_person_l.addWidget(label, 0, idx)
        
        self.doc_type_edit = QtWidgets.QComboBox()
        self.doc_person_edit = QtWidgets.QComboBox()
        self.doc_type_edit.addItems(('Паспорт', 'Удостоверение', 'Свидетельство о рождении', 'Свид-во о заключении брака', 'Загран. паспорт', 'Водительское удостоверение'))
        self.doc_serial_edit = QtWidgets.QLineEdit()
        self.doc_numberl_edit = QtWidgets.QLineEdit()
        self.doc_given_by_edit = QtWidgets.QLineEdit()
        self.doc_gby_cod = QtWidgets.QLineEdit()
        self.doc_from_edit = QtWidgets.QDateEdit()
        self.doc_from_edit.setCalendarPopup(True)

        self.doc_person_l.addWidget(self.doc_type_edit, 1, 0)
        self.doc_person_l.addWidget(self.doc_person_edit, 1, 1)
        self.doc_person_l.addWidget(self.doc_serial_edit, 1, 2)
        self.doc_person_l.addWidget(self.doc_numberl_edit, 1, 3)
        self.doc_person_l.addWidget(self.doc_given_by_edit, 1, 4)
        self.doc_person_l.addWidget(self.doc_gby_cod, 1, 5)
        self.doc_person_l.addWidget(self.doc_from_edit, 1, 6)
        
        self.doc_add_btn = QtWidgets.QPushButton(QtGui.QIcon(r'.\data\add.png'), '')
        self.doc_add_btn.clicked.connect(self.add_doc)
        self.doc_person_l.addWidget(self.doc_add_btn, 0, 7, 2, 1)
        
        self.doc_table = Table(0,7, 1)
        self.doc_table.setHorizontalHeaderLabels(('Тип документа', 'Член семьи', 'Серия', 'Номер', 'Кем выдан', 'Код подразделения', 'Дата выдачи'))
        self.doc_table.signal.connect(self.update_docs)
        
        self.doc_l.addLayout(self.doc_person_l)
        self.doc_l.addWidget(self.doc_table)
        
        self.doc_widget.setLayout(self.doc_l)

        #==================================      Тачки          ===================================

        self.auto_widget = QtWidgets.QWidget()
        self.auto_l = QtWidgets.QVBoxLayout()
        self.auto_person_l = QtWidgets.QGridLayout()

        labels = []
        labels.append(QtWidgets.QLabel('Марка'))
        labels.append(QtWidgets.QLabel('Модель'))
        labels.append(QtWidgets.QLabel('Гос. номер'))
        labels.append(QtWidgets.QLabel('Цвет'))

        for idx, label in enumerate(labels):
            label.setAlignment(QtCore.Qt.AlignHCenter)
            self.auto_person_l.addWidget(label, 0, idx)

        self.auto_brand_edit = QtWidgets.QLineEdit()
        self.auto_model_edit = QtWidgets.QLineEdit()
        self.auto_gos_num_edit = QtWidgets.QLineEdit()
        self.auto_color_edit = QtWidgets.QLineEdit()

        self.auto_person_l.addWidget(self.auto_brand_edit, 1, 0)
        self.auto_person_l.addWidget(self.auto_model_edit, 1, 1)
        self.auto_person_l.addWidget(self.auto_gos_num_edit, 1, 2)
        self.auto_person_l.addWidget(self.auto_color_edit, 1, 3)


        self.auto_add_btn = QtWidgets.QPushButton(QtGui.QIcon(r'.\data\add.png'), '')
        self.auto_add_btn.clicked.connect(self.add_auto)
        self.auto_person_l.addWidget(self.auto_add_btn, 0, 6, 2, 1)

        self.auto_table = Table(0, 4, 2)
        self.auto_table.setHorizontalHeaderLabels(
            ('Марка', 'Модель', 'Гос. номер', 'Цвет'))
        self.auto_table.signal.connect(self.update_auto)

        self.auto_l.addLayout(self.auto_person_l)
        self.auto_l.addWidget(self.auto_table)

        self.auto_widget.setLayout(self.auto_l)


        #================================== Ипотека ===========================================

        self.nis_widget = QtWidgets.QWidget()
        self.nis_l = QtWidgets.QVBoxLayout()
        form = QtWidgets.QFormLayout()

        self.nis_user = QtWidgets.QCheckBox('Участник НИС')
        self.nis_user.stateChanged.connect(self.change_nis)
        self.nis_finished = QtWidgets.QComboBox()
        self.nis_finished.addItem('Да', True)
        self.nis_finished.addItem('Нет', False)
        self.nis_number = QtWidgets.QLineEdit()
        self.nis_date = QtWidgets.QDateEdit()
        self.nis_date.setCalendarPopup(True)
        self.nis_add = QtWidgets.QPushButton('Сохранить')
        self.nis_add.clicked.connect(self.add_nis)

        form.addRow('Реализовал ипотеку', self.nis_finished)
        form.addRow('Номер НИС', self.nis_number)
        form.addRow('Дата включения', self.nis_date)

        self.nis_l.addWidget(self.nis_user)
        self.nis_l.addLayout(form)
        #self.nis_l.addWidget(self.nis_add)

        self.nis_widget.setLayout(self.nis_l)

        self.nis_date.setEnabled(False)
        self.nis_number.setEnabled(False)
        self.nis_finished.setEnabled(False)

        #===================================    Льготы       =================================

        self.lgot_widget = QtWidgets.QWidget()

        self.lgot_l = QtWidgets.QVBoxLayout()
        self.lgot_w = {}
        query = """
        SELECT * FROM lgoty
        """
        res = self.db.select(query)
        if res:
            for row in res:
                self.lgot_w[row[0]] = QtWidgets.QCheckBox(row[1])

        self.lgot_add = QtWidgets.QPushButton('Сохранить')
        self.lgot_add.clicked.connect(self.add_lgot)

        for key in self.lgot_w.keys():
            self.lgot_l.addWidget(self.lgot_w[key])

        #self.lgot_l.addWidget(self.lgot_add)
        self.lgot_widget.setLayout(self.lgot_l)

        # ================================== Долги ===========================================

        self.dolg_widget = QtWidgets.QWidget()
        self.dolg_l = QtWidgets.QVBoxLayout()
        form = QtWidgets.QFormLayout()

        query = """
        SELECT name, "ID" FROM credit_types
        """
        res = self.db.select(query)

        self.dolg_exist = QtWidgets.QComboBox()
        self.dolg_exist.addItem('Да', True)
        self.dolg_exist.addItem('Нет', False)
        self.dolg_exist.currentIndexChanged.connect(self.change_dolg)
        self.dolg_type = QtWidgets.QComboBox()
        if res:
            for row in res:
                self.dolg_type.addItem(row[0], row[1])
        self.dolg_org = QtWidgets.QLineEdit()
        self.dolg_summ = QtWidgets.QLineEdit()
        self.dolg_add = QtWidgets.QPushButton('Сохранить')
        self.dolg_add.clicked.connect(self.add_dolg)

        form.addRow('Наличие долгов', self.dolg_exist)
        form.addRow('Тип кредитной задолжности', self.dolg_type)
        form.addRow('Кредитная организация', self.dolg_org)
        form.addRow('Сумма долга', self.dolg_summ)

        self.dolg_l.addLayout(form)
        #self.dolg_l.addWidget(self.dolg_add)

        self.dolg_widget.setLayout(self.dolg_l)

        #===================================       Члены семьи     ===========================
        
        
        self.family_widget = QtWidgets.QWidget()
        self.family_l = QtWidgets.QVBoxLayout()
        self.family_person_l = QtWidgets.QGridLayout()
        
        labels = []
        labels.append(QtWidgets.QLabel('Степень родства'))
        labels.append(QtWidgets.QLabel('Фамилия'))
        labels.append(QtWidgets.QLabel('Имя'))
        labels.append(QtWidgets.QLabel('Отчество'))
        labels.append(QtWidgets.QLabel('Дата рождения'))
        
        for idx, label in enumerate(labels):
            label.setAlignment(QtCore.Qt.AlignHCenter)
            self.family_person_l.addWidget(label, 0, idx)
        
        self.family_type_edit = QtWidgets.QComboBox()
        self.family_type_edit.addItems(('Жена', 'Муж', 'Сын', 'Дочь'))
        self.family_family_edit = QtWidgets.QLineEdit()
        self.family_name_edit = QtWidgets.QLineEdit()
        self.family_patr_edit = QtWidgets.QLineEdit()
        self.family_birthday_edit = QtWidgets.QDateEdit()
        self.family_birthday_edit.setCalendarPopup(True)

        self.family_person_l.addWidget(self.family_type_edit, 1, 0)
        self.family_person_l.addWidget(self.family_family_edit, 1, 1)
        self.family_person_l.addWidget(self.family_name_edit, 1, 2)
        self.family_person_l.addWidget(self.family_patr_edit, 1, 3)
        self.family_person_l.addWidget(self.family_birthday_edit, 1, 4)
        
        self.family_add_btn = QtWidgets.QPushButton(QtGui.QIcon(r'.\data\add.png'), '')
        self.family_add_btn.clicked.connect(self.add_family)
        self.family_person_l.addWidget(self.family_add_btn, 0, 5, 2, 1)
        
        self.family_table = Table(0,5, 3)
        self.family_table.setHorizontalHeaderLabels(('Степень родства', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения'))
        self.family_table.signal.connect(self.update_family)
        
        self.family_l.addLayout(self.family_person_l)
        self.family_l.addWidget(self.family_table)
        
        self.family_widget.setLayout(self.family_l)
        

        
        #====================================       =========     ===========================

        self.tab_widget.addTab(self.person_data, 'Персональные данные')
        self.tab_widget.addTab(self.doc_widget, 'Документы')
        self.tab_widget.addTab(self.family_widget, 'Члены семьи')
        self.tab_widget.addTab(self.fizo_widget, 'ФИЗО')
        self.tab_widget.addTab(self.class_widget, 'Классная квалификация')
        self.tab_widget.addTab(self.nis_widget, 'НИС')
        self.tab_widget.addTab(self.lgot_widget, 'Льготы')
        self.tab_widget.addTab(self.dolg_widget, 'Долги')
        self.tab_widget.addTab(self.auto_widget, 'Авто')

        self.setCentralWidget(central_w)
        
        self.exit_text = 'Вы уверенны что хотите выйти?<br>Все несохраненные данные будут утеряны'

        self.nex_btn.clicked.connect(self.person_ID_changed)

        self.move(0, 0)

    def full_save(self):
        self.add_dolg()
        self.add_lgot()
        self.add_nis()
        #self.add_auto()
        #self.add_class()
        self.add_fizo()

        for i in range(self.doc_table.rowCount()):
            print(self.doc_table.columnCount())

            query = """UPDATE documents SET type = ?,
            name = ?,
            serial = ?,
            num = ?,
            given_by = ?,
            code = ?,
            doc_date = ?
            WHERE "ID" = {}""".format(self.doc_table.id_list[i])
            self.db.execute_n(query, (self.doc_table.item(i, 0).text(),
                                      self.doc_table.item(i, 1).text(),
                                      self.doc_table.item(i, 2).text(),
                                      self.doc_table.item(i, 3).text(),
                                      self.doc_table.item(i, 4).text(),
                                      self.doc_table.item(i, 5).text(),
                                      f_date(self.doc_table.item(i, 6).text()),
                                      #
                                      ))

        for i in range(self.family_table.rowCount()):

            query = """UPDATE family SET type = ?,
            second_name = ?,
            first_name = ?,
            patr = ?,
            birthday = ?
            WHERE "ID" = {}""".format(self.family_table.id_list[i])
            self.db.execute_n(query, (self.family_table.item(i, 0).text(),
                                      self.family_table.item(i, 1).text(),
                                      self.family_table.item(i, 2).text(),
                                      self.family_table.item(i, 3).text(),
                                      f_date(self.family_table.item(i, 4).text()),))

        for i in range(self.auto_table.rowCount()):

            query = """UPDATE auto SET brand = ?,
            model = ?,
            gos_num = ?,
            color = ?
            WHERE "ID" = {}""".format(self.auto_table.id_list[i])
            self.db.execute_n(query, (self.auto_table.item(i, 0).text(),
                                      self.auto_table.item(i, 1).text(),
                                      self.auto_table.item(i, 2).text(),
                                      self.auto_table.item(i, 3).text(),))

        for i in range(self.class_table.rowCount()):

            query = """UPDATE class SET level = ?,
            order_date = ?,
            order_by = ?,
            date_passing = ?,
            actual_from = ?,
            actual_to = ?,
            vus = ?
            WHERE "ID" = {}""".format(self.class_table.id_list[i])
            self.db.execute_n(query, (self.class_table.item(i, 0).text(),
                                      f_date(self.class_table.item(i, 3).text()),
                                      self.class_table.item(i, 2).text(),
                                      f_date(self.class_table.item(i, 1).text()),
                                      f_date(self.class_table.item(i, 5).text()),
                                      f_date(self.class_table.item(i, 6).text()),
                                      self.class_table.item(i, 4).text(),))



    def change_dolg(self):
        enabled = self.dolg_exist.itemData(self.dolg_exist.currentIndex())
        self.dolg_org.setEnabled(enabled)
        self.dolg_summ.setEnabled(enabled)
        self.dolg_type.setEnabled(enabled)

    def change_nis(self):
        enabled = self.nis_user.isChecked()
        self.nis_date.setEnabled(enabled)
        self.nis_number.setEnabled(enabled)
        self.nis_finished.setEnabled(enabled)
                
    def change_sp(self):
        self.labels['family_status'].clear()
        gender = self.labels['gender'].currentText()
        query = """
        SELECT 
        family_status."ID", 
        family_status.name
        FROM 
        family_status
        WHERE 
        family_status.gender = '{}'
        ORDER BY
        family_status.name ASC;
        """.format(gender)
        print(query)
        
        result = self.db.select(query)
        if result:
            for row in result:
                self.labels['family_status'].addItem(row[1], row[0])

    def change_type(self):
        mil = self.labels['status'].itemData(self.labels['status'].currentIndex())
        self.labels['number'].setEnabled(mil)
        self.labels['rank'].setEnabled(mil)
        self.labels['buisness'].setEnabled(mil)
        self.tab_widget.setTabEnabled(3, mil)
        self.tab_widget.setTabEnabled(4, mil)
        self.tab_widget.setTabEnabled(5, mil)
        self.tab_widget.setTabEnabled(6, mil)
        
    def person_ID_changed(self):
        pass

    def _load_financing(self, selected_id=None):
        """Заполняет комбобокс 'Финансовое обеспечение' из словаря."""
        combo = self.labels['financing']
        combo.blockSignals(True)
        combo.clear()
        combo.addItem('—', None)
        res = self.db.select('SELECT "ID", name FROM financing ORDER BY name ASC;')
        if res:
            for row in res:
                combo.addItem(row[1], row[0])
        idx = 0
        if selected_id is not None:
            for i in range(combo.count()):
                if combo.itemData(i) == int(selected_id):
                    idx = i
                    break
        combo.setCurrentIndex(idx)
        combo.blockSignals(False)

    def currentFinancingId(self):
        data = self.labels['financing'].itemData(self.labels['financing'].currentIndex())
        return 'NULL' if data is None else "'{}'".format(data)

    def set_img(self):
        dialog = QtWidgets.QFileDialog(self, '', '', filter="Images (*.png *.jpg)")
        res = dialog.exec_()
        if res:
            file = dialog.selectedFiles()[0]
            if os.path.exists(file):
                with open(file, 'rb') as f:
                    data = f.read()
                query = """
                UPDATE persons
                SET photo=?
                WHERE "ID" = '{}'
                """.format(self.pid)
                self.db.execute_n(query, (data, ))
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                pixmap = pixmap.scaled(150, self.img_label.height(), QtCore.Qt.KeepAspectRatio)
                self.img_label.setPixmap(pixmap)

    def add_doc(self):
        typ = self.doc_type_edit.currentText()
        person = self.doc_person_edit.currentText()
        serial = self.doc_serial_edit.text()
        number = self.doc_numberl_edit.text()
        giv_by = self.doc_given_by_edit.text()
        cod = self.doc_gby_cod.text()
        date = self.doc_from_edit.dateTime().toPyDateTime().date()

        query = """
        INSERT INTO documents("PID", type, name, serial, num, given_by, code, doc_date)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(self.pid, typ, person, serial, number, giv_by, cod, date)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

        self.doc_table.insertRow(self.doc_table.rowCount())
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(typ))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(person))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(serial))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(number))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 4, QtWidgets.QTableWidgetItem(giv_by))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 5, QtWidgets.QTableWidgetItem(cod))
        self.doc_table.setItem(self.doc_table.rowCount() - 1, 6, QtWidgets.QTableWidgetItem(self.doc_from_edit.text()))

        query = """SELECT "ID" FROM documents"""
        self.doc_table.id_list.append(self.db.select(query)[-1][0])

    def add_class(self):
        class_typ = self.class_type_edit.currentText()
        date_pass = self.class_date_passing_edit.dateTime().toPyDateTime().date()
        order = self.class_order_edit.text()
        order_from = self.class_order_from_edit.dateTime().toPyDateTime().date()
        actual_from = self.class_actual_from.dateTime().toPyDateTime().date()
        actual_to = self.class_actual_to.dateTime().toPyDateTime().date()
        vus = self.class_vus_edit.text()

        query = """
        INSERT INTO class
        (PID, level, order_date, order_by, date_passing, actual_from, actual_to, vus)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
        """.format(self.pid, class_typ, order_from, order, date_pass, actual_from, actual_to, vus)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

        new_id = self.db.last_insert_id("class", self.pid)

        # История: старая текущая классность сохраняется, а не перезаписывается.
        # Если у предыдущей действующей записи период был открыт (actual_to не задан),
        # закрываем его датой начала новой классности.
        prev_rows = self.db.select(
            '''SELECT "ID", actual_to FROM class
               WHERE PID = '{}' AND "ID" != {}
               ORDER BY order_date DESC, "ID" DESC'''.format(self.pid, new_id))
        if prev_rows and not prev_rows[0][1]:
            close_date = actual_to if actual_to else actual_from
            self.db.execute_n(
                'UPDATE class SET actual_to = ? WHERE "ID" = ?',
                (close_date, prev_rows[0][0]))
            for i, row_id in enumerate(self.class_table.id_list):
                if row_id == prev_rows[0][0]:
                    item = self.class_table.item(i, 6)
                    if item is None or not item.text():
                        self.class_table.setItem(i, 6, QtWidgets.QTableWidgetItem(
                            close_date.strftime(self.date_format)))

        self.class_table.insertRow(self.class_table.rowCount())
        self.class_table.setItem(self.class_table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(class_typ))
        self.class_table.setItem(self.class_table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(self.class_date_passing_edit.text()))
        self.class_table.setItem(self.class_table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(order))
        self.class_table.setItem(self.class_table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(self.class_order_from_edit.text()))
        self.class_table.setItem(self.class_table.rowCount() - 1, 4, QtWidgets.QTableWidgetItem(vus))
        self.class_table.setItem(self.class_table.rowCount() - 1, 5, QtWidgets.QTableWidgetItem(self.class_actual_from.text()))
        self.class_table.setItem(self.class_table.rowCount() - 1, 6, QtWidgets.QTableWidgetItem(self.class_actual_to.text()))

        self.class_table.id_list.append(new_id)
    
    def add_fizo(self):
        category = self.fizo_type_edit.currentText()
        rank = self.fizo_rank_edit.currentText()

        query = """
        INSERT INTO fizo_act (PID, act_level, rank)
        VALUES ('{}', '{}', '{}')
        """.format(self.pid, category, rank)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

    def add_nis(self):
        if self.nis_user.isChecked():
            finished = self.nis_finished.itemData(self.nis_finished.currentIndex())
            num = self.nis_number.text()
            date = self.nis_date.dateTime().toPyDateTime().date()
            query = """
            INSERT INTO ipoteka (PID, user, finished, number, date_joining)
            VALUES ('{}', 'True', '{}', '{}', '{}')
            """.format(self.pid, finished, num, date)
            try:
                self.db.execute(query)
            except Exception as e:
                self.db.connection.commit()
                self.error(str(e))
        else:
            query = """
            DELETE FROM ipoteka WHERE PID = '{}'
            """.format(self.pid)
            try:
                self.db.execute(query)
            except Exception as e:
                self.db.connection.commit()
                self.error(str(e))

    def add_auto(self):
        brand = self.auto_brand_edit.text()
        model = self.auto_model_edit.text()
        num = self.auto_gos_num_edit.text()
        color = self.auto_color_edit.text()

        query = """
        INSERT INTO auto (PID, brand, model, gos_num, color)
        VALUES ('{}', '{}', '{}', '{}', '{}')
        """.format(self.pid, brand, model, num, color)

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

        self.auto_table.insertRow(self.auto_table.rowCount())
        self.auto_table.setItem(self.auto_table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(brand))
        self.auto_table.setItem(self.auto_table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(model))
        self.auto_table.setItem(self.auto_table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(num))
        self.auto_table.setItem(self.auto_table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(color))

        self.auto_table.id_list.append(self.db.last_insert_id("auto", self.pid))

    def add_lgot(self):
        lgots = ''
        for key in self.lgot_w.keys():
            if self.lgot_w[key].isChecked():
                lgots += str(key) + ','
        query = """INSERT INTO person_lgoty (PID, lgots) VALUES ('{}', '{}')""".format(self.pid, lgots)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

    def add_dolg(self):
        exist = self.dolg_exist.itemData(self.dolg_exist.currentIndex())
        if exist:
            typ = self.dolg_type.itemData(self.dolg_type.currentIndex())
            org = self.dolg_org.text()
            summ = self.dolg_summ.text()
            query = """
            INSERT INTO dolg (PID, credit_type, credit_org, summ)
            VALUES ('{}', {}, '{}', '{}')
            """.format(self.pid, typ, org, summ)
            try:
                self.db.execute(query)
            except Exception as e:
                self.db.connection.commit()
                self.error(str(e))
        else:
            query = """DELETE FROM dolg WHERE PID = '{}'""".format(self.pid)
            try:
                self.db.execute(query)
            except Exception as e:
                self.db.connection.commit()
                self.error(str(e))

    def add_family(self):
        typ = self.family_type_edit.currentText()
        date = self.family_birthday_edit.dateTime().toPyDateTime().date()
        fam = self.family_family_edit.text()
        nam = self.family_name_edit.text()
        pat = self.family_patr_edit.text()
        
        query = """
        INSERT INTO family 
        (PID, type, second_name, first_name, patr, birthday)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
        """.format(self.pid, typ, fam, nam, pat, date)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))

        self.doc_person_edit.addItem(f'{typ} {fam} {nam[0]}.{pat[0]}')
        
        self.family_table.insertRow(self.family_table.rowCount())
        self.family_table.setItem(self.family_table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(typ))
        self.family_table.setItem(self.family_table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(fam))
        self.family_table.setItem(self.family_table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(nam))
        self.family_table.setItem(self.family_table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(pat))
        self.family_table.setItem(self.family_table.rowCount() - 1, 4, QtWidgets.QTableWidgetItem(self.family_birthday_edit.text()))

        query = """SELECT "ID" FROM family"""
        self.family_table.id_list.append(self.db.select(query)[-1][0])

    def closeEvent(self, e):
        if self.pid:
            self.parent.chose_person(self.pid)
        QtWidgets.QWidget.closeEvent(self, e)

            
    def error(self, text):
        w = QtWidgets.QMessageBox.critical(self, 'Ошибка!', text, defaultButton=QtWidgets.QMessageBox.Ok)

    def update_docs(self, typ):
        columns = {
            0: "type",
            1: "serial",
            2: "num",
            3: "given_by",
            4: "code",
            5: "doc_date"
        }
        self.update_table(typ, self.doc_table, 'documents', columns, (5, ))

    def update_family(self, typ):
        columns = {
            0: "type",
            1: "second_name",
            2: "first_name",
            3: "patr",
            4: "birthday"
        }
        self.update_table(typ, self.family_table, 'family', columns, (4,))

    def update_auto(self, typ):
        columns = {
            0: "brand",
            1: "model",
            2: "gos_num",
            3: "color"
        }
        self.update_table(typ, self.auto_table, 'auto', columns, ())

    def update_class(self, typ):
        columns = {
            0: "level",
            3: "order_date",
            2: "order_by",
            1: "date_passing",
            5: "actual_from",
            6: "actual_to",
            4: "vus"
        }
        self.update_table(typ, self.class_table, 'class', columns, (1, 3, 5, 6))

    def update_table(self, typ, table, table_name, columns, data_format):
        if typ == 'delete':
            rows = set()
            for index in table.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM {}
                    WHERE "ID" = {};
                """.format(table_name, table.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', str(e), defaultButton=QtWidgets.QMessageBox.Ok)
                table.id_list.pop(row)
                table.removeRow(row)


class InsertWindow(UpdateWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        if parent:
            self.parent = parent
        
        self.pid = None
        
        for i in range(1, len(self.tab_widget)):
            self.tab_widget.setTabEnabled(i, False)
        
        
    def person_ID_changed(self):
        data = dict()

        if self.labels['surname'].text() != '' or self.labels['surname'].text() != '' or self.labels['surname'].text() != '':

            data['surname'] = self.labels['surname'].text()
            data['name'] = self.labels['name'].text()
            data['patr'] = self.labels['patr'].text()
            data['number'] = self.labels['number'].text()
            data['rank'] = self.labels['rank'].text()
            data['birthday_date'] = self.labels['birthday_date'].dateTime().toPyDateTime().date()
            data['place_of_birth'] = self.labels['place_of_birth'].text()
            data['nation'] = self.labels['nation'].text()
            data['gender'] = self.labels['gender'].currentText()
            data['family_status'] = self.labels['family_status'].itemData(self.labels['family_status'].currentIndex())
            data['mobile_number'] = self.labels['mobile_number'].text()
            data['mobile_number1'] = self.labels['mobile_number1'].text()
            data['status'] = self.labels['status'].itemData(self.labels['status'].currentIndex())
            data['status1'] = self.labels['status1'].itemData(self.labels['status1'].currentIndex())
            data['position'] = self.labels['position'].currentText()
            data['division'] = self.labels['division'].currentText()
            data['order'] = self.labels['order'].text()
            data['order_date'] = self.labels['order_date'].dateTime().toPyDateTime().date()
            data['allowance'] = self.labels['allowance'].text()
            data['allowance_by'] = self.labels['allowance_by'].text()
            data['allowance_date'] = self.labels['allowance_date'].dateTime().toPyDateTime().date()
            data['reg_addr'] = self.labels['reg_addr'].text()
            data['liv_addr'] = self.labels['liv_addr'].text()
            data['buisness'] = self.labels['buisness'].text()
            data['snils'] = self.labels['snils'].text()
            data['inn'] = self.labels['inn'].text()
            data['fizo_num'] = self.labels['fizo_num'].text()

            query = """
            INSERT INTO persons(
                lnum, second_name, first_name, patr, place_of_birth, date_of_birth, 
                gender, nation, phone_num1, phone_num2, active, mil, address_reg, 
                address_living, allowance_num, allowance_by, allowance_date, 
                family_status, rank, division, "position", order_by, order_date, person_buisness,
                snils, inn, fizo_num, financing)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 
                    '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                    '{}', '{}', '{}', '{}', 
                    '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {});
            ;
            """.format(
                    data['number'],
                    data['surname'],
                    data['name'],
                    data['patr'],
                    data['place_of_birth'],
                    data['birthday_date'],
                    data['gender'],
                    data['nation'],
                    data['mobile_number'],
                    data['mobile_number1'],
                    data['status1'],
                    data['status'],
                    data['reg_addr'],
                    data['liv_addr'],
                    data['allowance'],
                    data['allowance_by'],
                    data['allowance_date'],
                    data['family_status'],
                    data['rank'],
                    data['division'],
                    data['position'],
                    data['order'],
                    data['order_date'],
                    data['buisness'],
                    data['snils'],
                    data['inn'],
                    data['fizo_num'],
                    self.currentFinancingId()
                )
            try:
                self.db.execute(query)
                if data['status']:
                    for i in range(1, len(self.tab_widget)):
                        self.tab_widget.setTabEnabled(i, True)
                else:
                    self.tab_widget.setTabEnabled(1, True)
                    self.tab_widget.setTabEnabled(2, True)
                    self.tab_widget.setTabEnabled(7, True)
                    self.tab_widget.setTabEnabled(8, True)
                query = """
                SELECT 
                persons."ID"
                FROM 
                persons
                WHERE 
                persons.lnum = '{}' AND 
                persons.second_name = '{}' AND
                persons.first_name = '{}' AND
                persons.patr = '{}';
                """.format(
                    data['number'],
                    data['surname'],
                    data['name'],
                    data['patr']
                    )
                res = self.db.select(query)
                if res:
                    self.pid = res[0][0]
                w = QtWidgets.QMessageBox.information(self, '', 'Запись добавлена', defaultButton=QtWidgets.QMessageBox.Ok)
                self.parent.find()
                self.parent.win = ChangeWindow(self.db.get_data(self.pid)[0], self.parent)
                self.parent.win.setWindowTitle('Редактировать')
                self.parent.win.show()
                self.parent.win.showMaximized()
                self.close()
            except Exception as e:
                self.db.connection.commit()
                self.error(str(e))
        else:
            self.error('Поля ФИО обязательны для заполнения!')
    

class ChangeWindow(UpdateWindow):
    def __init__(self, main_data, parent=None):
        super().__init__(parent=parent)
        
        self.pid = main_data[0]
        
        pixmap = QtGui.QPixmap()
        #self.img_label.setAlignment(QtCore.Qt.AlignCenter)
        
        data = dict()

        data['number'] = main_data[1]
        data['surname'] = main_data[2]
        data['name'] = main_data[3]
        data['patr'] = main_data[4]
        data['place_of_birth'] = main_data[5]
        data['birthday_date'] = main_data[6]
        data['gender'] = main_data[7]
        data['nation'] = main_data[8]
        data['mobile_number'] = main_data[9]
        data['mobile_number1'] = main_data[10]
        data['status1'] = main_data[11]
        data['status'] = main_data[12]
        data['reg_addr'] = main_data[13]
        data['liv_addr'] = main_data[14]
        data['allowance'] = main_data[15]
        data['allowance_by'] = main_data[16]
        data['allowance_date'] = main_data[17]
        data['family_status'] = main_data[19]
        data['rank'] = main_data[20]
        data['division'] = main_data[21]
        data['position'] = main_data[22]
        data['order'] = main_data[23]
        data['order_date'] = main_data[24]
        data['buisness'] = main_data[26]
        data['snils'] = main_data[27]
        data['inn'] = main_data[28]
        data['fizo_num'] = main_data[29]
        # вид финансового обеспечения (колонка persons.financing)
        data['financing'] = None
        try:
            res_fin = self.db.select("SELECT financing FROM persons WHERE \"ID\" = {};".format(main_data[0]))
            if res_fin and res_fin[0][0] is not None:
                data['financing'] = int(res_fin[0][0])
        except Exception:
            pass
        
        for i in range(1, len(self.tab_widget)):
            self.tab_widget.setTabEnabled(i, True)
        
        blob = main_data[25]
        if blob:
            pixmap.loadFromData(blob)
            pixmap = pixmap.scaled(150, self.img_label.height(), QtCore.Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)
        
        if parent:
            self.parent = parent
        
        #self.finish_btn.clicked.connect(self.update_data)
        
        self.labels['surname'].setText(data['surname'])
        self.labels['name'].setText(data['name'])
        self.labels['patr'].setText(data['patr'])
        self.labels['number'].setText(data['number'])
        self.labels['rank'].setText(data['rank'])
        self.labels['birthday_date'].setDate(data['birthday_date'])
        self.labels['place_of_birth'].setText(data['place_of_birth'])
        self.labels['nation'].setText(data['nation'])
        self.labels['gender'].setCurrentText(data['gender'])
        self.labels['family_status'].setCurrentText(self.db.select("""SELECT name FROM family_status WHERE "ID" = '{}';""".format(data['family_status']))[0][0])
        self.labels['mobile_number'].setText(data['mobile_number'])
        self.labels['mobile_number1'].setText(data['mobile_number1'])
        if data['status'] == 'False':
            self.labels['status'].setCurrentText('ГП ВС РФ')
        if data['status1'] == 'False':
            self.labels['status1'].setCurrentText('Резерв')
        self.labels['position'].setCurrentText(data['position'])
        self.labels['division'].setCurrentText(data['division'])
        self.labels['order'].setText(data['order'])
        if data['order_date']:
            self.labels['order_date'].setDate(data['order_date'])
        self.labels['allowance'].setText(data['allowance'])
        self.labels['allowance_by'].setText(data['allowance_by'])
        if data['allowance_date']:
            self.labels['allowance_date'].setDate(data['allowance_date'])
        self.labels['reg_addr'].setText(data['reg_addr'])
        self.labels['liv_addr'].setText(data['liv_addr'])
        self.labels['buisness'].setText(data['buisness'])
        self.labels['snils'].setText(data['snils'])
        self.labels['inn'].setText(data['inn'])
        self.labels['fizo_num'].setText(data['fizo_num'])
        self._load_financing(data.get('financing'))

        query = f'''
        SELECT second_name, first_name, patr FROM persons where ID = '{self.pid}'
        '''
        res = self.db.select(query)
        if res:
            for row in res:
                self.doc_person_edit.addItem(f'{row[0]} {row[1][0]}.{row[2][0]}')


        query = f'''
        SELECT type, second_name, first_name, patr FROM family where PID = '{self.pid}'
        '''
        res = self.db.select(query)
        if res:
            for row in res:
                self.doc_person_edit.addItem(f'{row[0]} {row[1]} {row[2][0]}.{row[3][0]}')

        query = """
            SELECT 
            documents.type, 
            documents.name, 
            documents.serial, 
            documents.num, 
            documents.given_by, 
            documents.code, 
            documents.doc_date,
            documents."ID"
            FROM 
            documents
            WHERE 
            documents."PID" = '{}'
            ORDER BY
            documents.doc_date ASC;
            """.format(self.pid)
        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.doc_table.insertRow(self.doc_table.rowCount())
                self.doc_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.doc_table.setItem(idx, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.doc_table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2]))
                self.doc_table.setItem(idx, 3, QtWidgets.QTableWidgetItem(line[3]))
                self.doc_table.setItem(idx, 4, QtWidgets.QTableWidgetItem(line[4]))
                self.doc_table.setItem(idx, 5, QtWidgets.QTableWidgetItem(line[5]))
                _dd = line[6].strftime(self.date_format) if hasattr(line[6], 'strftime') else (str(line[6]) if line[6] else '')
                self.doc_table.setItem(idx, 6, QtWidgets.QTableWidgetItem(_dd))
                self.doc_table.id_list.append(line[-1])

        query = """
                SELECT 
                family.type, 
                family.second_name, 
                family.first_name, 
                family.patr, 
                family.birthday,
                family."ID"
                FROM 
                family
                WHERE "PID"={}
                ORDER BY
                family.birthday ASC;
                """.format(self.pid)
        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.family_table.insertRow(self.family_table.rowCount())
                self.family_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.family_table.setItem(idx, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.family_table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2]))
                self.family_table.setItem(idx, 3, QtWidgets.QTableWidgetItem(line[3]))
                _fb = line[4].strftime(self.date_format) if hasattr(line[4], 'strftime') else (str(line[4]) if line[4] else '')
                self.family_table.setItem(idx, 4, QtWidgets.QTableWidgetItem(_fb))
                self.family_table.id_list.append(line[-1])

        query = '''
                    SELECT 
                    class.level, 
                    class.order_date, 
                    class.order_by, 
                    class.date_passing, 
                    class.actual_from, 
                    class.actual_to, 
                    class.vus,
                    "ID"
                    FROM 
                    class
                    WHERE
                    class."PID" = {};
                    '''.format(self.pid)
        res = self.db.select(query)
        if res:
            def c_date(d):
                return d.strftime(self.date_format) if d else ''
            for idx, line in enumerate(res):
                self.class_table.insertRow(self.class_table.rowCount())
                self.class_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.class_table.setItem(idx, 1, QtWidgets.QTableWidgetItem(c_date(line[3])))
                self.class_table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2]))
                self.class_table.setItem(idx, 3, QtWidgets.QTableWidgetItem(c_date(line[1])))
                self.class_table.setItem(idx, 4, QtWidgets.QTableWidgetItem(line[6]))
                self.class_table.setItem(idx, 5, QtWidgets.QTableWidgetItem(c_date(line[4])))
                self.class_table.setItem(idx, 6, QtWidgets.QTableWidgetItem(c_date(line[5])))
                self.class_table.id_list.append(line[-1])

        query = '''
                    SELECT 
                    auto.brand, 
                    auto.model, 
                    auto.gos_num, 
                    auto.color,
                    auto."ID"
                    FROM 
                    auto 
                    WHERE
                    auto."PID" = {};
                    '''.format(self.pid)
        res = self.db.select(query)
        if res:
            for idx, line in enumerate(res):
                self.auto_table.insertRow(self.auto_table.rowCount())
                self.auto_table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0] or ''))
                self.auto_table.setItem(idx, 1, QtWidgets.QTableWidgetItem(line[1] or ''))
                self.auto_table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2] or ''))
                self.auto_table.setItem(idx, 3, QtWidgets.QTableWidgetItem(line[3] or ''))
                self.auto_table.id_list.append(line[-1])


        query = '''
            SELECT 
            lgots
            FROM 
            person_lgoty
            WHERE 
            person_lgoty."PID" = {};
            '''.format(self.pid)
        res = self.db.select(query)
        if res:
            lgots = res[-1][0].split(',')
            for el in lgots:
                if el:
                    self.lgot_w[int(el)].setChecked(True)

        query = '''
                SELECT act_level, rank
                FROM fizo_act
                WHERE 
                fizo_act."PID" = '{}'
                '''.format(self.pid)
        res = self.db.select(query)
        if res:
            self.fizo_type_edit.setCurrentText(res[-1][0])
            self.fizo_rank_edit.setCurrentText(res[-1][1])

        query = '''
                    SELECT 
                    ipoteka."user", 
                    ipoteka.finished, 
                    ipoteka."number", 
                    ipoteka.date_joining
                    FROM 
                    ipoteka
                    WHERE 
                    ipoteka."PID" = {};
                    '''.format(self.pid)
        res = self.db.select(query)
        if res:
            if res[-1][0]:
                self.nis_user.setChecked(True)
                if res[-1][1] == 'True':
                    t = 'Да'
                else:
                    t = 'Нет'
                self.nis_finished.setCurrentText(res[-1][1])
                self.nis_number.setText(res[-1][2])
                self.nis_date.setDate(res[-1][3])
            else:
                self.nis_user.setChecked(False)

        query = '''
                    SELECT 
                    dolg.credit_org, 
                    credit_types.name, 
                    dolg.summ
                    FROM 
                    dolg, 
                    credit_types
                    WHERE 
                    credit_types."ID" = dolg.credit_type AND 
                    dolg."PID" = {};
                    '''.format(self.pid)
        res = self.db.select(query)
        if res:
            row = res[-1]
            self.dolg_exist.setCurrentText('Да')
            self.dolg_type.setCurrentText(row[1])
            self.dolg_org.setText(row[0])
            self.dolg_summ.setText(row[2])
        else:
            self.dolg_exist.setCurrentText('Нет')

    def person_ID_changed(self):
        self.full_save()
        data = dict()
        data['surname'] = self.labels['surname'].text()
        data['name'] = self.labels['name'].text()
        data['patr'] = self.labels['patr'].text()
        data['number'] = self.labels['number'].text()
        data['rank'] = self.labels['rank'].text()
        data['birthday_date'] = self.labels['birthday_date'].dateTime().toPyDateTime().date()
        data['place_of_birth'] = self.labels['place_of_birth'].text()
        data['nation'] = self.labels['nation'].text()
        data['gender'] = self.labels['gender'].currentText()
        data['family_status'] = self.labels['family_status'].itemData(self.labels['family_status'].currentIndex())
        data['mobile_number'] = self.labels['mobile_number'].text()
        data['mobile_number1'] = self.labels['mobile_number1'].text()
        data['status'] = self.labels['status'].itemData(self.labels['status'].currentIndex())
        data['status1'] = self.labels['status1'].itemData(self.labels['status1'].currentIndex())
        data['position'] = self.labels['position'].currentText()
        data['division'] = self.labels['division'].currentText()
        data['order'] = self.labels['order'].text()
        data['order_date'] = self.labels['order_date'].dateTime().toPyDateTime().date()
        data['allowance'] = self.labels['allowance'].text()
        data['allowance_by'] = self.labels['allowance_by'].text()
        data['allowance_date'] = self.labels['allowance_date'].dateTime().toPyDateTime().date()
        data['reg_addr'] = self.labels['reg_addr'].text()
        data['liv_addr'] = self.labels['liv_addr'].text()
        data['buisness'] = self.labels['buisness'].text()
        data['snils'] = self.labels['snils'].text()
        data['inn'] = self.labels['inn'].text()
        data['fizo_num'] = self.labels['fizo_num'].text()
        
        query = """
        UPDATE persons
        SET 
        "lnum" = '{}',
        "second_name" = '{}',
        "first_name" = '{}',
        "patr" = '{}',
        "place_of_birth" = '{}',
        "date_of_birth" = '{}',
        "gender" = '{}',
        "nation" = '{}',
        "phone_num1" = '{}',
        "phone_num2"  = '{}',
        "active" = '{}',
        "mil" = '{}',
        "address_reg" = '{}',
        "address_living" = '{}',
        "allowance_num" = '{}',
        "allowance_by" = '{}',
        "allowance_date" = '{}',
        "family_status" = '{}',
        "rank" = '{}',
        "division" = '{}',
        "position" = '{}',
        "order_by" = '{}',
        "order_date" = '{}',
        "person_buisness" = '{}',
        "snils" = '{}',
        "inn" = '{}',
        "fizo_num" = '{}',
        "financing" = {}
        WHERE "ID"='{}'            
        """.format(
            data['number'],
                data['surname'],
                data['name'],
                data['patr'],
                data['place_of_birth'],
                data['birthday_date'],
                data['gender'],
                data['nation'],
                data['mobile_number'],
                data['mobile_number1'],
                data['status1'],
                data['status'],
                data['reg_addr'],
                data['liv_addr'],
                data['allowance'],
                data['allowance_by'],
                data['allowance_date'],
                data['family_status'],
                data['rank'],
                data['division'],
                data['position'],
                data['order'],
                data['order_date'],
                data['buisness'],
                data['snils'],
                data['inn'],
                data['fizo_num'],
                self.currentFinancingId(),
                self.pid
            )
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            self.error(str(e))
        
    def update_data(self):
        self.close()


class Table(QtWidgets.QTableWidget):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, rows, cols, ident, parent=None):
        super().__init__(rows, cols, parent=parent)

        self.ident = str(ident)
        self.id_list = list()

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.setWordWrap(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.context_menu = QtWidgets.QMenu()
        self.delete_action = QtWidgets.QAction(QtGui.QIcon(), 'Удалить', self)
        self.delete_action.triggered.connect(self.delete)
        self.context_menu.addAction(self.delete_action)

        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)

        # кроссплатформенный каталог конфигурации (Windows: %APPDATA%, иначе ~/.config)
        conf_root = os.environ.get('APPDATA') or os.path.expanduser('~/.config')
        self.conf_dir = os.path.join(conf_root, 'HRaccounting')

        if not os.path.exists(self.conf_dir):
            os.makedirs(self.conf_dir, exist_ok=True)

        self.horizontalHeader().sectionResized.connect(self.save_state)

        if os.path.exists(os.path.join(self.conf_dir, self.ident)):
            with open(os.path.join(self.conf_dir, self.ident), 'rb') as f:
                self.horizontalHeader().restoreState(f.read())

    def delete(self):
        result = QtWidgets.QMessageBox.question(None, "Удаление элемента",
                                                "Вы уверены что хотите удалить выделенные элементы?",
                                                defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            self.signal.emit('delete')

    def save_state(self):
        with open(os.path.join(self.conf_dir, self.ident), 'wb') as f:
            f.write(self.horizontalHeader().saveState())

    def contextMenuEvent(self, e):
        self.context_menu.exec_(e.globalPos())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = InsertWindow()
    window.show()

    sys.exit(app.exec_())
