from xml.etree import ElementTree
import zipfile
import os
import shutil
from pathlib import Path

from db_API import Database as DB


def to_zip(file_name):
    available_types = ['docx', 'pptx', 'xlsx', 'odt']
    doc_type = Path(file_name).suffix[1:]
    work_dir = os.getcwd()
    if doc_type not in available_types:
        return
    temp_doc = os.path.join(work_dir, 'templates', file_name)
    temp_folder = os.path.join(work_dir, 'templates', 'tmp')

    try:
        with zipfile.ZipFile(temp_doc, 'r') as z:
            z.extractall(temp_folder)
    except Exception as e:
        print('Err0:', e)
        return
    finally:
        return temp_doc, temp_folder


def from_zip(out_doc, temp_folder):
    try:
        shutil.make_archive(temp_folder, 'zip', temp_folder)
        os.rename(temp_folder + '.zip', out_doc)
        shutil.rmtree(temp_folder)

    except Exception as e:
        print('Err1:', e)
        

def create_doc(template, out_doc, replace_table):
    temp_doc, temp_folder = to_zip(template)

    with open(os.path.join(temp_folder, 'content.xml'), 'r') as f:
        raw_data = f.read()
    
    data = raw_data
    for key in replace_table.keys():
        data = data.replace(key, replace_table[key])

    with open(os.path.join(temp_folder, 'content.xml'), 'w') as f:
        f.write(data)
        
    from_zip(out_doc, temp_folder)
    

def generate(directory, template, person):
    db = DB('employees')
    data = db.get_data(person)
    
    if data:
        for row in data:

            replace_table = {
                '{фамилия}': row[1],
                '{имя}': row[2],
                '{отчеcтво}': row[3],
                '{личный номер}': person,
                '{дата рождения}': row[4].strftime("%d.%m.%Y"),
                '{место рождения}': row[5],
                '{национальность}': row[6],
                '{семейное положение}': row[7],
                }

            create_doc(template, os.path.join(directory, row[1] + '_' + template), replace_table)
