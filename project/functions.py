import os
import tkinter as tk
from tkinter import filedialog
import sqlite3
import csv
import pandas as pd
import hashlib


# curatare ecran
def clear(f):
    for w in f.winfo_children():
        w.destroy()


def fetch_db(com, user_input, pass_input):
    connection = sqlite3.connect("timetabling.db")
    cursor = connection.cursor()
    result = ""

    if com == "login":
        cursor.execute(f"select * from users where username=(?)", (user_input,))
        table_content = cursor.fetchall()

        if table_content:
            if hashlib.md5(pass_input.encode()).hexdigest() == table_content[0][2]:
                result = user_input
        else:
            result = ""
    elif com == "create":
        cursor.execute(f"select * from users where username=(?)", (user_input,))
        table_content = cursor.fetchall()

        if table_content:
            result = ""
        else:
            # id crescator
            count = 0
            for _ in cursor.execute("select * from users"):
                count += 1

            password = pass_input.encode()
            password = hashlib.md5(password)
            password = password.hexdigest()
            user_data = (count - 1, user_input, password)
            rows = cursor.execute("insert into users values (?,?,?)", user_data)

            if rows:
                result = user_input

    connection.commit()
    connection.close()
    return result


def file_to_db(file_path):
    connection = sqlite3.connect("timetabling.db")
    cursor = connection.cursor()

    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)

    sql_delete_query = "delete from classes where id >= 0"
    cursor.execute(sql_delete_query)
    connection.commit()

    for row in df.itertuples():
        row_list = [row[1], row[2], row[3], row[4]]
        cursor.execute("insert into classes values (?,?,?,?)", row_list)

    connection.commit()
    connection.close()


def get_export_list():
    connection = sqlite3.connect("timetabling.db")
    cursor = connection.cursor()

    export_list = []
    for row in cursor.execute("select * from classes"):
        temp_list = [row[1], row[2], row[3]]
        export_list.append(temp_list)

    connection.close()
    return export_list


def save_file(export_list):
    # print(export_list)
    f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    else:
        f1 = open(f.name, 'w', encoding='UTF8', newline='')
        writer = csv.writer(f1)
        header = ["id", "name", "day", "hour"]
        writer.writerow(header)
        for idx, row in enumerate(export_list):
            row = list(row)
            row.insert(0, idx)
            writer.writerow(row)
            # print(row)
        f1.close()
    f.close()


def add_class(class_listbox, item_class, day_select, hour_select, export_list):
    # listbox management - partea vizuala
    if day_select[0] == "M":
        box_item = item_class + " (" + day_select[:2] + ", " + hour_select + ")"
    else:
        box_item = item_class + " (" + day_select[0] + ", " + hour_select + ")"

    class_listbox.insert(class_listbox.size() + 1, box_item)

    class_tuple = list((item_class, day_select, hour_select))
    export_list.append(class_tuple)


def remove_class(class_listbox, selection, export_list):
    # listbox management - partea vizuala
    DAYS = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
    for item in selection:
        item = str(class_listbox.get(item))
        first = item.rfind('(') - 1
        name = item[0:first]

        day = item[first+2]
        if str(day) == "M":
            day = item[(first+2):(first+4)]
        last = item.rfind(')')
        hour = item[(last-11):last]

        for d in DAYS:
            if d.find(day) == 0:
                day = d

        class_tuple = list((str(name), str(day), str(hour)))
        export_list.remove(class_tuple)
        idx = class_listbox.get(0, tk.END).index(item)
        class_listbox.delete(idx)


def operate_classes(f2, class_listbox, export_list):
    file_path = search_for_file_path(f2)
    if file_path:
        file_to_db(file_path)

        connection = sqlite3.connect("timetabling.db")
        cursor = connection.cursor()

        for row in cursor.execute("select * from classes"):
            temp_list = [row[1], row[2], row[3]]
            export_list.append(temp_list)

        connection.close()

        for entry in export_list:
            if entry[1][0] == "M":
                box_item = entry[0] + " (" + entry[1][:2] + ", " + entry[2] + ")"
            else:
                box_item = entry[0] + " (" + entry[1][0] + ", " + entry[2] + ")"

            class_listbox.insert(class_listbox.size() + 1, box_item)


def search_for_file_path(f2):
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent=f2, initialdir=currdir, title="Selectează fișier")
    return tempdir


def call_algorithm(export_list, type):
    # probabil o functie pentru tot acest proces
    v = len(export_list)

    q = []
    for c in export_list:
        if c[0] not in q:
            q.append(c[0])
    q = len(q)

    e = 0
    for x in range(0, v - 1):
        for y in range(x + 1, v):
            if (export_list[x][1] == export_list[y][1]) and (export_list[x][2] == export_list[y][2]):
                e += 1

    # print("|V| = " + str(v) + ", |E| = " + str(e) + ", |Q| = " + str(q))

    f = open('input.txt', "w")
    f.write(str(v) + " " + str(e) + " " + str(q) + '\n')

    part_count = 0
    # print(part_count)
    f.write(str(part_count) + '\n')
    for i in range(1, v):
        if export_list[i][0] != export_list[i - 1][0]:
            part_count += 1
            # print(part_count)
            f.write(str(part_count) + '\n')
        else:
            # print(part_count)
            f.write(str(part_count) + '\n')

    e_copy = 0
    for x in range(0, v - 1):
        for y in range(x + 1, v):
            if (export_list[x][1] == export_list[y][1]) and (export_list[x][2] == export_list[y][2]):
                e_copy += 1
                # print(str(x) + " " + str(y) + " adica " + export_list[x][0] + " " + export_list[x][1] + " " +
                #       export_list[x][2] + " si " + export_list[y][0] + " " + export_list[y][1] + " " + export_list[y][
                #           2])
                f.write(str(x) + " " + str(y))
                if e_copy < e:
                    f.write('\n')

    f.close()

    # generare raspuns
    if type == 1:
        os.system('python ACO.py')
    else:
        os.system('python TS.py')
