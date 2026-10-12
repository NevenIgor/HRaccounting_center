import os
import sqlite3


class Database(object):
    def __init__(self, db):
        host = '172.30.79.12'
        db_name = db
        u_name = 'sysadmin'
        password = '1q2w3E_4r'
        
        self.connection = sqlite3.connect('employees.db',
                                            detect_types=sqlite3.PARSE_DECLTYPES |
                                            sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()

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

    def execute_n(self, query, args):
        res = self.cursor.execute(query, args)
        self.connection.commit()


    def get_data(self, person_ID):
        data = self.select("""
            SELECT 
                *
            FROM 
                persons
            WHERE 
                persons."ID" = '{}';
            """.format(person_ID))
        return data    
    
        
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

