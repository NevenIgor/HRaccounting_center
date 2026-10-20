import os
import sqlite3
import datetime


def _to_bool(val):
    """Приводит любое хранимое представление флага (0/1, 'True'/'False',
    'Да'/'Нет', bytes, None) к bool."""
    if isinstance(val, (bytes, bytearray)):
        val = val.decode('utf-8', 'ignore')
    if isinstance(val, str):
        s = val.strip().lower()
        return s in ('true', '1', 'да', 'yes', 'y', 'и')
    return bool(val)


class Database(object):
    # имена колонок persons, данные для которых теперь берутся из последней
    # по дате приказа строки таблицы service_passing
    SERVICE_COLS = ('division', 'position', 'order_by', 'order_date')

    def __init__(self, db):
        host = '172.30.79.12'
        db_name = db
        u_name = 'sysadmin'
        password = '1q2w3E_4r'
        
        self.connection = sqlite3.connect('employees.db',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                            sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()
        self._migrate()
        # кэш имён колонок таблицы persons (состав колонок может различаться
        # в базах разных версий — индексы нельзя хардкодить)
        self._persons_cols = [r[1] for r in self.cursor.execute(
            'PRAGMA table_info(persons)').fetchall()]

    def _migrate(self):
        """Лёгкая миграция схемы: словарь финансового обеспечения + ссылка в persons."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS financing (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        ''')
        cols = [r[1] for r in self.cursor.execute('PRAGMA table_info(persons)').fetchall()]
        if 'financing' not in cols:
            self.cursor.execute('ALTER TABLE persons ADD COLUMN financing INTEGER')
        # несколько разумных пунктов по умолчанию, если словарь пуст
        cnt = self.cursor.execute('SELECT COUNT(*) FROM financing').fetchone()[0]
        if cnt == 0:
            for n in ('Федеральный бюджет', 'Внебюджетные средства',
                      'Средства бюджета субъекта РФ'):
                self.cursor.execute('INSERT INTO financing(name) VALUES (?)', (n,))
        # прохождение службы (вкладка сотрудника + окно редактирования)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_passing (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                "PID" integer,
                conventional_name character varying(100),
                actual_name character varying(200),
                division character varying(150),
                position character varying(150),
                tariff_rank character varying(50),
                staff_category character varying(50),
                order_by character varying(50),
                order_date date
            );
        ''')
        # подразделение/должность/приказ больше не хранятся в persons —
        # они берутся из последней по дате строки service_passing.
        # Колонки persons удаляются (миграция существующих баз).
        pcols = [r[1] for r in self.cursor.execute('PRAGMA table_info(persons)').fetchall()]
        obsolete = [c for c in ('division', 'position', 'order_by', 'order_date') if c in pcols]
        if obsolete:
            pk = [r[1] for r in self.cursor.execute(
                'PRAGMA table_info(persons)').fetchall() if r[5] > 0]
            pk_str = ', '.join('"{}"'.format(c) for c in pk) if pk else '"ID"'
            keep = [c for c in pcols if c not in obsolete]
            keep_str = ', '.join('"{}"'.format(c) for c in keep)
            self.cursor.execute('PRAGMA foreign_keys=OFF;')
            self.cursor.execute('ALTER TABLE persons RENAME TO persons_old;')
            self.cursor.execute(
                'CREATE TABLE persons AS SELECT {} FROM persons_old WHERE 0;'.format(keep_str))
            # восстанавливаем автоинкремент первичного ключа
            try:
                seq = self.cursor.execute(
                    "SELECT seq FROM sqlite_sequence WHERE name='persons'").fetchone()
                if seq is None:
                    mx = self.cursor.execute(
                        'SELECT MAX("ID") FROM persons_old').fetchone()[0] or 0
                    self.cursor.execute(
                        'INSERT INTO sqlite_sequence(name, seq) VALUES (?, ?)',
                        ('persons', mx))
                else:
                    self.cursor.execute('DELETE FROM sqlite_sequence WHERE name=?;', ('persons',))
                    self.cursor.execute(
                        'INSERT INTO sqlite_sequence(name, seq) VALUES (?, ?)',
                        ('persons', seq[0]))
            except Exception:
                pass
            self.cursor.execute(
                'INSERT INTO persons ({}) SELECT {} FROM persons_old;'.format(keep_str, keep_str))
            self.cursor.execute('DROP TABLE persons_old;')
            self.cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_service_passing_pid '
                'ON service_passing ("PID", order_date);')
            self.cursor.execute('PRAGMA foreign_keys=ON;')
        # ---------- нормализация данных ----------
        # 1) persons.photo: раньше фото могло сохраняться как hex-строка
        #    (ASCII), из-за чего loadFromData получал str вместо bytes.
        try:
            rows = self.cursor.execute(
                'SELECT "ID", photo FROM persons WHERE typeof(photo) = \'text\' '
                'AND photo IS NOT NULL AND photo != \'\'').fetchall()
            for rid, val in rows:
                try:
                    data = bytes.fromhex(val.strip())
                except ValueError:
                    continue
                if data:
                    self.cursor.execute(
                        'UPDATE persons SET photo = ? WHERE "ID" = ?', (data, rid))
        except Exception:
            pass
        # 2) ipoteka.user / ipoteka.finished: значения хранились вперемешку
        #    ('True'/'False', 0/1, ''/NULL) — приводим к единому виду 0/1.
        def norm_bool(col):
            cur = self.cursor.execute(
                'SELECT "ID", {} FROM ipoteka'.format(col)).fetchall()
            for rid, val in cur:
                if isinstance(val, bytes):
                    val = val.decode('utf-8', 'ignore')
                s = str(val).strip().lower() if val is not None else ''
                new = 1 if s in ('true', '1', 'да', 'yes', 'y') else 0
                if val != new:
                    self.cursor.execute(
                        'UPDATE ipoteka SET {} = ? WHERE "ID" = ?'.format(col),
                        (new, rid))
        try:
            norm_bool('"user"')
            norm_bool('finished')
        except Exception:
            pass
        # 3) ipoteka: у одного сотрудника могла накопиться пачка строк
        #    (добавление без удаления старых) — оставляем последнюю по ID.
        try:
            self.cursor.execute('''
                DELETE FROM ipoteka WHERE "ID" NOT IN (
                    SELECT MAX("ID") FROM ipoteka GROUP BY "PID");
            ''')
        except Exception:
            pass
        self.connection.commit()

    def select(self, query):
        res = self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    
    def execute(self, query):
        res = self.cursor.executescript(query)
        self.connection.commit()
        '''try:
            res = self.cursor.execute(query)
            self.connection.commit()
            return
        except Exception as e:
            return e'''

    def last_insert_id(self, table, pid=None):
        """ID последней вставленной записи (executescript не обновляет lastrowid)."""
        if pid is not None:
            q = 'SELECT MAX("ID") FROM {} WHERE PID = {}'.format(table, pid)
        else:
            q = 'SELECT MAX("ID") FROM {}'.format(table)
        res = self.select(q)
        return res[0][0] if res and res[0][0] is not None else None

    def execute_n(self, query, args):
        res = self.cursor.execute(query, args)
        self.connection.commit()


    # ---------- импорт данных из старой базы ----------
    IMPORT_TABLES = ('persons', 'auto', 'class', 'documents', 'family', 'dolg',
                     'ipoteka', 'scans', 'fizo_act', 'fizo_pass', 'person_lgoty',
                     'divisions', 'positions', 'family_status', 'credit_types',
                     'lgoty', 'fizo_dates', 'financing', 'service_passing')

    @staticmethod
    def make_backup_name():
        """Имя бекапа: текущая дата + время + backup.db"""
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_backup.db')

    def backup_current_db(self, backup_name=None):
        """Копия текущей employees.db рядом с ней. Возвращает путь к бекапу."""
        name = backup_name or self.make_backup_name()
        dst = os.path.join(os.path.dirname(os.path.abspath('employees.db')), name)
        src_con = sqlite3.connect('employees.db')
        try:
            dst_con = sqlite3.connect(dst)
            try:
                src_con.backup(dst_con)  # корректная «горячая» копия БД
            finally:
                dst_con.close()
        finally:
            src_con.close()
        return dst

    def clear_db(self):
        """Полная очистка всех таблиц текущей базы (структура сохраняется)."""
        for t in self.IMPORT_TABLES:
            exists = self.select("SELECT name FROM sqlite_master "
                                 "WHERE type='table' AND name='{}';".format(t))
            if exists:
                self.cursor.execute('DELETE FROM "{}"'.format(t))
        try:
            self.cursor.execute("DELETE FROM sqlite_sequence")
        except sqlite3.Error:
            pass  # таблицы sqlite_sequence может не существовать
        self.connection.commit()

    def _columns(self, table):
        return [r[1] for r in self.cursor.execute(
            'PRAGMA table_info("{}")'.format(table)).fetchall()]

    def import_from_file(self, file_path):
        """Переносит данные из выбранного .db в текущую (предварительно очищенную) базу.

        Совместимы только общие колонки — лишние поля старых версий игнорируются,
        недостающие заполняются NULL. Возвращает dict {таблица: кол-во строк}.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError('Файл не найден: {}'.format(file_path))
        src = sqlite3.connect(file_path,
                              detect_types=sqlite3.PARSE_DECLTYPES |
                              sqlite3.PARSE_COLNAMES)
        imported = {}
        try:
            src_tables = {r[0] for r in src.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            for t in self.IMPORT_TABLES:
                if t not in src_tables:
                    continue
                cur_exists = self.select("SELECT name FROM sqlite_master "
                                         "WHERE type='table' AND name='{}';".format(t))
                if not cur_exists:
                    continue
                src_cols = [c[1] for c in src.execute('PRAGMA table_info("{}")'.format(t))]
                dst_cols = self._columns(t)
                common = [c for c in dst_cols if c in src_cols]
                if not common:
                    continue
                rows = src.execute('SELECT "{}" FROM "{}"'.format(
                    '", "'.join(common), t)).fetchall()
                if not rows:
                    imported[t] = 0
                    continue
                placeholders = ', '.join(['?'] * len(common))
                self.cursor.executemany(
                    'INSERT INTO "{}" ("{}") VALUES ({})'.format(
                        t, '", "'.join(common), placeholders), rows)
                imported[t] = len(rows)
            # словарь финансового обеспечения есть только в новой версии —
            # если в импортируемой базе он пуст, возвращаем дефолтные пункты
            if not imported.get('financing'):
                cnt = self.cursor.execute('SELECT COUNT(*) FROM financing').fetchone()[0]
                if cnt == 0:
                    for n in ('Федеральный бюджет', 'Внебюджетные средства',
                              'Средства бюджета субъекта РФ'):
                        self.cursor.execute('INSERT INTO financing(name) VALUES (?)', (n,))
            self.connection.commit()
        finally:
            src.close()
        return imported

    def get_data(self, person_ID):
        """Возвращает список из одного кортежа со ВСЕМИ колонками таблицы
        persons (порядок = PRAGMA table_info) плюс дополнительная колонка
        financing_name в конце. Состав колонок не хардкодится — индексы
        вычисляются по имени колонки (см. col_index), поэтому ошибка
        IndexError при различиях схемы базы больше невозможна.

        Подразделение/должность/приказ/дата приказа перезаписываются
        значениями из строки таблицы «Прохождение службы» с самой поздней
        датой приказа (get_last_service_row)."""
        cols = self._persons_cols or [r[1] for r in self.cursor.execute(
            'PRAGMA table_info(persons)').fetchall()]
        sel_cols = ', '.join('p."{}"'.format(c) for c in cols)
        query = '''
            SELECT
                {},
                (SELECT name FROM financing WHERE financing."ID" = p.financing)
                    AS financing_name
            FROM
                persons p
            WHERE
                p."ID" = ?;
            '''.format(sel_cols)
        try:
            self.cursor.execute(query, (int(person_ID),))
            data = self.cursor.fetchall()
        except Exception:
            # если словарь financing отсутствует в старой базе
            self.cursor.execute(
                'SELECT {} FROM persons p WHERE p."ID" = ?;'.format(sel_cols),
                (int(person_ID),))
            data = self.cursor.fetchall()
        if not data:
            return data
        row = list(data[0])
        # самые свежие данные о службе — из последней по дате приказа строки
        sp_row = self.get_last_service_row(person_ID)
        if sp_row:
            for name, value in zip(self.SERVICE_COLS, sp_row):
                i = self.col_index(name)
                if i is not None and i < len(row):
                    row[i] = value
        return [tuple(row)]

    def col_index(self, name):
        """Индекс колонки таблицы persons по имени (None, если колонки нет)."""
        try:
            return self._persons_cols.index(name)
        except ValueError:
            return None

    def get_last_service_row(self, person_ID):
        """Строка «Прохождения службы» с самой поздней датой приказа:
        (division, position, order_by, order_date) или None.

        Записи без даты приказа считаются самыми старыми; при равных датах
        берётся более поздняя по ID запись."""
        res = self.select('''
            SELECT division, position, order_by, order_date
            FROM service_passing
            WHERE service_passing."PID" = {}
                  AND service_passing.order_date IS NOT NULL
                  AND service_passing.order_date != ''
            ORDER BY service_passing.order_date DESC,
                     service_passing."ID" DESC
            LIMIT 1;
        '''.format(int(person_ID)))
        if res:
            return res[0]
        # если ни одна запись не имеет даты приказа — берём последнюю добавленную
        res = self.select('''
            SELECT division, position, order_by, order_date
            FROM service_passing
            WHERE service_passing."PID" = {}
            ORDER BY service_passing."ID" DESC
            LIMIT 1;
        '''.format(int(person_ID)))
        return res[0] if res else None

    def get_nis(self, person_ID):
        """Актуальная запись НИС: (user, finished, number, date_joining) или None.

        user/finished возвращаются как bool (приведение 'True'/1/да -> True)."""
        res = self.select('''
            SELECT "user", finished, "number", date_joining
            FROM ipoteka
            WHERE ipoteka."PID" = {}
            ORDER BY ipoteka."ID" DESC
            LIMIT 1;
        '''.format(int(person_ID)))
        if not res:
            return None

        def to_bool(v):
            if isinstance(v, bytes):
                v = v.decode('utf-8', 'ignore')
            s = str(v).strip().lower() if v is not None else ''
            return s in ('true', '1', 'да', 'yes', 'y')

        r = res[0]
        return (to_bool(r[0]), to_bool(r[1]), r[2], r[3])

    def save_nis(self, person_ID, is_user, finished, number, date_joining):
        """Сохраняет НИС сотрудника одной актуальной строкой (INSERT OR REPLACE
        по PID), исключая накопление дублей и рассинхрон 'Да'/'Нет'."""
        self.execute_n('''
            DELETE FROM ipoteka WHERE ipoteka."PID" = ?;
            INSERT INTO ipoteka ("PID", "user", finished, "number", date_joining)
            VALUES (?, ?, ?, ?, ?);
        ''', (person_ID, person_ID,
              1 if is_user else 0,
              1 if finished else 0,
              number,
              date_joining))    
    
        
class DB(object):
    def __init__(self, host, db_name):
        
        self.connection = psycopg2.connect(host=host, dbname=db_name)
        self.cursor = self.connection.cursor()
        
    def execute(self, query):
        try:
            res = self.cursor.execute(query)
            self.connection.commit()
            data = self.cursor.fetchall()
            if data:
                return data
        except Exception as e:
            print('err: {}'.format(e))
        
def upload_photos():
    db = Database('employees')
    query = """
SELECT 
  "Сотрудники"."Личный номер"
FROM 
  public."Сотрудники";
"""
    res = db.select(query)
    for row in res:
        lnum = row[0]
        photo_db = Database('employees_csho_ss')
        query = """
SELECT 
  "Сотрудники"."Фотография"
FROM 
  public."Сотрудники"
WHERE 
  "Сотрудники"."Личный номер" = '{}'
""".format(lnum)
        data = photo_db.select(query)
        if data:
            query = """UPDATE public."Сотрудники" SET "Фотография" = {} WHERE "Сотрудники"."Личный номер" = '{}'""".format(psycopg2.Binary(data[0][0]), lnum)
            db.execute(query)
            
def insert_photos(directory):
    db = Database('employees_csho_ss')
    for root, dirs, files in os.walk(directory):
        for f in files:
            name = f.split(' ')
            sur = name[0]
            io = name[1]
            query = """
            SELECT "Личный номер", "Имя", "Отчество" FROM public."Сотрудники" WHERE "Сотрудники"."Фамилия" = '{}'""".format(sur.upper())
            
            res = db.select(query)
            for row in res:
                if row[1][0] == io[0] and row[2][0] == io[2]:
                    with open(os.path.join(directory, f), 'rb') as fl:
                        data = fl.read()
                    query = """UPDATE public."Сотрудники" SET "Фотография" = {} WHERE "Сотрудники"."Личный номер" = '{}'""".format(psycopg2.Binary(data), row[0])
                    db.execute(query)
                    print(name)
                    
            
def download_photos():
    os.mkdir('photos')
    os.chdir('photos')

    db = Database('employees_csho')
    query = """
SELECT 
  "Сотрудники"."Личный номер",
  "Сотрудники"."Фамилия",
  "Сотрудники"."Фотография"
FROM 
  public."Сотрудники"
"""
    res = db.select(query)
    for row in res:
        lnum = row[0]
        name = row[1]
        data = row[2]
        if data:
            with open('{}_{}.png'.format(lnum, name), 'wb') as f:
                f.write(data)
            print(name)

if __name__ == '__main__':
    
    upload_photos()
    #insert_photos('photos')
            
    '''with open('./4.jpg', 'rb') as f:
        data = f.read()
    query = "UPDATE person_data SET photo = '{}' WHERE profile_id = 'МТ-054752'".format(data.hex())
    db.execute(query)'''
    
    '''db = input('DB Name: ')
    db = DB('172.30.79.12', db)
    while True:
        q = input('QUERY: ')
        r = db.execute(q)
        print(r)'''

