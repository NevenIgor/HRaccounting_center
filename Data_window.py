from PyQt5 import QtCore, QtWidgets, QtGui
import widgets.data_forms as Widgets
import time
import threading

        
class FamilyWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)
        
        self.db = db
        
        self.ui = Widgets.Ui_family_widget()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        
        self.ui.tableWidget.id_list.clear()
        query = """
        SELECT 
        family_status.name, 
        family_status.gender
        FROM 
        family_status;

        """
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.setItem(idx, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.ui.tableWidget.id_list.append(row[-1])
        
        self.ui.tableWidget.restore()
        
    def add(self):
        sp = self.ui.lineEdit.text()
        
        query = """
        INSERT INTO family_status(
            name, gender)
        VALUES ('{}', '{}');
        """.format(sp, self.ui.comboBox.currentText())
        
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', e.pgerror, defaultButton=QtWidgets.QMessageBox.Ok)
        
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(self.ui.comboBox.currentText()))
        
        query = """SELECT "ID" FROM family_status;"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])
        
        self.ui.lineEdit.clear()
        
    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM "!_Семейное положение"
                WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', e.pgerror, defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: '"Семейное положение"',
                    #1: '"Пол"',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE "!_Семейное положение" SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()
    
    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text() + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class DivisionsWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)

        self.db = db

        self.ui = Widgets.Ui_rewards_widget('Подразделения')
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        self.ui.tableWidget.signal.connect(self.update)

        self.ui.tableWidget.id_list.clear()
        query = """
        SELECT name_full, "ID"
          FROM divisions;
        """
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.id_list.append(row[-1])

        self.ui.tableWidget.restore()

    def add(self):
        sp = self.ui.lineEdit.text()

        query = """
        INSERT INTO divisions(
            name_full)
        VALUES ('{}');
        """.format(sp)

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
            return

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))

        query = """SELECT "ID" FROM divisions;"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])

        self.ui.lineEdit.clear()

    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM divisions
    WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: 'name_full',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE divisions SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(
                        self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()

    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text() + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class PositionsWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)

        self.db = db

        self.ui = Widgets.Ui_rewards_widget('Должность')
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        self.ui.tableWidget.signal.connect(self.update)

        self.ui.tableWidget.id_list.clear()
        query = """
SELECT name_full, "ID"
  FROM positions;
"""
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.id_list.append(row[-1])

        self.ui.tableWidget.restore()

    def add(self):
        sp = self.ui.lineEdit.text()

        query = """
        INSERT INTO positions(
            name_full)
        VALUES ('{}');
        """.format(sp)

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', e.pgerror, defaultButton=QtWidgets.QMessageBox.Ok)
            return

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))

        query = """SELECT "ID" FROM positions;"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])

        self.ui.lineEdit.clear()

    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM positions
    WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', e.pgerror, defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: 'name_full',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE positions SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(
                        self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()

    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text() + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class DolgsWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)

        self.db = db

        self.ui = Widgets.Ui_rewards_widget("Тип кредитной задолжности")
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        self.ui.tableWidget.signal.connect(self.update)

        self.ui.tableWidget.id_list.clear()
        query = """
        SELECT name, "ID"
          FROM credit_types;
        """
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.id_list.append(row[-1])

        self.ui.tableWidget.restore()

    def add(self):
        sp = self.ui.lineEdit.text()

        query = """
        INSERT INTO credit_types(
            name)
        VALUES ('{}');
        """.format(sp)

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
            return

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))

        query = """SELECT "ID" FROM credit_types;"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])

        self.ui.lineEdit.clear()

    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM credit_types
    WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: 'name',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE credit_types SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(
                        self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()

    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text() + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class LgotyWidget(QtWidgets.QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent=parent)

        self.db = db

        self.ui = Widgets.Ui_rewards_widget('Вид льготы')
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        self.ui.tableWidget.signal.connect(self.update)

        self.ui.tableWidget.id_list.clear()
        query = """
        SELECT name, "ID"
          FROM lgoty;
        """
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.id_list.append(row[-1])

        self.ui.tableWidget.restore()

    def add(self):
        sp = self.ui.lineEdit.text()

        query = """
        INSERT INTO lgoty(
            name)
        VALUES ('{}');
        """.format(sp)

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
            return

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))

        query = """SELECT "ID" FROM lgoty"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])

        self.ui.lineEdit.clear()

    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM lgoty
    WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', e, defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: 'name',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE lgoty SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(
                        self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()

    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text() + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class FinancingWidget(QtWidgets.QWidget):
    """Словарь 'Финансовое обеспечение' — пункты для карточки сотрудника."""

    def __init__(self, db, parent=None):
        super().__init__(parent=parent)

        self.db = db

        self.ui = Widgets.Ui_rewards_widget('Финансовое обеспечение')
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add)
        self.ui.tableWidget.signal.connect(self.delete)
        self.ui.tableWidget.signal.connect(self.update)

        self.ui.tableWidget.id_list.clear()
        query = """
        SELECT name, "ID"
          FROM financing
         ORDER BY name ASC;
        """
        result = self.db.select(query)
        if result:
            for idx, row in enumerate(result):
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(idx, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.ui.tableWidget.id_list.append(row[-1])

        self.ui.tableWidget.restore()

    def add(self):
        sp = self.ui.lineEdit.text().strip()
        if not sp:
            return

        query = """
        INSERT INTO financing(
            name)
        VALUES ('{}');
        """.format(sp.replace("'", "''"))

        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()
            QtWidgets.QMessageBox.critical(self, 'Ошибка!', str(e), defaultButton=QtWidgets.QMessageBox.Ok)
            return

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(sp))

        query = """SELECT "ID" FROM financing"""
        self.ui.tableWidget.id_list.append(self.db.select(query)[-1][0])

        self.ui.lineEdit.clear()

    def delete(self, typ):
        if typ == 'delete':
            rows = set()
            for index in self.ui.tableWidget.selectedIndexes():
                rows.add(index.row())
            for row in list(rows)[::-1]:
                query = """
                DELETE FROM financing
                WHERE "ID" = {};
                """.format(self.ui.tableWidget.id_list[row])
                try:
                    self.db.execute(query)
                except Exception as e:
                    self.db.connection.commit()
                    QtWidgets.QMessageBox.critical(self, 'Ошибка!', str(e), defaultButton=QtWidgets.QMessageBox.Ok)
                self.ui.tableWidget.id_list.pop(row)
                self.ui.tableWidget.removeRow(row)
        elif typ == 'update':
            if self.ui.tableWidget.selectedIndexes():
                column = {
                    0: 'name',
                }
                col_n = column.get(self.ui.tableWidget.selectedIndexes()[0].column(), None)
                if col_n:
                    head = """UPDATE financing SET {} = '""".format(col_n)
                    tail = """' WHERE "ID" = {}""".format(
                        self.ui.tableWidget.id_list[self.ui.tableWidget.selectedIndexes()[0].row()])
                    item = self.ui.tableWidget.currentItem()
                    self.thread = threading.Thread(target=self.update_db, args=(head, tail, item), daemon=True)
                    self.thread.start()

    def update_db(self, head, tail, item):
        time.sleep(0.5)
        query = head + item.text().replace("'", "''") + tail
        print(query)
        try:
            self.db.execute(query)
        except Exception as e:
            self.db.connection.commit()


class DataWindow(QtWidgets.QMainWindow):
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
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Подразделения'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Должности'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Виды семейного положения'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Типы кредитной задолжности'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Льготы'))
        self.list_widget.addItem(QtWidgets.QListWidgetItem('Финансовое обеспечение'))
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
            self.current_w.ui.tableWidget.save_state()
        self.w_dict = {
            'Подразделения': DivisionsWidget(db), #DivisionWidget(db),
            'Должности': PositionsWidget(db), #PassageWidget(db),
            'Виды семейного положения': FamilyWidget(db),
            'Типы кредитной задолжности': DolgsWidget(db), #PunishWidget(db),
            'Льготы': LgotyWidget(db),  # PunishWidget(db),
            'Финансовое обеспечение': FinancingWidget(db),
            }
        self.current_w = self.w_dict.get(self.list_widget.currentItem().text(), None)
        self.layout.replaceWidget(1, self.w_dict.get(self.list_widget.currentItem().text(), self.main_w))
        
    def closeEvent(self, e):
        for key in self.w_dict:
            if self.w_dict[key].ui:
                self.w_dict[key].ui.tableWidget.save_state()
        

        
        


