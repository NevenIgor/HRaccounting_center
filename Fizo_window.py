from PyQt5 import QtCore, QtWidgets, QtGui
import widgets.data_forms as Widgets
import time
import threading
import datetime
from fp.points import get_points

from db_API import Database as DB
            
class ExercisesWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)
        
        self.db = db
        self.ui = None
        
        main_layout = QtWidgets.QVBoxLayout()
        
        self.tv = QtWidgets.QTableView()
        self.sti = QtGui.QStandardItemModel()
        groups = []
        for i in range(9):
            groups.append(list())
        for i in range(9):
            for j in range(71):
                item = QtGui.QStandardItem()
                item.setCheckable(True)
                groups[i].append(item)
        for i in range(9):
            self.sti.appendRow(groups[i])
            
        labels = []
        for i in range(9):
            labels.append("{} возростная группа".format(i + 1))
            
        self.sti.setVerticalHeaderLabels(labels)
            
        self.tv.setModel(self.sti)
        self.tv.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        for i in range(71):
            self.tv.setColumnWidth(i, 1)
            
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(QtWidgets.QLabel('Период сдачи:'))
        self.name_edit = QtWidgets.QLineEdit()
        h_layout.addWidget(self.name_edit)
        add_btn = QtWidgets.QPushButton()
        add_btn.clicked.connect(self.add)
        h_layout.addWidget(add_btn)
        
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.currentIndexChanged.connect(self.update_data)
        self.save_btn = QtWidgets.QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save)
        query = """
        SELECT 
        name, 
        "ID"
        FROM 
        fizo_dates;
        """
        res = self.db.select(query)
        if res:
            for el in res:
                self.combo_box.addItem(el[0], el[1])
        else:
            self.tv.setDisabled(True)
            self.save_btn.setDisabled(True)
        
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.combo_box)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(self.tv)
        
        
        self.setLayout(main_layout)
        
    def add(self):
        text = self.name_edit.text()
        if text:
            query = """
            INSERT INTO fizo_dates (name) VALUES ('{}');
            """.format(text)
            self.db.execute(query)
            query = """
            SELECT 
            fizo_dates."ID"
            FROM 
            fizo_dates
            WHERE 
            fizo_dates.name = '{}';
            """.format(text)
            res = self.db.select(query)
            if res:
                idx = res[0][0]
                self.combo_box.addItem(text, idx)
                self.tv.setEnabled(True)
                self.save_btn.setEnabled(True)
                
    def save(self):
        strings = []
        for i in range(9):
            row = []
            for j in range(70):
                if self.sti.item(i, j).checkState() == 2:
                    row.append(str(j + 1))
            strings.append(','.join(row))
        query = """
        UPDATE fizo_dates
        SET "1m"='{}', "2m"='{}', "3m"='{}', "4m"='{}', "5m"='{}', "6m"='{}', 
        "7m"='{}', "8m"='{}', "9m"='{}'
        WHERE fizo_dates."ID" = '{}';
        """.format(strings[0], strings[1], strings[2], strings[3], strings[4], strings[5], strings[6], strings[7], strings[8], self.combo_box.itemData(self.combo_box.currentIndex()))
        self.db.execute(query)
        
    def update_data(self):
        query = """
        SELECT 
        fizo_dates."1m", 
        fizo_dates."2m", 
        fizo_dates."3m", 
        fizo_dates."4m", 
        fizo_dates."5m", 
        fizo_dates."6m", 
        fizo_dates."7m", 
        fizo_dates."8m", 
        fizo_dates."9m"
        FROM 
        fizo_dates
        WHERE 
        "ID" = '{}';
        """.format(self.combo_box.itemData(self.combo_box.currentIndex()))
        result = self.db.select(query)
        if result:
            for i, row in enumerate(result[0]):
                if row:
                    data = row.split(',')
                    for el in data:
                        self.sti.item(i, int(el) - 1).setCheckState(QtCore.Qt.Checked)
                
        
        
        
class FizoWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)
        
        self.db = db
        self.ui = None
        
        self.exercises = get_points()
        self.current_age = None
        self.group = None
        self.points = None
        
        main_layout = QtWidgets.QVBoxLayout()
        
        self.tv = QtWidgets.QTableView()
        self.sti = QtGui.QStandardItemModel()
            
        self.tv.setModel(self.sti)
        self.tv.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.strong = range(1, 17)
        self.speed = range(17, 23)
        self.stamina = range(23, 30)
        self.acc = range(30, 39)
        self.spec = range(39, 71)

        query = """
        SELECT  
        persons.second_name, 
        persons.first_name, 
        persons.patr, 
        persons."ID", 
        persons.date_of_birth
        FROM 
        persons
        WHERE 
        persons.mil = True;
        """
        res = self.db.select(query)
        self.arr = []
        self.persons = {}
        for row in res:
            text = row[0].capitalize() + ' ' + row[1][0] + '.' + row[2][0] + '.'
            self.arr.append(text)
            self.persons[text] = row[3]
            
        self.h_layout = QtWidgets.QGridLayout()
        
        self.main_data_combo_box = QtWidgets.QComboBox()
        self.weight_box = QtWidgets.QComboBox()
        self.fio_edit = QtWidgets.QLineEdit()
        self.fio_edit.textChanged.connect(self.update_data)
        completer = QtWidgets.QCompleter(self.arr)
        self.fio_edit.setCompleter(completer)
        self.num_edit = QtWidgets.QLineEdit()
        self.speed_exercize = QtWidgets.QComboBox()
        self.stamina_exercize = QtWidgets.QComboBox()
        self.strong_exercize = QtWidgets.QComboBox()
        
        self.str_res_int = QtWidgets.QSpinBox()
        self.str_res_min = QtWidgets.QTimeEdit()
        self.str_res_min.setDisplayFormat("mm:ss")
        self.speed_res_sec = QtWidgets.QTimeEdit()
        self.speed_res_sec.setDisplayFormat("ss,z")
        self.speed_res_sec.timeChanged.connect(self.time_inc)
        self.speed_res_min = QtWidgets.QTimeEdit()
        self.speed_res_min.setDisplayFormat("mm:ss")
        self.speed_res_min.setEnabled(True)
        self.speed_res_int = QtWidgets.QSpinBox()
        self.speed_res_int.setMaximum(1000)
        self.speed_res_box = QtWidgets.QComboBox()
        self.stamina_res_min = QtWidgets.QTimeEdit()
        self.stamina_res_min.setDisplayFormat("mm:ss")
        self.stamina_res_int = QtWidgets.QSpinBox()
        self.stamina_res_int.setMaximum(1000)
        
        self.str_p = QtWidgets.QLineEdit()
        self.stamina_p = QtWidgets.QLineEdit()
        self.speed_p = QtWidgets.QLineEdit()
        self.summ = QtWidgets.QLineEdit()
        self.mark = QtWidgets.QLineEdit()
        self.level = QtWidgets.QLineEdit()
        
        self.str_p.textChanged.connect(self.total_calc)
        self.stamina_p.textChanged.connect(self.total_calc)
        self.speed_p.textChanged.connect(self.total_calc)
        
        self.showed = self.speed_res_sec
        
        self.weight_box.currentIndexChanged.connect(self.strong_calculate)
        self.str_res_int.valueChanged.connect(self.strong_calculate)
        self.str_res_min.timeChanged.connect(self.strong_calculate)
        self.speed_res_sec.timeChanged.connect(self.speed_calculate)
        self.speed_res_min.timeChanged.connect(self.speed_calculate)
        self.speed_res_box.currentIndexChanged.connect(self.speed_calculate)
        self.speed_res_int.valueChanged.connect(self.speed_calculate)
        self.stamina_res_min.timeChanged.connect(self.stamina_calculate)
        self.stamina_res_int.valueChanged.connect(self.stamina_calculate)
        
        
        
        self.speed_res_box.addItem('Выполнен вариант № 1', 100)
        self.speed_res_box.addItem('Выполнен вариант № 2', 70)
        self.speed_res_box.addItem('Выполнен вариант № 3', 40)
        self.speed_res_box.addItem('Невыполнено', 0)
        
        labels = []
        labels_text = ('Фамилия и инициалы', 'Нагрудный\nномер', 'Весовая\nкатегория', 'Номер\nупражнения', 'Результат', 'Балл', 'Номер\nупражнения', 'Результат', 'Балл', 'Номер\nупражнения', 'Результат', 'Балл', 'Сумма\nбаллов', 'Оценка', 'Уровень')
        for text in labels_text:
            labels.append(QtWidgets.QLabel(text))
            
        for label in labels:
            label.setAlignment(QtCore.Qt.AlignCenter)
        for i, label in enumerate(labels):
            self.h_layout.addWidget(label, 1, i)
        l1 = QtWidgets.QLabel('Быстрота\n(ловкость)')
        l2 = QtWidgets.QLabel('Сила')
        l3 = QtWidgets.QLabel('Выносливость')
        l1.setAlignment(QtCore.Qt.AlignCenter)
        l2.setAlignment(QtCore.Qt.AlignCenter)
        l3.setAlignment(QtCore.Qt.AlignCenter)
        self.h_layout.addWidget(l1, 0, 3, 1, 3)
        self.h_layout.addWidget(l2, 0, 6, 1, 3)
        self.h_layout.addWidget(l3, 0, 9, 1, 3)
        
        self.h_layout.addWidget(self.fio_edit)
        self.h_layout.addWidget(self.num_edit)
        self.h_layout.addWidget(self.weight_box)
        self.h_layout.addWidget(self.speed_exercize)
        self.h_layout.addWidget(self.speed_res_sec)
        self.h_layout.addWidget(self.speed_p)
        self.h_layout.addWidget(self.strong_exercize)
        self.h_layout.addWidget(self.str_res_int)
        self.h_layout.addWidget(self.str_p)
        self.h_layout.addWidget(self.stamina_exercize)
        self.h_layout.addWidget(self.stamina_res_min)
        self.h_layout.addWidget(self.stamina_p)
        self.h_layout.addWidget(self.summ)
        self.h_layout.addWidget(self.mark)
        self.h_layout.addWidget(self.level)
        self.h_layout.setColumnStretch(0, 1000)
        
        self.strong_exercize.currentIndexChanged.connect(self.set_strong)
        self.speed_exercize.currentIndexChanged.connect(self.set_speed)
        self.stamina_exercize.currentIndexChanged.connect(self.set_stamina)
        
        
        self.str_res_int.setDisabled(True)
        self.speed_res_sec.setDisabled(True)
        self.stamina_res_min.setDisabled(True)
        self.weight_box.addItem('<70', 'L')
        self.weight_box.addItem('70-80', 'M')
        self.weight_box.addItem('80+', 'H')
        
        self.weight_box.setDisabled(True)
        
        
        main_layout.addWidget(self.main_data_combo_box)
        main_layout.addLayout(self.h_layout)
        main_layout.addWidget(self.tv)
        
        query = """
        SELECT 
        fizo_dates.name, 
        fizo_dates."ID"
        FROM 
        fizo_dates
        """
        res = self.db.select(query)
        if res:
            for el in res:
                self.main_data_combo_box.addItem(el[0], el[1])
        
        
        self.setLayout(main_layout)
        
    def total_calc(self):
        if self.str_p.text() and self.speed_p.text() and self.stamina_p.text():
            total = int(self.str_p.text()) + int(self.speed_p.text()) + int(self.stamina_p.text())
            self.summ.setText(str(total))
            mark = ''
            level = ''
            if total >= self.points[0]:
                mark = '5'
                level = 'ВКУ'
            elif total >= self.points[1]:
                mark = '5'
                level = '1КУ'
            elif total >= self.points[2]:
                mark = '5'
                level = '2КУ'
            elif total >= self.points[5]:
                mark = '5'
                level = '3КУ'
            elif total >= self.points[4]:
                mark = '4'
            elif total >= self.points[3]:
                mark = '3'
            else:
                mark = '2'
            self.mark.setText(mark)
            self.level.setText(level)
            
                
        
        
    def time_inc(self):
        time = self.speed_res_sec.time()
        if time.msec() % 100 != 0:
            new_ms = (time.msec() + 100) - ((time.msec() + 100) % 100)
            self.speed_res_sec.setTime(QtCore.QTime(time.second(), new_ms))
        
    def set_speed(self):
        self.speed_res_sec.setEnabled(True)
        if int(self.speed_exercize.currentText()) in (17, 18, 19, 20, 30, 32, 36, 37, 38):
            if self.showed != self.speed_res_sec:
                self.showed.hide()
                self.h_layout.replaceWidget(self.showed, self.speed_res_sec)
                self.speed_res_sec.show()
                self.showed = self.speed_res_sec
        elif int(self.speed_exercize.currentText()) in (21, 22):
            if self.showed != self.speed_res_min:
                self.showed.hide()
                self.h_layout.replaceWidget(self.showed, self.speed_res_min)
                self.speed_res_min.show()
                self.showed = self.speed_res_min
        elif int(self.speed_exercize.currentText()) in (33, 34, 35):
            if self.showed != self.speed_res_box:
                self.showed.hide()
                self.h_layout.replaceWidget(self.showed, self.speed_res_box)
                self.speed_res_box.show()
                self.showed = self.speed_res_box
        elif int(self.speed_exercize.currentText()) in (31,):
            if self.showed != self.speed_res_int:
                self.showed.hide()
                self.h_layout.replaceWidget(self.showed, self.speed_res_int)
                self.speed_res_int.show()
                self.showed = self.speed_res_int
        self.speed_calculate()
        
    def speed_calculate(self):
        points = ''
        if self.speed_exercize.currentText():
            if int(self.speed_exercize.currentText()) in (17, 18, 19, 20, 30, 32, 36, 37, 38):
                res = self.speed_res_sec.time()
                result = str(res.second())
                if res.msec():
                    result += '.' + str(res.msec() // 100)
                if int(self.speed_exercize.currentText()) in (17, 18, 19):
                    ex = self.exercises[int(self.speed_exercize.currentText())][self.current_age]
                else:
                    ex = self.exercises[int(self.speed_exercize.currentText())]
                maximum = max(map(float, ex.keys()))
                minimum = min(map(float, ex.keys()))
                if float(result) > maximum:
                    points = 0
                elif float(result) < minimum:
                    points = 100
                else:
                    points = ex.get(result, None)
                    if not points:
                        i = 1
                        while not points:
                            print(result)
                            if '.' not in result:
                                result += '.1'
                            else:
                                msec = result[-1]
                                if msec == '9':
                                    sec, msec = result.split('.')
                                    result = str(int(sec) + 1)
                                else:
                                    result = result[:-1] + str(int(result[-1]) + 1)
                            points = ex.get(result, None) 
                            i += 1   
            elif int(self.speed_exercize.currentText()) in (21, 22):
                res = self.speed_res_min.time()
                result = str(res.minute()).rjust(2, '0') + ':' + str(res.second()).rjust(2, '0') + ':00'
                ex = self.exercises[int(self.speed_exercize.currentText())]
                if int(self.speed_exercize.currentText()) == 21:
                    minimum = 70
                    maximum = 195
                else:
                    minimum = 90
                    maximum = 220
                if res.second() + res.minute() * 60 < minimum:
                    points = 100
                elif res.second() + res.minute() * 60 < maximum + 1:
                    points = ex.get(result, None)
                    if not points:
                        i = 1
                        while not points:
                            sec = res.second() + i
                            if sec == 60:
                                mins = res.minute() + 1
                                sec = 0
                            else:
                                mins = res.minute()
                            result = str(mins).rjust(2, '0') + ':' + str(sec).rjust(2, '0') + ':00' 
                            points = ex.get(result, None) 
                            i += 1
                else:
                    points = 0 
            elif int(self.speed_exercize.currentText()) == 31:
                result = self.speed_res_int.value()
                maximum = 180
                minimum = 81
                if result > maximum:
                    points = 100
                elif result < minimum:
                    points = 0
                else:
                    points = self.exercises[31][str(result)]
            elif int(self.speed_exercize.currentText()) in (33, 34, 35):
                points = self.speed_res_box.itemData(self.speed_res_box.currentIndex())
                
        self.speed_p.setText(str(points))
        
    def set_strong(self):
        if self.strong_exercize.currentText() == '9' or self.strong_exercize.currentText() == '13':
            self.h_layout.replaceWidget(self.str_res_int, self.str_res_min)
            self.str_res_int.hide()
            self.str_res_min.show()
        else:
            self.h_layout.replaceWidget(self.str_res_min, self.str_res_int)
            self.str_res_min.hide()
            self.str_res_int.show()
            self.str_res_int.setEnabled(True)
        self.strong_calculate()
            
    def strong_calculate(self):
        points = ''
        if self.strong_exercize.currentText():
            if self.strong_exercize.currentText() == '13':
                res = self.str_res_min.time()
                result = str(res.minute()).rjust(2, '0') + ':' + str(res.second()).rjust(2, '0') + ':00'
                if res.second() + res.minute() * 60 < 180:
                    points = 100
                elif res.second() + res.minute() * 60 < 651:
                    points = self.exercises[13].get(result, None)
                    if not points:
                        i = 1
                        while not points:
                            sec = res.second() + i
                            if sec == 60:
                                mins = res.minute() + 1
                                sec = 0
                            else:
                                mins = res.minute()
                            result = str(mins).rjust(2, '0') + ':' + str(sec).rjust(2, '0') + ':00' 
                            points = self.exercises[13].get(result, None) 
                            i += 1
                else:
                    points = 0           
            elif self.strong_exercize.currentText() == '9':
                res = self.str_res_min.time()
                result = str(res.second() + res.minute() * 60)
                if res.second() + res.minute() * 60 > 1:
                    points = self.exercises[9].get(str(result), 100)
                else:
                    points = 0
            else:
                result = self.str_res_int.value()
                if int(self.strong_exercize.currentText()) in range(10, 17):
                    ex = self.exercises[int(self.strong_exercize.currentText())][self.weight_box.itemData(self.weight_box.currentIndex())]
                else:
                    ex = self.exercises[int(self.strong_exercize.currentText())]
                maximum = max(map(int, ex.keys()))
                minimum = min(map(int, ex.keys()))
                if result > maximum:
                    points = 100
                elif result < minimum:
                    points = 0
                else:
                    points = ex[str(result)]
            self.str_p.setText(str(points))
            
    def set_stamina(self):
        if self.stamina_exercize.currentText() == '29':
            self.h_layout.replaceWidget(self.stamina_res_min, self.stamina_res_int)
            self.stamina_res_min.hide()
            self.stamina_res_int.show()
        else:
            self.h_layout.replaceWidget(self.stamina_res_int, self.stamina_res_min)
            self.stamina_res_int.hide()
            self.stamina_res_min.show()
            self.stamina_res_min.setEnabled(True)
        self.stamina_calculate()
        
    def stamina_calculate(self):
        points = ''
        if self.stamina_exercize.currentText():
            if self.stamina_exercize.currentText() == '29':
                result = self.stamina_res_int.value()
                ex = self.exercises[29][self.current_age]
                maximum = max(map(int, ex.keys()))
                minimum = min(map(int, ex.keys()))
                if result > maximum:
                    points = 100
                elif result < minimum:
                    points = 0
                else:
                    points = ex[str(result)]
            else:
                res = self.stamina_res_min.time()
                result = str(res.minute()).rjust(2, '0') + ':' + str(res.second()).rjust(2, '0') + ':00'
                if int(self.stamina_exercize.currentText()) in (23, 24, 25, 26, 27, 28):
                    ex = self.exercises[int(self.stamina_exercize.currentText())][self.current_age]
                else:
                    ex = self.exercises[int(self.stamina_exercize.currentText())]
                maximum = max(ex.keys())
                minimum = min(ex.keys())
                if result < minimum:
                    points = 100
                elif result < maximum:
                    points = ex.get(result, None)
                    if not points:
                        i = 1
                        while not points:
                            sec = res.second() + i
                            if sec == 60:
                                mins = res.minute() + 1
                                sec = 0
                            else:
                                mins = res.minute()
                            result = str(mins).rjust(2, '0') + ':' + str(sec).rjust(2, '0') + ':00' 
                            points = ex.get(result, None) 
                            i += 1
                else:
                    points = 0    
            self.stamina_p.setText(str(points))
            
    def update_data(self):
        if self.fio_edit.text() in self.arr:
            if self.main_data_combo_box.currentText():
                pass_id = self.main_data_combo_box.itemData(self.main_data_combo_box.currentIndex())
                idx = self.persons[self.fio_edit.text()]
                query = """
                SELECT 
                persons.gender, 
                persons.date_of_birth
                FROM 
                persons
                WHERE 
                persons."ID" = '{}';
                """.format(idx)
                res = self.db.select(query)
                if res:
                    gender = res[0][0]
                    birthday = res[0][1]
                    years = datetime.datetime.now().year - birthday.year
                    if datetime.datetime.now().month < birthday.month:
                        years -= 1
                    elif datetime.datetime.now().month == birthday.month:
                        if datetime.datetime.now().day < birthday.day:
                            years -= 1
                    if gender == 'М':
                        self.current_age = 'O'
                        if years < 25:
                            self.group = 1
                            self.minimum = 30
                            self.points = {
                                3: 120,
                                4: 170,
                                5: 190,
                                2: 200,
                                1: 210,
                                0: 230,
                                }
                            self.current_age = 'Y'
                        elif years < 30:
                            self.group = 2
                            self.minimum = 28
                            self.points = {
                                3: 110,
                                4: 160,
                                5: 180,
                                2: 190,
                                1: 200,
                                0: 220,
                                }
                            self.current_age = 'Y'
                        elif years < 35:
                            self.group = 3
                            self.minimum = 26
                            self.points = {
                                3: 100,
                                4: 150,
                                5: 170,
                                2: 180,
                                1: 190,
                                0: 210,
                                }
                            self.current_age = 'Y'
                        elif years < 40:
                            self.group = 4
                            self.points = {
                                3: 80,
                                4: 130,
                                5: 150,
                                2: 160,
                                1: 170,
                                0: 190,
                                }
                            self.minimum = 22
                        elif years < 45:
                            self.group = 5
                            self.points = {
                                3: 70,
                                4: 110,
                                5: 130,
                                2: 140,
                                1: 150,
                                0: 160,
                                }
                            self.minimum = 20
                        elif years < 50:
                            self.group = 6
                            self.minimum = 16
                            self.points = {
                                3: 60,
                                4: 80,
                                5: 100,
                                2: 110,
                                1: 120,
                                0: 130,
                                }
                        elif years < 55:
                            self.group = 7
                            self.minimum = 12
                            self.points = {
                                3: 30,
                                4: 40,
                                5: 50,
                                2: 55,
                                1: 60,
                                0: 70,
                                }
                        elif years < 60:
                            self.group = 8
                            self.minimum = 10
                            self.points = {
                                3: 20,
                                4: 30,
                                5: 40,
                                2: 45,
                                1: 50,
                                0: 55,
                                }
                        else:
                            self.group = 9
                            self.minimum = 8
                            self.points = {
                                3: 16,
                                4: 20,
                                5: 25,
                                2: 30,
                                1: 35,
                                0: 40,
                                }
                        query = """
                        SELECT 
                        fizo_dates."{}m"
                        FROM 
                        fizo_dates
                        WHERE 
                        fizo_dates."ID" = '{}';
                        """.format(self.group, pass_id)
                        res = self.db.select(query)
                        if res:
                            if res[0][0]:
                                exercises_raw = res[0][0].split(',')
                                self.strong_exercize.clear()
                                self.stamina_exercize.clear()
                                self.speed_exercize.clear()
                                for ex in exercises_raw:
                                    if int(ex) in self.strong:
                                        self.strong_exercize.addItem(ex)
                                    elif int(ex) in self.speed:
                                        self.speed_exercize.addItem(ex)
                                    elif int(ex) in self.acc:
                                        self.speed_exercize.addItem(ex)
                                    elif int(ex) in self.stamina:
                                        self.stamina_exercize.addItem(ex)
                        self.weight_box.setEnabled(True)
                        self.set_strong()
        else:
            self.str_res_int.setDisabled(True)
            self.speed_res_sec.setDisabled(True)
            self.stamina_res_min.setDisabled(True)            
            self.weight_box.setDisabled(True)
            self.strong_exercize.clear()
            self.stamina_exercize.clear()
            self.speed_exercize.clear()
        
        
class FizoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        db = parent.db
        self.db = db
        
        self.layout = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        w = QtWidgets.QWidget()
        
        self.w_dict = {
            
            }
        
        self.current_w = None
        
        text = ''
        self.main_w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(text)
        label.setStyleSheet('text-align: justify; padding: 40px;')
        label.setWordWrap(True)
        layout.addWidget(label)
        self.main_w.setLayout(layout)
        
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Упражнения ФП'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Результаты сдачи ФП'))
        self.list_widget.setMaximumWidth(250)
        
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.main_w)
        
        #self.list_widget.itemClicked.connect(lambda: self.layout.replaceWidget(1, self.w_dict.get(self.list_widget.currentItem().text(), main_w)))
        self.list_widget.itemClicked.connect(self.change_widget)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.layout)
        w.setLayout(layout)
        self.setCentralWidget(w)
        
        self.resize(1350, 600)
        
    def change_widget(self):
        db = self.db
        if self.current_w:
            if self.current_w.ui:
                self.current_w.ui.tableWidget.save_state()
        self.w_dict = {
            'Упражнения ФП': ExercisesWidget(db),
            'Результаты сдачи ФП': FizoWidget(db),
            }
        self.current_w = self.w_dict.get(self.list_widget.currentItem().text(), None)
        self.layout.replaceWidget(1, self.w_dict.get(self.list_widget.currentItem().text(), self.main_w))
        
    def closeEvent(self, e):
        for key in self.w_dict:
            if self.w_dict[key].ui:
                self.w_dict[key].ui.tableWidget.save_state()
            
            
            
