import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = tk.Tk()
window.geometry('400x200')
window.title('Student RFID')

#Frames
main_frame = ttk.Frame(window)