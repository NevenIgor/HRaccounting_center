import csv

'''
with open('1.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        for idx in range(0, len(row), 2):
            try:
                data[int(row[idx + 1])] = row[idx]  
            except:
                print(row[idx + 1], row[idx])

row = []
current = 0
for i in range(1, 101):
    if data.get(i, None):
        row.append(data[i])
    else:
        row.append('')
        
with open('total_raw.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        #writer.writerows((row, ))
'''


def get_points():

    age_depend = (17, 18, 19, 23, 24, 25, 26, 27, 28, 29, 45,)
    weight_depend = (10, 11, 12, 14, 15, 16)

    exercises = dict()
    for i in range(1, 71):
        exercises[i] = dict()


    with open('./fp/total_raw.csv', 'r') as f:
            reader = csv.reader(f)
            cur = 1
            tur = 0
            for idx, row in enumerate(reader):
                if idx == 0:
                    continue
                if cur in weight_depend:
                    if tur == 0:
                        exercises[cur]['H'] = dict()
                        exercises[cur]['M'] = dict()
                        exercises[cur]['L'] = dict()
                        for num, el in enumerate(row):
                            if el:
                                exercises[cur]['L'][el] = num + 1
                        cur -= 1
                        tur += 1
                    elif tur == 1:
                        for num, el in enumerate(row):
                            if el:
                                exercises[cur]['M'][el] = num + 1
                        cur -= 1
                        tur += 1
                    elif tur == 2:
                        for num, el in enumerate(row):
                            if el:
                                exercises[cur]['H'][el] = num + 1
                        tur = 0
                elif cur in age_depend:
                    if tur == 0:
                        exercises[cur]['Y'] = dict()
                        exercises[cur]['O'] = dict()
                        for num, el in enumerate(row):
                            if el:
                                exercises[cur]['Y'][el] = num + 1
                        cur -= 1
                        tur += 1
                    elif tur == 1:
                        for num, el in enumerate(row):
                            if el:
                                exercises[cur]['O'][el] = num + 1
                        tur = 0
                else:
                    for num, el in enumerate(row):
                        if el:
                            exercises[cur][el] = num + 1
                cur += 1
    return exercises        
    
        
