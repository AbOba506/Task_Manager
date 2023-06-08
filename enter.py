import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from main import Window
from PyQt5.QtWidgets import QApplication
import sys

def enter():
    def toggle_mode():
        if mode_switch.instate(["selected"]):
            style.theme_use("forest-light")
        else:
            style.theme_use("forest-dark")

    def insert_row():
        login = login_entry.get()
        password = password_entry.get()
        s1 = 0
        s2 = 0
        while True:
            sqlite_connection = sqlite3.connect('users.db')
            cursor = sqlite_connection.cursor()
            sql_select_query = """select * from users where login = ?"""
            cursor.execute(sql_select_query, (login,))
            records = cursor.fetchall()
            for row in records:
                username_in_db = row[1]
                password_in_bd = row[2]
            if len(records) == 0:
                break
            cursor.close()
            sqlite_connection.close()
            if (login == username_in_db and password == password_in_bd):
                db = sqlite3.connect("users.db")
                cursor = db.cursor()
                query = "UPDATE users SET selected = 1 WHERE login = ?"
                row = (login,)
                cursor.execute(query, row)
                db.commit()
                root.destroy()
                s1 = 1
                app = QApplication(sys.argv)
                window = Window()
                window.show()
                sys.exit(app.exec())
            else:
                s2 = 0
        if (s1 == 0 and s2 ==0 ):
            messagebox.showerror('Ошибка','Неправильный логин или пароль')

    root = tk.Tk()
    root.title('Вход')
    root.geometry('200x215+500+150')

    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    frame = ttk.Frame(root)
    frame.pack()

    widjets_frame = ttk.LabelFrame(frame, text='Поле входа')
    widjets_frame.grid(row=0, column=0, padx=20, pady=10)

    login_entry = ttk.Entry(widjets_frame)
    login_entry.insert(0, "Логин")
    login_entry.bind("<FocusIn>", lambda e: login_entry.delete('0', 'end'))
    login_entry.grid(row=1, column=0, padx=5, pady=(0, 5),sticky="ew")

    password_entry = ttk.Entry(widjets_frame, show='*')
    password_entry.insert(0, "Пароль")
    password_entry.bind("<FocusIn>", lambda e: password_entry.delete('0', 'end'))
    password_entry.grid(row=2, column=0, padx=5, pady=(0, 5),sticky="ew")

    insert_button = ttk.Button(widjets_frame, text="Продолжить", command=insert_row)
    insert_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

    separator = ttk.Separator(widjets_frame)
    separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

    mode_switch = ttk.Checkbutton(widjets_frame, text="Тема", style="Switch", command=toggle_mode)
    mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")