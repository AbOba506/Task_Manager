import tkinter as tk
from tkinter import ttk
from reg import reg
from enter import enter

def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

def registration():
    root.destroy()
    reg()
    
def ent():
    root.destroy()
    enter()

root = tk.Tk()
root.title('Авторизация')
root.geometry('170x160+500+150')

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

widjets_frame = ttk.LabelFrame(frame, text='Поле авторизации')
widjets_frame.grid(row=0, column=0, padx=20, pady=10)

insert_button = ttk.Button(widjets_frame, text="Регистрация", command=registration)
insert_button.grid(row=4, column=0, padx=15, pady=5, sticky="nsew")

insert_button = ttk.Button(widjets_frame, text="Вход", command=ent)
insert_button.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")

mode_switch = ttk.Checkbutton(widjets_frame, text="Тема", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

root.mainloop()