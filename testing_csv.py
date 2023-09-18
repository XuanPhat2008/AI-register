import pandas as pd
import csv

file_db = "user_db.csv"

def read_csv():
    file_data = pd.read_csv(file_db)
    with open(file_db, 'r', encoding='utf8') as f:
        for i in range(0, len(file_db)):
            print(f.readline().replace('\n', '').split(','))
        print(len(file_data))

def write_csv(all_info):
    with open(file_db, 'a', newline='\n', encoding="utf8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(all_info)

def lines():
    with open(file_db, 'r', encoding='utf8') as f:
        x = len(f.readlines())
        return x

def read_usr():
    with open(file_db, 'r', encoding='utf8') as f:
        next(f)
        x = lines() - 1
        for i in range(0, x):
            info = f.readline().replace('\n', '').split(',')
            print(info[1])
read_usr()