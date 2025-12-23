import sqlite3
import csv
import os


# поменять путь к файлу на нужный если не работает так
path_bd = r"/workspaces/BD_Tests/lesha_bd_3.db"


def update_database_from_excel(file_name, bd_name, table_name):
    connection = sqlite3.connect(bd_name)
    cursor = connection.cursor()
    connection.commit()
    
    file_path = f"{file_name}"
    with open(file_name, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_names = "".join(next(csv_reader)).split(";")
        print(row_names)
        print(csv_reader)
        print(table_name)
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
                    {row_names[0]} TEXT,
                    {row_names[1]} TEXT,
                    {row_names[2]} TEXT,
                    {row_names[3]} TEXT,
                    {row_names[4]} TEXT
                    )
        ''')
        connection.commit()
        print("file=done")
        for row in csv_reader:
            rspl = "".join(row).split(";")
            cursor.execute(f'INSERT INTO {table_name} ({row_names[0]}, {row_names[1]}, {row_names[2]}, {row_names[3]}, {row_names[4]}) VALUES(?, ?, ?, ?, ?)', (rspl[0], rspl[1], rspl[2], rspl[3], rspl[4]))
    connection.commit()
    connection.close()


def get_column_names(db_path, table_name):
    """Получить названия столбцов таблицы"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [column[1] for column in columns_info]
    
    conn.close()
    return column_names

def f_test(cur, mas_zav, ids):
    tests = []
    for row in cur.execute('SELECT * FROM tests'):
        for test in (row[3].split(" ")):
            for zav in (mas_zav):
                if (test == zav):
                    if row[0] not in tests:
                        print("\t \t test_id: " + row[0])
                        print("\t \t \t test_info:" + ", ".join(row))
                        tests.append(row[0])
            if (test == ids):
                if row[0] not in tests:
                        print("\t \t test_id: " + row[0])
                        print("\t \t \t test_info:" + ", ".join(row))
                        tests.append(row[0])


def check_tests(id):
    conn = sqlite3.connect(path_bd)
    cur = conn.cursor()
    
    rows = cur.fetchall()

    columns_komp = get_column_names(path_bd, "komp")
    columns_zavi = get_column_names(path_bd, "zavi")
    columns_test = get_column_names(path_bd, "tests")
    print(id + ":")
    mas_zav = []    
    for row in cur.execute('SELECT * FROM komp'):
        if row[0] == id:
            for i in range(1, 5):
                print("\t" + columns_komp[i] + ": " + row[i])

    for row in cur.execute('SELECT * FROM zavi'):
        if row[0] == id:
            print("\t" + "\t" + columns_zavi[1] + ": " + row[1])
            mas_zav.append(row[1])
            for i in range(2, 5):
                print("\t" + "\t" + "\t" + columns_zavi[i] + ": " + row[i])
    print("test_cases:")
    f_test(cur, mas_zav, id)
    
    

# update_database_from_excel(r"C:\Users\Xiaomi\OneDrive\Рабочий стол\леша_бд\компонетны.csv", path_bd, "komp")
# update_database_from_excel(r"C:\Users\Xiaomi\OneDrive\Рабочий стол\леша_бд\2_зависимости.csv", path_bd,"zavi")
# update_database_from_excel(r"C:\Users\Xiaomi\OneDrive\Рабочий стол\леша_бд\test_case.csv", path_bd,"tests")
while True:
    print("write ID:")
    inp = input()
    if inp == "1":
        break
    check_tests(inp)

