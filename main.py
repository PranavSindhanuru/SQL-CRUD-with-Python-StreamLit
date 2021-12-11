import mysql.connector

db = mysql.connector.connect(
    host="localhost", 
    user="root",
    passwd="root",
    database="dbms_mini_project"
    )

mycursor = db.cursor()