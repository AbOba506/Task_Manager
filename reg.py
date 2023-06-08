import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from enter import enter
import re

def reg():
    def toggle_mode():
        if mode_switch.instate(["selected"]):
            style.theme_use("forest-light")
        else:
            style.theme_use("forest-dark")

    def insert_row():
        name = name_entry.get()
        login = login_entry.get()
        password = password_entry.get()
        age = int(age_spinbox.get())
        gender_status = "Man" if a.get() else "Woman"
        flag = 0
        while True:
            if (len(password)<3):
                flag = -1
                messagebox.showerror('Ошибка','B пароле должно быть не менее 3 трёх символов')
                break
            elif (len(password)>20):
                flag = -1
                messagebox.showerror('Ошибка','B пароле должно быть не более 20 символов')
                break
            elif not re.search("[a-z]", password):
                flag = -1
                messagebox.showerror('Ошибка','В пароле нет строчных латинских букв')
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                messagebox.showerror('Ошибка','В пароле нет заглавных латинских букв')
                break
            elif not re.search("[0-9]", password):
                flag = -1
                messagebox.showerror('Ошибка','В пароле нет цифр')
                break
            elif re.search("\s" , password):
                flag = -1
                messagebox.showerror('Ошибка','В пароле есть пробел')
                break
            elif (len(login)<=2):
                flag = -1
                messagebox.showerror('Ошибка','B логине должно быть не менее 3 трёх символов')
                break
            elif (len(login)>=21):
                flag = -1
                messagebox.showerror('Ошибка','B логине должно быть не более 20 символов')
                break
            elif not re.search("[a-z]", login):
                flag = -1
                messagebox.showerror('Ошибка','В логине нет строчных латинских букв')
                break
            elif not re.search("[A-Z]", login):
                flag = -1
                messagebox.showerror('Ошибка','В логине нет заглавных латинских букв')
                break
            elif re.search("\s" , login):
                flag = -1
                messagebox.showerror('Ошибка','В логине не должно быть пробелов')
                break
            else:
                while True:
                    sqlite_connection = sqlite3.connect('users.db')
                    cursor = sqlite_connection.cursor()
                    sql_select_query = """select login from users where login = ?"""
                    cursor.execute(sql_select_query, (login,))
                    records = cursor.fetchall()
                    for row in records:
                        username_in_db = row[0]
                        print(row[0])
                    if len(records) == 0:
                        break
                    cursor.close()
                    sqlite_connection.close()
                    if (login == username_in_db):
                        flag = -1
                        messagebox.showerror('Ошибка','Такой логин уже занят')
                        root.destroy()
                        enter()
            if (flag == 0):     
                db = sqlite3.connect("users.db")
                cursor = db.cursor()
                query = "INSERT INTO users(login, password, name, age, gender, selected) VALUES (?,?,?,?,?,?)"
                row = (login, password, name, age, gender_status, 0)
                cursor.execute(query, row)
                db.commit()
                cursor.close()

                root.destroy()
                enter()
                break

    root = tk.Tk()
    root.title('Регистрация')
    root.geometry('335x330+400+150')

    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    frame = ttk.Frame(root)
    frame.pack()

    widjets_frame = ttk.LabelFrame(frame, text='Поле регистрации')
    widjets_frame.grid(row=0, column=0, padx=20, pady=10)

    name_entry = ttk.Entry(widjets_frame)
    name_entry.insert(0, "Имя")
    name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    name_entry.grid(row=0, column=0, padx=5, pady=(0, 5),sticky="ew")

    login_entry = ttk.Entry(widjets_frame)
    login_entry.insert(0, "Логин")
    login_entry.bind("<FocusIn>", lambda e: login_entry.delete('0', 'end'))
    login_entry.grid(row=1, column=0, padx=5, pady=(0, 5),sticky="ew")
    
    password_entry = ttk.Entry(widjets_frame, show='*')
    password_entry.insert(0, "Пароль")
    password_entry.bind("<FocusIn>", lambda e: password_entry.delete('0', 'end'))
    password_entry.grid(row=2, column=0, padx=5, pady=(0, 5),sticky="ew")

    age_spinbox = ttk.Spinbox(widjets_frame, from_=18, to=100)
    age_spinbox.insert(0, "Возраст")
    age_spinbox.bind("<FocusIn>", lambda e: age_spinbox.delete('0', 'end'))
    age_spinbox.grid(row=3, column=0, padx=5, pady=5,sticky="ew")

    a = tk.BooleanVar()
    check_button = ttk.Checkbutton(widjets_frame, text="Мужчина", variable=a)
    check_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

    b = tk.BooleanVar()
    check_button = ttk.Checkbutton(widjets_frame, text="Женщина", variable=b)
    check_button.grid(row=4, column=0, padx=100, pady=5, sticky="nsew")

    insert_button = ttk.Button(widjets_frame, text="Продолжить", command=insert_row)
    insert_button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

    separator = ttk.Separator(widjets_frame)
    separator.grid(row=6, column=0, padx=(20, 10), pady=10, sticky="ew")

    mode_switch = ttk.Checkbutton(widjets_frame, text="Тема", style="Switch", command=toggle_mode)
    mode_switch.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

    root.mainloop()
