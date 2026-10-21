from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import datetime
import os
import threading

from Scan_window import ScanWindow
from db_API import Database as DB
import style


class PersonWidget(QtWidgets.QScrollArea):
    def __init__(self, parent, main_data):
        super(PersonWidget, self).__init__()
        widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(widget)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        self.db = parent.db

        main_layout.setSpacing(16)
        main_layout.setContentsMargins(18, 18, 18, 18)

        # фон карточек (QGroupBox) задан темой; сам скролл — прозрачный
        self.setStyleSheet('QScrollArea { border: none; background: transparent; }')

        if main_data:

            # get_data возвращает ВСЕ колонки таблицы persons в её текущем
            # составе (порядок = PRAGMA table_info) + financing_name последней.
            # Индексы вычисляются по ИМЕНАМ колонок, а не хардкодом — база
            # может иметь отличающийся набор колонок (отсюда IndexError).
            cols = getattr(self.db, '_persons_cols', None) or []
            if not cols:
                try:
                    cols = [r[1] for r in self.db.cursor.execute(
                        'PRAGMA table_info(persons)').fetchall()]
                except Exception:
                    cols = []

            def val(name, default=None):
                """Значение колонки persons по имени из кортежа main_data."""
                try:
                    i = cols.index(name)
                except ValueError:
                    return default
                if i < len(main_data) and main_data[i] is not None:
                    return main_data[i]
                return default

            def to_bool(v):
                """Любое представление флага ('True'/1/'Да'/bytes) -> bool."""
                if isinstance(v, (bytes, bytearray)):
                    v = v.decode('utf-8', 'ignore')
                if isinstance(v, str):
                    return v.strip().lower() in ('true', '1', 'да', 'yes', 'y')
                return bool(v)

            mil = to_bool(val('mil'))

            self.date_format = "%d.%m.%Y"
                        
            data = dict()
            
            data['number'] = val('lnum', '') or ''
            data['surname'] = val('second_name', '') or ''
            data['name'] = val('first_name', '') or ''
            data['patr'] = val('patr', '') or ''
            data['place_of_birth'] = val('place_of_birth', '') or ''
            data['birthday'] = val('date_of_birth')
            data['gender'] = val('gender', '') or ''
            data['nation'] = val('nation', '') or ''
            data['mobile_number'] = val('phone_num1', '') or ''
            data['mobile_number1'] = val('phone_num2', '') or ''
            data['status1'] = val('active')
            data['reg_addr'] = val('address_reg', '') or ''
            data['liv_addr'] = val('address_living', '') or ''
            data['allowance'] = val('allowance_num', '') or ''
            data['allowance_by'] = val('allowance_by', '') or ''
            data['allowance_date'] = val('allowance_date')
            fam_id = val('family_status')
            if fam_id and str(fam_id) != 'None':
                res = self.db.select("""SELECT family_status.name FROM family_status WHERE family_status."ID" = '{}';""".format(int(fam_id)))
                if res:
                    data['family_status'] = res[0][0]
            data['rank'] = val('rank', '') or ''
            # подразделение/должность/приказ — из последней по дате приказа
            # строки таблицы «Прохождение службы» (get_data подмешивает их
            # последними колонками: ..., financing_name, division, position,
            # order_by, order_date)
            sp_row = self.db.get_last_service_row(main_data[0])
            if sp_row:
                data['division'] = sp_row[0] or ''
                data['position'] = sp_row[1] or ''
                data['order_by'] = sp_row[2]
                data['order_date'] = sp_row[3]
            else:
                data['division'] = ''
                data['position'] = ''
                data['order_by'] = None
                data['order_date'] = None
            # история должностей (все записи «Прохождения службы», как история
            # классности) — показывается на главной вкладке
            def _pd(d):
                return d.strftime(self.date_format) + ' г.' if hasattr(d, 'strftime') else (str(d) if d else '—')
            data['position_history'] = [
                {
                    'position': p or '',
                    'division': dv or '',
                    'order_by': o or '',
                    'order_date': _pd(dt),
                } for p, dv, o, dt in self.db.get_service_history(main_data[0])
            ]
            data['person_buisness'] = val('person_buisness', '') or ''
            data['snils'] = val('snils', '') or ''
            data['inn'] = val('inn', '') or ''
            data['fizo_num'] = val('fizo_num', '') or ''
            # вид финансового обеспечения — доп. колонка financing_name,
            # всегда последняя в результате get_data
            data['financing'] = (main_data[-1] if cols and
                                 len(main_data) > len(cols) else '') or ''

            # Фото: раньше оно могло сохраниться как hex-строка (text), из-за
            # чего loadFromData падал с TypeError. Приводим к bytes в любом случае.
            blob = val('photo')
            if isinstance(blob, str):
                try:
                    blob = bytes.fromhex(blob.strip())
                except ValueError:
                    blob = blob.encode('utf-8', 'ignore')
            elif isinstance(blob, bytearray):
                blob = bytes(blob)
            if not isinstance(blob, bytes):
                blob = None
            
            query = '''
            SELECT 
            class.level, 
            class.order_date, 
            class.order_by, 
            class.date_passing, 
            class.actual_from, 
            class.actual_to, 
            class.vus
            FROM 
            class
            WHERE
            class."PID" = {}
            ORDER BY
            class.order_date DESC, class."ID" DESC;
            '''.format(main_data[0])
            res = self.db.select(query)
            if res:
                def f_d(d):
                    return d.strftime(self.date_format) + ' г.' if d else '—'

                row = res[0]
                data['class_level'] = str(row[0])
                data['class_order_date'] = f_d(row[1])
                data['class_order_by'] = row[2]
                data['class_date_passing'] = f_d(row[3])
                data['class_actual_from'] = f_d(row[4])
                data['class_actual_to'] = f_d(row[5])
                data['class_vus'] = row[6]
                # история предыдущих классностей (старые записи сохраняются);
                # если запись всего одна — это текущая классность, историю
                # показывать не нужно
                data['class_history'] = [
                    {
                        'level': str(r[0]),
                        'order_date': f_d(r[1]),
                        'order_by': r[2],
                        'date_passing': f_d(r[3]),
                        'actual_from': f_d(r[4]),
                        'actual_to': f_d(r[5]),
                        'vus': r[6],
                    } for r in res[1:]
                ] if len(res) > 1 else []

            first_group = QtWidgets.QGroupBox('Персональные данные')
            first_group.setObjectName('GBox')
            first_level = QtWidgets.QHBoxLayout()

            self.img_label = QtWidgets.QLabel('')
            self.img_label.setStyleSheet(
                'border: 1px solid {}; border-radius: 10px; background: {};'.format(
                    style.BORDER, style.SURFACE))
            # self.img_label.setScaledContents(True)
            pixmap = QtGui.QPixmap()
            if blob:
                try:
                    pixmap.loadFromData(blob)
                except TypeError:
                    pass  # фото повреждено — показываем пустую заглушку
            pixmap = pixmap.scaled(200, self.img_label.height(), QtCore.Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)
            self.img_label.setAlignment(QtCore.Qt.AlignCenter)
            self.img_label.setFixedWidth(200)

            p1 = QtWidgets.QVBoxLayout()
            p1.setAlignment(QtCore.Qt.AlignCenter)
            self.labels = dict()
            self.labels['person1'] = dict()
            self.labels['person1']['rank'] = QtWidgets.QLabel("<b>{}</b>".format(data['rank']))
            self.labels['person1']['surname'] = QtWidgets.QLabel("<b>{}</b>".format(data['surname']))
            self.labels['person1']['name'] = QtWidgets.QLabel("<b>{}</b>".format(data['name']))
            self.labels['person1']['patr'] = QtWidgets.QLabel("<b>{}</b>".format(data['patr']))

            self.labels['person1']['rank'].setObjectName('Name')
            self.labels['person1']['surname'].setObjectName('Name')
            self.labels['person1']['name'].setObjectName('Name')
            self.labels['person1']['patr'].setObjectName('Name')

            self.labels['person1']['rank'].setAlignment(QtCore.Qt.AlignCenter)
            self.labels['person1']['surname'].setAlignment(QtCore.Qt.AlignCenter)
            self.labels['person1']['name'].setAlignment(QtCore.Qt.AlignCenter)
            self.labels['person1']['patr'].setAlignment(QtCore.Qt.AlignCenter)
            p1.addWidget(self.labels['person1']['rank'])
            p1.addWidget(self.labels['person1']['surname'])
            p1.addWidget(self.labels['person1']['name'])
            p1.addWidget(self.labels['person1']['patr'])
            
            if data['birthday'] and hasattr(data['birthday'], 'year'):
                years = datetime.datetime.now().year - data['birthday'].year
                if datetime.datetime.now().month < data['birthday'].month:
                    years -= 1
                elif datetime.datetime.now().month == data['birthday'].month:
                    if datetime.datetime.now().day < data['birthday'].day:
                        years -= 1
            else:
                years = None

            if years is None:
                group = '—'
            elif years < 25:
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

            self.labels['person2'] = dict()
            self.labels['person2']['number'] = QtWidgets.QLabel(data['number'])
            self.labels['person2']['person_buisness'] = QtWidgets.QLabel(data['person_buisness'])
            self.labels['person2']['gender'] = QtWidgets.QLabel(data['gender'])
            if data['birthday'] and hasattr(data['birthday'], 'strftime'):
                birthday_txt = data['birthday'].strftime(self.date_format) + ' г.'
                if years is not None:
                    birthday_txt += ' - {} полных лет ({} возрастная группа)'.format(years, group)
            else:
                birthday_txt = ''
            self.labels['person2']['birthday_date'] = QtWidgets.QLabel(birthday_txt)
            self.labels['person2']['place_of_birth'] = QtWidgets.QLabel(data['place_of_birth'])
            self.labels['person2']['nation'] = QtWidgets.QLabel(data['nation'])
            self.labels['person2']['family_status'] = QtWidgets.QLabel(data.get('family_status') or '')
            self.labels['person2']['mobile_number'] = QtWidgets.QLabel(data['mobile_number'])
            self.labels['person2']['mobile_number1'] = QtWidgets.QLabel(data['mobile_number1'])
            self.labels['person2']['snils'] = QtWidgets.QLabel(data['snils'])
            self.labels['person2']['inn'] = QtWidgets.QLabel(data['inn'])
            self.labels['person2']['fizo_num'] = QtWidgets.QLabel(data['fizo_num'])
            # вид финансового обеспечения (из словаря) — показываем
            # в первой вкладке «Персональные данные»
            self.labels['person2']['financing'] = QtWidgets.QLabel(data.get('financing', '') or '—')

            form = QtWidgets.QFormLayout()
            if mil:
                form.addRow('Личный номер:', self.labels['person2']['number'])
                form.addRow('Номер личного дела:', self.labels['person2']['person_buisness'])
            form.addRow('Пол:', self.labels['person2']['gender'])
            form.addRow('Дата рождения:', self.labels['person2']['birthday_date'])
            form.addRow('Место рождения:', self.labels['person2']['place_of_birth'])
            form.addRow('Национальность:', self.labels['person2']['nation'])
            form.addRow('Семейное положение:', self.labels['person2']['family_status'])
            form.addRow('Номер телефона:', self.labels['person2']['mobile_number'])
            form.addRow('Доп. номер:', self.labels['person2']['mobile_number1'])
            form.addRow('СНИЛС:', self.labels['person2']['snils'])
            form.addRow('ИНН:', self.labels['person2']['inn'])
            form.addRow('Номерок сдачи ФП:', self.labels['person2']['fizo_num'])
            form.addRow('Финансовое обеспечение:', self.labels['person2']['financing'])

            first_level.addSpacing(30)
            first_level.addWidget(self.img_label)
            first_level.addLayout(p1)
            first_level.addLayout(form)
            first_group.setLayout(first_level)

            main_layout.addWidget(first_group)
            
            
            self.labels['passage'] = dict()

            self.labels['passage']['division'] = QtWidgets.QLabel(data.get('division', ''))
            self.labels['passage']['position'] = QtWidgets.QLabel(data.get('position', ''))
            # защита от пустых значений: order_by/order_date могут быть None (AttributeError)
            order_by = data.get('order_by') or ''
            order_date = data.get('order_date')
            if hasattr(order_date, 'strftime'):
                order_date = order_date.strftime(self.date_format)
            elif order_date:
                order_date = str(order_date)
            else:
                order_date = ''
            if order_by and order_date:
                order_text = '{} от {}'.format(order_by, order_date)
            else:
                order_text = order_by or order_date
            self.labels['passage']['order'] = QtWidgets.QLabel(order_text)

            passage_gr = QtWidgets.QGroupBox('Должность')
            passage_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            form.addRow('Подразделение: ', self.labels['passage']['division'])
            form.addRow('Должность: ', self.labels['passage']['position'])
            form.addRow('Приказ о назначении: ', self.labels['passage']['order'])

            # история должностей — отображается строчками ниже
            # (по аналогии с историей классности); если запись всего одна —
            # это текущая должность, историю показывать не нужно
            history = data.get('position_history', [])
            if len(history) > 1:
                hist_label = QtWidgets.QLabel('<b>История должностей:</b>')
                hist_label.setStyleSheet('margin-top: 8px;')
                form.addRow('', hist_label)
                for h in history:
                    txt = '{} — {}, приказ {} от {}'.format(
                        h['position'] or '—',
                        h['division'] or '—',
                        h['order_by'] or '—',
                        h['order_date'])
                    item = QtWidgets.QLabel(txt)
                    item.setStyleSheet('color: {};'.format(style.MUTED))
                    form.addRow('', item)
            passage_gr.setLayout(form)
            
            self.labels['class'] = dict()

            self.labels['class']['class'] = QtWidgets.QLabel(data.get('class_level', ''))
            self.labels['class']['class_order_date'] = QtWidgets.QLabel(data.get('class_order_date', ''))
            self.labels['class']['order'] = QtWidgets.QLabel(data.get('class_order_by', ''))
            self.labels['class']['class_date_passing'] = QtWidgets.QLabel(data.get('class_date_passing', ''))
            self.labels['class']['class_actual_from'] = QtWidgets.QLabel(data.get('class_actual_from', ''))
            self.labels['class']['class_actual_to'] = QtWidgets.QLabel(data.get('class_actual_to', ''))
            self.labels['class']['class_vus'] = QtWidgets.QLabel(data.get('class_vus', ''))

            class_gr = QtWidgets.QGroupBox('Классная квалификация')
            class_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            form.addRow('<b>Текущая классность:</b> ', self.labels['class']['class'])
            if data.get('class_level', '') != 'Нет':
                form.addRow('ВУС: ', self.labels['class']['class_vus'])
                form.addRow('Приказ: ', self.labels['class']['order'])
                form.addRow('Приказ от: ', self.labels['class']['class_order_date'])
                form.addRow('Дата сдачи: ', self.labels['class']['class_date_passing'])
                form.addRow('Действительно с: ', self.labels['class']['class_actual_from'])
                form.addRow('Действительно по: ', self.labels['class']['class_actual_to'])

            # история предыдущих классностей — отображается строчками ниже
            # (если запись всего одна — историю показывать не нужно)
            history = data.get('class_history', [])
            if len(history) > 0:
                hist_label = QtWidgets.QLabel('<b>История классности:</b>')
                hist_label.setStyleSheet('margin-top: 8px;')
                form.addRow('', hist_label)
                for h in history:
                    txt = ('{} — приказ {} от {}; ВУС {}; действ. с {} по {}'.format(
                        h['level'], h['order_by'], h['order_date'],
                        h['vus'] or '—', h['actual_from'], h['actual_to']))
                    item = QtWidgets.QLabel(txt)
                    item.setStyleSheet('color: {};'.format(style.MUTED))
                    form.addRow('', item)
            class_gr.setLayout(form)
            
            presecond_level = QtWidgets.QHBoxLayout()
            presecond_level.addWidget(passage_gr)
            if mil:
                presecond_level.addWidget(class_gr)


            second_level = QtWidgets.QHBoxLayout()
            

            self.labels['allowance'] = dict()
            _ad = data.get('allowance_date', '')
            if hasattr(_ad, 'strftime'):
                allowance_date = _ad.strftime(self.date_format) + ' г.'
            elif _ad:
                allowance_date = str(_ad)
            else:
                allowance_date = ''
            self.labels['allowance']['allowance_num'] = QtWidgets.QLabel(data.get('allowance', ''))
            self.labels['allowance']['given_by'] = QtWidgets.QLabel(data.get('allowance_by', ''))
            self.labels['allowance']['allowance_date'] = QtWidgets.QLabel(allowance_date)

            allowance_gr = QtWidgets.QGroupBox('Допуск')
            allowance_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            form.addRow('Номер допуска:', self.labels['allowance']['allowance_num'])
            form.addRow('Дата допуска:', self.labels['allowance']['allowance_date'])
            form.addRow('Кем допущен:', self.labels['allowance']['given_by'])
            allowance_gr.setAlignment(QtCore.Qt.AlignVCenter)
            allowance_gr.setLayout(form)

            lgts = {}
            query = """
            SELECT "ID", name from lgoty
            """
            result = self.db.select(query)
            if result:
                for row in result:
                    lgts[row[0]] = row[1]
            priv_gr = QtWidgets.QGroupBox('Льготы')
            priv_gr.setObjectName('GBox')
            form = QtWidgets.QVBoxLayout()
            query = '''
            SELECT 
            lgots
            FROM 
            person_lgoty
            WHERE 
            person_lgoty."PID" = {};
            '''.format(main_data[0])
            res = self.db.select(query)
            if res:
                lgots = res[-1][0].split(',')
                for el in lgots:
                    if el:
                        form.addWidget(QtWidgets.QLabel(lgts[int(el)]))
            else:
                form.addWidget(QtWidgets.QLabel('Льгот нет'))
            priv_gr.setAlignment(QtCore.Qt.AlignVCenter)
            priv_gr.setLayout(form)
            
            nis_gr = QtWidgets.QGroupBox('НИС')
            nis_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            # НИС читаем через db.get_nis(): всегда последняя запись,
            # флаги приводятся к bool ('True'/1/'Да' -> True) — раньше
            # сравнение со строкой 'True' давало инверсию «Да»/«Нет»
            nis = self.db.get_nis(main_data[0])
            if nis:
                is_user, finished, num, date_joining = nis
                if is_user:
                    form.addRow('Реализовал ипотеку: ',
                                QtWidgets.QLabel('Да' if finished else 'Нет'))
                    form.addRow('Номер НИС: ', QtWidgets.QLabel(num or ''))
                    if date_joining:
                        if hasattr(date_joining, 'strftime'):
                            dj = date_joining.strftime(self.date_format)
                        else:
                            dj = str(date_joining)
                        form.addRow('Дата включения: ',
                                    QtWidgets.QLabel(dj + ' г.'))
                else:
                    form.addRow('', QtWidgets.QLabel('Не является участником НИС'))
            else:
                form.addRow('', QtWidgets.QLabel('Нет данных'))
            nis_gr.setAlignment(QtCore.Qt.AlignVCenter)
            nis_gr.setLayout(form)

            if mil:
                second_level.addWidget(allowance_gr)
                second_level.addWidget(priv_gr)
                second_level.addWidget(nis_gr)
            else:
                presecond_level.addWidget(allowance_gr)
            
            self.labels['addres'] = dict()

            self.labels['addres']['reg'] = QtWidgets.QLabel(data.get('reg_addr', ''))
            self.labels['addres']['liv'] = QtWidgets.QLabel(data.get('liv_addr', ''))

            addres_gr = QtWidgets.QGroupBox('Адреса')
            addres_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            form.addRow('Регистрация: ', self.labels['addres']['reg'])
            form.addRow('Проживание: ', self.labels['addres']['liv'])

            addres_gr.setLayout(form)
            
            dolg_gr = QtWidgets.QGroupBox('Долги')
            dolg_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
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
            '''.format(main_data[0])
            res = self.db.select(query)
            if res:
                row = res[-1]
                form.addRow('Кредитная организация: ', QtWidgets.QLabel(row[0]))
                form.addRow('Вид кредита: ', QtWidgets.QLabel(row[1]))
                form.addRow('Сумма долга: ', QtWidgets.QLabel(row[2]))
            else:
                form.addRow('',QtWidgets.QLabel('Нет задолжностей'))
            dolg_gr.setAlignment(QtCore.Qt.AlignVCenter)
            dolg_gr.setLayout(form)
            
            auto_gr = QtWidgets.QGroupBox('Авто')
            auto_gr.setObjectName('GBox')
            form = QtWidgets.QFormLayout()
            query = '''
            SELECT
            auto.brand,
            auto.model,
            auto.gos_num,
            auto.color,
            auto.year
            FROM
            auto
            WHERE
            auto."PID" = {};
            '''.format(main_data[0])
            res = self.db.select(query)
            if res:
                row = res[-1]
                form.addRow('Марка: ', QtWidgets.QLabel(row[0] or '—'))
                form.addRow('Модель: ', QtWidgets.QLabel(row[1] or '—'))
                form.addRow('Гос. номер: ', QtWidgets.QLabel(row[2] or '—'))
                form.addRow('Цвет: ', QtWidgets.QLabel(row[3] or '—'))
                # новая графа «Год» на вкладке АВТО
                form.addRow('Год: ', QtWidgets.QLabel(str(row[4] or '—')))
            else:
                form.addRow('',QtWidgets.QLabel('Нет автомобиля'))
            auto_gr.setLayout(form)
            
            third_level = QtWidgets.QHBoxLayout()
            third_level.addWidget(dolg_gr)
            third_level.addWidget(auto_gr)
            

            main_layout.addLayout(presecond_level)
            main_layout.addLayout(second_level)
            main_layout.addLayout(third_level)
            main_layout.addWidget(addres_gr)

            for key in self.labels.keys():
                for label in self.labels[key].keys():
                    self.labels[key][label].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        else:
            pass

        self.setWidget(widget)
        self.setWidgetResizable(True)
        
        
class FIZOWidget(QtWidgets.QScrollArea):
    def __init__(self, parent, ID):
        super().__init__()
        widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(widget)
        
        level = ''
        rank = ''

        
        self.db = parent.db
        self.date_format = "%d.%m.%Y"
        
        query = '''
        SELECT act_level, rank, order_by
        FROM fizo_act
        WHERE 
        fizo_act."PID" = '{}'
        '''.format(ID)
        res = self.db.select(query)
        if res:
            level = res[-1][0] or ''
            rank = res[-1][1] or ''
            order_by = res[-1][2] or ''
        
        form = QtWidgets.QFormLayout()
        form.addRow('Уровень ФП: ', QtWidgets.QLabel(level))
        form.addRow('Спортивный разряд: ', QtWidgets.QLabel(rank))
        # новая графа «Приказ» на вкладке ФИЗО
        form.addRow('Приказ: ', QtWidgets.QLabel(order_by))
        main_layout.addLayout(form)    
        
        query = """
        SELECT 
        fizo_dates.name,
        fizo_pass.num, 
        fizo_pass.weight_group, 
        fizo_pass.speed_ex, 
        fizo_pass.speed_res, 
        fizo_pass.speed_point, 
        fizo_pass.str_ex, 
        fizo_pass.str_res, 
        fizo_pass.str_point, 
        fizo_pass.stamina_ex, 
        fizo_pass.stamina_res, 
        fizo_pass.stamina_point, 
        fizo_pass.summ, 
        fizo_pass.mark, 
        fizo_pass.level
        FROM 
        fizo_pass, 
        fizo_dates
        WHERE 
        fizo_pass."date_ID" = '{}'
        ORDER BY
        fizo_dates."ID" ASC;
        """.format(ID)
        
        self.table = QtWidgets.QTableWidget(0,15)
        self.table.setHorizontalHeaderLabels(('Сдача', 'Нагрудный\nномер', 'Весовая\nкатегория', 'Номер\nупражнения', 'Результат', 'Балл', 'Номер\nупражнения', 'Результат', 'Балл', 'Номер\nупражнения', 'Результат', 'Балл', 'Сумма\nбаллов', 'Оценка', 'Уровень'))
        #main_layout.addWidget(self.table)

        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.table.insertRow(self.table.rowCount())
                for i in range(15):
                    self.table.setItem(idx, i, QtWidgets.QTableWidgetItem(line[i]))
        
        self.setWidget(widget)
        self.setWidgetResizable(True)
        

class DocsWidget(QtWidgets.QScrollArea):
    def __init__(self, parent, ID):
        super().__init__()
        widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(widget)
        
        self.ID = ID
        self.parent = parent

        
        self.db = parent.db
        self.date_format = "%d.%m.%Y"
        
        self.table = Table(0, 7, 1)
        self.table.setHorizontalHeaderLabels(('Тип', 'Член семьи', 'Серия', 'Номер', 'Кем выдан', 'Код подразделения','Дата выдачи'))
        main_layout.addWidget(self.table)
        
        query = """
            SELECT 
            documents.type, 
            documents.name,
            documents.serial, 
            documents.num, 
            documents.given_by, 
            documents.code, 
            documents.doc_date
            FROM 
            documents
            WHERE 
            documents."PID" = '{}'
            ORDER BY
            documents.doc_date ASC;
            """.format(ID)
        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.table.setItem(idx, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2]))
                self.table.setItem(idx, 3, QtWidgets.QTableWidgetItem(line[3]))
                self.table.setItem(idx, 4, QtWidgets.QTableWidgetItem(line[4]))
                self.table.setItem(idx, 5, QtWidgets.QTableWidgetItem(line[5]))
                doc_date = line[6].strftime(self.date_format) + ' г.' if hasattr(line[6], 'strftime') else (str(line[6]) if line[6] else '')
                self.table.setItem(idx, 6, QtWidgets.QTableWidgetItem(doc_date))
                
                
        self.scroll_area = QtWidgets.QScrollArea()
        self.doc_widget = QtWidgets.QWidget()
        self.doc_layout = QtWidgets.QHBoxLayout(self.doc_widget)
        #self.doc_layout.setAlignment(QtCore.Qt.AlignTop)
        self.doc_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.doc_layout.setSpacing(20)
        self.doc_widget.setLayout(self.doc_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.doc_widget)
        
        self.add_btn = QtWidgets.QPushButton(QtGui.QIcon('./data/True.png'), 'Добавить')
        self.add_btn.clicked.connect(self.add_doc)
        
        query = """
        SELECT 
        scans.name, 
        scans.scan,
        scans."ID",
        scans."PID"
        FROM 
        scans
        WHERE 
        scans."PID" = '{}'
        """.format(ID)
        result = self.db.select(query)
        if result:
            for row in result:
                self.doc_layout.addWidget(ScanWidget(row[1], row[0], row[2], row[3], self))
        
        #self.doc_layout.addWidget(self.add_btn)
        
        
        main_layout.addWidget(self.scroll_area)
        
        
        self.setWidget(widget)
        self.setWidgetResizable(True)
        
    def add_doc(self):
        self.w = ScanWindow(self.ID, self.parent)
        self.w.setWindowTitle('Прикрепить документ')
        self.w.show()
        
        
class ServiceWidget(QtWidgets.QScrollArea):
    """Вкладка «Прохождение службы»: таблица записей о прохождении службы.

    По требованию в окне просмотра оставляем только поля
    «Должность», «Подразделение», «Приказ», «Дата приказа»."""

    HEADERS = ('Должность', 'Подразделение', 'Приказ', 'Дата приказа')

    def __init__(self, parent, ID):
        super().__init__()
        widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(widget)

        self.ID = ID
        self.parent = parent

        self.db = parent.db
        self.date_format = "%d.%m.%Y"

        self.table = Table(0, 4, 'service_passing_view_tab')
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        main_layout.addWidget(self.table)

        query = """
        SELECT
        service_passing.position,
        service_passing.division,
        service_passing.order_by,
        service_passing.order_date
        FROM
        service_passing
        WHERE
        service_passing."PID" = '{}'
        ORDER BY
        service_passing.order_date ASC;
        """.format(ID)
        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.table.insertRow(self.table.rowCount())
                for col in range(3):
                    self.table.setItem(idx, col, QtWidgets.QTableWidgetItem(str(line[col] or '')))
                _sd = line[3].strftime(self.date_format) + ' г.' if hasattr(line[3], 'strftime') else (str(line[3]) if line[3] else '')
                self.table.setItem(idx, 3, QtWidgets.QTableWidgetItem(_sd))

        self.setWidget(widget)
        self.setWidgetResizable(True)


class FamilyWidget(QtWidgets.QScrollArea):
    def __init__(self, parent, ID):
        super().__init__()
        widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(widget)

        
        self.db = parent.db
        self.date_format = "%d.%m.%Y"
        
        self.table = Table(0,5, 2)
        self.table.setHorizontalHeaderLabels(('Степень родства', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения'))
        main_layout.addWidget(self.table)
        
        query = """
        SELECT 
        family.type, 
        family.second_name, 
        family.first_name, 
        family.patr, 
        family.birthday
        FROM 
        family
        WHERE "PID"={}
        ORDER BY
        family.birthday ASC;

        """.format(ID)
        data = self.db.select(query)
        if data:
            for idx, line in enumerate(data):
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(idx, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.table.setItem(idx, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.table.setItem(idx, 2, QtWidgets.QTableWidgetItem(line[2]))
                self.table.setItem(idx, 3, QtWidgets.QTableWidgetItem(line[3]))
                fam_birthday = line[4].strftime(self.date_format) + ' г.' if hasattr(line[4], 'strftime') else (str(line[4]) if line[4] else '')
                self.table.setItem(idx, 4, QtWidgets.QTableWidgetItem(fam_birthday))
        
        self.setWidget(widget)
        self.setWidgetResizable(True)
              

class Table(QtWidgets.QTableWidget):
    def __init__(self, rows, cols, ident, parent=None):
        super().__init__(rows, cols, parent=parent)
        
        self.ident = str(ident)

        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.horizontalHeader().setSectionResizeMode(0)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setWordWrap(True)

        # кроссплатформенный каталог конфигурации (Windows: %APPDATA%, иначе ~/.config)
        conf_root = os.environ.get('APPDATA') or os.path.expanduser('~/.config')
        self.conf_dir = os.path.join(conf_root, 'HRaccounting')
        
        if not os.path.exists(self.conf_dir):
            os.makedirs(self.conf_dir, exist_ok=True)
        
        self.horizontalHeader().sectionResized.connect(self.save_state)
        
        if os.path.exists(os.path.join(self.conf_dir, self.ident)):
            with open(os.path.join(self.conf_dir, self.ident), 'rb') as f:
                self.horizontalHeader().restoreState(f.read())
        else:
            self.resizeRowsToContents()
        
    def save_state(self):
        with open(os.path.join(self.conf_dir, self.ident), 'wb') as f:
            f.write(self.horizontalHeader().saveState())
        
        
class ScanWidget(QtWidgets.QWidget):
    def __init__(self, img_bytes, name, sid, pid, parent=None):
        super().__init__(parent=parent)
        
        self.pid = pid
        self.sid = sid
        self.parent = parent
        self.db = self.parent.db
        self.name = name
        
        hbox = QtWidgets.QVBoxLayout()
        wid = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(img_bytes)
        self.pixmap = self.pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        wid.setPixmap(self.pixmap)
        hbox.addWidget(wid)
        hbox.addWidget(QtWidgets.QLabel('<center>{}</center>'.format(name)))
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        
        save_action = QtWidgets.QAction(QtGui.QIcon('./data/save.png'), 'Сохранить', self)
        delete_action = QtWidgets.QAction(QtGui.QIcon('./data/delete.png'), 'Удалить', self)
        print_action = QtWidgets.QAction(QtGui.QIcon('./data/print.png'), 'Печать', self)
        
        save_action.triggered.connect(self.save)
        delete_action.triggered.connect(self.delete_img)
        print_action.triggered.connect(self.print_img)
        
        self.context_menu = QtWidgets.QMenu()
        self.context_menu.addAction(save_action)
        self.context_menu.addAction(print_action)
        self.context_menu.addAction(delete_action)
        
        self.setLayout(hbox)
        
    def contextMenuEvent(self, e):
        self.context_menu.exec_(e.globalPos())
        
    def save(self):
        res = self.db.select('SELECT second_name, first_name, patr FROM persons WHERE "ID"={};'.format(self.pid))
        if res:
            fio = '{} {}.{}.'.format(res[0][0], res[0][1][0], res[0][2][0])
            f = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить как', self.name + ' ' + fio, 'Images (*.png *.jpg)')
            file_name = f[0]
            self.pixmap.save(file_name)
    
    def delete_img(self):
        result = QtWidgets.QMessageBox.question(self, 
                                                'Подтвердите удаление', 
                                                'Действительно удалить {}?'.format(self.name), 
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                                QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.db.execute('DELETE FROM scans WHERE "ID"={};'.format(self.sid))
            self.parent.doc_layout.removeWidget(self)
            self.close()
    
    def print_img(self):
        printer = QtPrintSupport.QPrinter()
        w = QtPrintSupport.QPrintDialog(printer)
        w.exec_()
        
        painter = QtGui.QPainter()
        painter.begin(printer)
        self.pixmap = self.pixmap.scaled(printer.width(), printer.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        
