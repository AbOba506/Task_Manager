import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from enter import enter
import re

conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    login TEXT,
    password TEXT,
    name TEXT,
    age INT,
    gender TEXT,
    selected INTEGER);
""")
conn.commit()
