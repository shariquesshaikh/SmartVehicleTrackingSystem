from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import pymysql
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

connection = pymysql.connect(host='localhost',database='vehicle',user='root',password='')

cursor = connection.cursor()

def textFeed(plate_no,color,make,b_type,model):
    
    x=(plate_no,color,make,b_type,model)
    
    print(x)

    query = """INSERT INTO crime_record(plate_no, color, make,body_type,model) 
                   VALUES (%s,%s,%s,%s,%s) """

    
    cursor.execute(query,x)
    connection.commit()
    messagebox.showinfo("Success!","Inserted into blacklist")
    

    

