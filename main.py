import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from qtconsole.qtconsoleapp import QtCore

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui", self)
        self.title = self.getName()
        self.setWindowTitle(self.title)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)
        self.delButton.clicked.connect(self.remove)
        self.tasksListWidget.doubleClicked.connect(self.change_func)

    def getName(self):
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """select * from users where selected = 1"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        for row in records:
            gettedname = row[3]
        cursor.close()
        sqlite_connection.close()
        return gettedname

    def calendarDateChanged(self):
        print("The calendar was changed")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()
        
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date, )
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        
        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else: 
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()
        
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Info")
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()
        
    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        
        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()
        
        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)
        
        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()

    def remove(self):
        task = self.tasksListWidget.currentIndex().data()
        current_row = self.tasksListWidget.currentRow()
        if current_row >= 0:
            current_item = self.tasksListWidget.takeItem(current_row)
            del current_item

        sqlite_connection = sqlite3.connect('data.db')
        cursor = sqlite_connection.cursor()
        sql_update_query = """DELETE from tasks where task = ?"""
        cursor.execute(sql_update_query, (task, ))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()

    def change_func(self): 
        def saveTask():
            taskChange = login_entry.get()
            # colorChange = color_combobox.get()
            messagebox.showinfo('Ok','Данные были сохранены')
            # if colorChange == 'red':
            #     print(QtCore.Qt.GlobalColor.red)
            #     item = QListWidgetItem(self.tasksListWidget.currentIndex().data())
            #     item = item.setForeground(QtCore.Qt.GlobalColor.red)
            self.changeTask(taskChange, self.tasksListWidget.currentIndex().data())
            root.destroy()
        def toggle_mode():
            if mode_switch.instate(["selected"]):
                style.theme_use("forest-light")
            else:
                style.theme_use("forest-dark")
        root = tk.Tk()
        root.title('Вход')
        root.geometry('245x230+1300+350')
        style = ttk.Style(root)
        root.tk.call("source", "forest-light.tcl")
        root.tk.call("source", "forest-dark.tcl")
        style.theme_use("forest-dark")

        frame = ttk.Frame(root)
        frame.pack()
        widjets_frame = ttk.LabelFrame(frame, text='Изменить задачу')
        widjets_frame.grid(row=0, column=0, padx=20, pady=10)

        login_entry = ttk.Entry(widjets_frame)
        login_entry.insert(0, self.tasksListWidget.currentIndex().data())
        login_entry.bind("<FocusIn>", lambda e: login_entry.delete('0', 'end'))
        login_entry.grid(row=1, column=0, padx=15, pady=10,sticky="ew")

        combo_list = ['red', 'blue', 'green', 'purple', 'orange', 'black']
        color_combobox = ttk.Combobox(widjets_frame, values=combo_list)
        color_combobox.current(0)
        color_combobox.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")


        insert_button = ttk.Button(widjets_frame, text="Save", command=saveTask)
        insert_button.grid(row=3, column=0, padx=15, pady=10, sticky="nsew")

        mode_switch = ttk.Checkbutton(widjets_frame, text="Тема", style="Switch", command=toggle_mode)
        mode_switch.grid(row=4, column=0, padx=15, pady=10, sticky="nsew")

        root.mainloop()

    def changeTask(self, salary, current):
        sqlite_connection = sqlite3.connect('data.db')
        cursor = sqlite_connection.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        sql_update_query = """Update tasks set task = ? where task = ?"""
        data = (salary, current)
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        self.updateTaskList(date)
        self.taskLineEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())