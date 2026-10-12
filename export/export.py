import sqlite3
import csv


def f_date(date):
    dates = date.split('.')
    new_date = '-'.join(dates[::-1])
    return new_date


'''with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    header = []
    for idx, row in enumerate(reader):
        if idx == 0:
            label = row[0].split(';')
            for hidx, el in enumerate(label):
                header.append(el.replace('"', ''))'''


connection = sqlite3.connect('employees.db',
                            detect_types=sqlite3.PARSE_DECLTYPES |
                            sqlite3.PARSE_COLNAMES)
cursor = connection.cursor()


connection_old = sqlite3.connect('bd.sqlite3',
                            detect_types=sqlite3.PARSE_DECLTYPES |
                            sqlite3.PARSE_COLNAMES)
cursor_old = connection_old.cursor()

res = cursor_old.execute("SELECT * FROM data")
raw_data = cursor_old.fetchall()

query = """
DELETE FROM persons
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM class
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM person_lgoty
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM ipoteka
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM dolg
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM auto
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM family
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM fizo_act
"""
cursor.execute(query)
connection.commit()

query = """
DELETE FROM documents
"""
cursor.execute(query)
connection.commit()

for idx, el in enumerate(raw_data):
    if idx == 0:
        continue
    #for indx, elem in enumerate(el):
    #    print(indx, header[indx], elem)
    #print()


    name = el[0].split(' ')
    
    query = """
    INSERT INTO family_status ("ID") VALUES (0)
    """
    #cursor.execute(query)
    #connection.commit()
    query = """
    SELECT "ID" FROM family_status WHERE name = '{}'
    """.format(el[33].lower())
    cursor.execute(query)
    res = cursor.fetchall()
    if res:
        fs = res[0][0]
    else:
        fs = 0
        
    data = {}
    
    if name[0] == 'Кожухарова':
        data['surname'] = 'Кожухарова (Пинчук, Черненко)'
        data['name'] = 'Мария'
        data['patr'] = 'Александровна'
    else:
        data['surname'] = name[0]
        data['name'] = name[1]
        if name[0] == 'Голубев':
            data['patr'] = 'Вячеславович'
        elif name[0] == 'Антуфьев':
            data['patr'] = 'Александрович'
        else:
            data['patr'] = name[2]
    data['number'] = el[4]
    data['rank'] = el[1]
    data['birthday_date'] = f_date(el[5])
    data['place_of_birth'] = el[27]
    data['nation'] = el[26]
    data['gender'] = el[25][0].upper()
    data['family_status'] = fs
    data['mobile_number'] = el[31]
    data['mobile_number1'] = el[32]
    data['status'] = True
    data['status1'] = True
    data['division'] = el[2]
    data['position'] = el[6]
    data['order'] = el[7]
    data['order_from'] = f_date(el[8])
    data['allowance'] = el[9]
    data['allowance_by'] = el[10]
    data['allowance_date'] = f_date(el[11])
    data['reg_addr'] = el[28]
    data['liv_addr'] = el[29]
    
    query = """
        INSERT INTO persons(
            lnum, second_name, first_name, patr, place_of_birth, date_of_birth, 
            gender, nation, phone_num1, phone_num2, active, mil, address_reg, 
            address_living, allowance_num, allowance_by, allowance_date, 
            family_status, rank, division, "position", order_by, order_date)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 
                '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                '{}', '{}', '{}', '{}', 
                '{}', '{}', '{}', '{}', '{}', '{}');
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
                data['order_from']
            )
    try:
        cursor.executescript(query)

    except Exception as e:
        connection.commit()
        print(str(e))

    query = 'SELECT "ID" FROM persons'
    cursor.execute(query)
    res = cursor.fetchall()
    ident = res[-1][0]

    class_type = el[40]
    class_order = el[42] + ' от ' + el[41]
    class_order_date = f_date(el[43])
    class_start_date = f_date(el[44])
    class_finish_date = f_date(el[45])
    class_vus = el[46]

    query = ('INSERT INTO class (PID, level, order_date, order_by, date_passing, actual_from, actual_to, vus)'
             'VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
    cursor.execute(query, (ident,
                           class_type,
                           class_order_date,
                           class_order,
                           class_order_date,
                           class_start_date,
                           class_finish_date,
                           class_vus))
    connection.commit()

    lgots = ''
    if el[51] == '1':
        lgots += '5,'
    if el[52] == '1':
        lgots += '4,'
    if el[53] == '1':
        lgots += '6,'

    if lgots:
        query = ('INSERT INTO person_lgoty (PID, lgots)'
                 'VALUES (?, ?)')
        cursor.execute(query, (ident, lgots))
        connection.commit()

    if el[47] == 'Да':
        if el[48] == 'Да':
            finished = True
        else:
            finished = False
        num = el[49]
        date = f_date(el[50])

        query = ('INSERT INTO ipoteka (PID, user, finished, number, date_joining)'
                 'VALUES (?, ?, ?, ?, ?)')
        cursor.execute(query, (ident,
                               True,
                               finished,
                               num,
                               date))
        connection.commit()

    if el[55] == 'Да':
        org = el[56]
        cred_type = 5
        summ = el[58]

        query = ('INSERT INTO dolg (PID, credit_org, credit_type, summ)'
                 'VALUES (?, ?, ?, ?)')
        cursor.execute(query, (ident,
                               org,
                               cred_type,
                               summ))
        connection.commit()

    if el[59] and el[59] != '-':
        model = el[59]
        gos_num = el[60]
        org = el[61]
        polis = el[62]
        polis_start_date = f_date(el[63])
        polis_fin_date = f_date(el[64])

        query = ('INSERT INTO auto (PID, model, gos_num, agency_name, agency_num, agency_from, agency_to)'
                 'VALUES (?, ?, ?, ?, ?, ?, ?)')
        cursor.execute(query, (ident,
                               model,
                               gos_num,
                               org,
                               polis,
                               polis_start_date,
                               polis_fin_date))
        connection.commit()

    if el[34] and el[34] != '-':
        wif_name = el[34].split(' ')
        first_name = wif_name[-2]
        patr = wif_name[-1]
        sec_name = ' '.join(wif_name[:-2])
        birthday = f_date(el[35])

        query = ("INSERT INTO family (PID, type, second_name, first_name, patr, birthday)"
                 "VALUES (?, 'жена', ?, ?, ?, ?)")
        cursor.execute(query, (ident,
                               sec_name,
                               first_name,
                               patr,
                               birthday))
        connection.commit()

        level = el[38]
        rank = el[39]

        query = ('INSERT INTO fizo_act (PID, act_level, rank)'
                 'VALUES (?, ?, ?)')
        cursor.execute(query, (ident,
                               level,
                               rank))
        connection.commit()

        udost = el[13]
        udost_given_by = el[14]
        udost_given_date = f_date(el[15])

        query = ('INSERT INTO documents (PID, type, serial, num, given_by, code, doc_date)'
                 'VALUES (?, ?, ?, ?, ?, ?, ?)')

        cursor.execute(query, (ident,
                               'Удостоверение',
                               'АА',
                               udost[3:],
                               udost_given_by,
                               '',
                               udost_given_date))
        connection.commit()

        if el[16] and el[16] != '-':
            passport = el[16].replace(' № ', ' ').replace(' №', ' ').split(' ')
            pass_given_by = el[17]
            pass_given_date = f_date(el[18])
            pass_code = el[19]
            cursor.execute(query, (ident,
                                   'Паспорт',
                                   passport[0],
                                   passport[1],
                                   pass_given_by,
                                   pass_code,
                                   pass_given_date))
            connection.commit()

        if el[20] and el[20] != '-':
            passport = el[20].split(' ')
            pass_given_by = el[21]
            pass_given_date = f_date(el[22])
            pass_code = el[23]

            cursor.execute(query, (ident,
                                   'Загран. паспорт',
                                   passport[0],
                                   passport[1],
                                   pass_given_by,
                                   pass_code,
                                   pass_given_date))
            connection.commit()



    print('inserted', ' '.join(name))