import tkinter as tk
from tkinter import ttk
from enter import enter

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
        print(name, login, password, age, gender_status)
        root.destroy()
        enter()

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
