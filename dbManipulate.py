import tkinter as tk
from tkinter.constants import *
from werkzeug.security import generate_password_hash, check_password_hash
# import MySQLdb as mdb
import sqlite3
import numpy as np
import pandas as pd

INCORRECT = 0
CORRECT = 1
INITCOLNUM = 6

def create_db(conn):
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS Users
            (Username TEXT NOT NULL PRIMARY KEY,
            PassHash TEXT ,
            ChinsesScore INT,
            PolishScore INT,
            NumberOfQuestions INT,
            Rank INT
            );''')

        conn.execute('''CREATE TABLE IF NOT EXISTS ChineseWords (
            WordID TEXT NOT NULL PRIMARY KEY,
            Chinese TEXT,
            CorrectAttempts INT,
            WrongAttempts INT,
            Average INT
            );''')

        conn.execute('''CREATE TABLE IF NOT EXISTS PolishWords (
            WordID TEXT NOT NULL PRIMARY KEY,
            Polish TEXT,
            CorrectAttempts INT,
            WrongAttempts INT,
            Average INT
            );''')
            
        conn.commit()
        print("Table created successfully")
    except:
        pass

def create_user(conn, userInfo):
    sql = ''' INSERT INTO Users(Username,PassHash,ChinsesScore,PolishScore,NumberOfQuestions,Rank) VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, userInfo)
    conn.commit()

    cur2 = conn.cursor()
    cur2.execute("ALTER TABLE ChineseWords ADD {} INT".format(userInfo[0]))
    conn.commit()

    cur3 = conn.cursor()
    cur3.execute("ALTER TABLE PolishWords ADD {} INT".format(userInfo[0]))
    conn.commit()

    cur4 = conn.cursor()
    cur4.execute("UPDATE PolishWords SET {} = 0".format(userInfo[0]))
    conn.commit()

    cur5 = conn.cursor()
    cur5.execute("UPDATE ChineseWords SET {} = 0".format(userInfo[0]))
    conn.commit()

def question_attempt(conn, lang, word, scoreOnQu, userName):
    if int(scoreOnQu) == INCORRECT:
        score = "WrongAttempts"
    elif int(scoreOnQu) == CORRECT:
        score = "CorrectAttempts"
    
    if lang in "ChineseWordschinaChi":
        lang = "ChineseWords"
    else: lang = "PolishWords"
    lang = "ChineseWords"
    cur = conn.cursor()  
    cur.execute("UPDATE {} SET {} ={}+1 WHERE WordID ='{}'".format(lang,score,score,word))

    cur2 = conn.cursor()
    cur2.execute("UPDATE {} SET {} = {} WHERE WordID ='{}'".format(lang,userName,int(scoreOnQu),word))
    # print("UPDATE {} SET {} = {}+1 WHERE WordID ={}".format(lang,score,score,word))
    conn.commit()

    # open the table from the 

def insert_word(conn, lang, word, transWord):
    if lang in "ChineseWordschinaChi":
        lang = '''ChineseWords'''
        langInd = '''Chinese'''
    else: 
        lang = '''PolishWords'''
        langInd = '''Polish'''

    sql = '''INSERT INTO '''+ lang + '''(WordID,''' + langInd+ ''',CorrectAttempts,WrongAttempts,Average'''

    cur = conn.cursor()
    originalSql = [word,transWord,0,0]
    cur3 = conn.cursor()
    cur3.execute("SELECT COUNT(*) from Users")
    result = cur3.fetchone()[0]
    conn.commit()

    cur4 = conn.cursor()
    cur4.execute("SELECT Username FROM Users")
    result2 = cur4.fetchall()

    for i in result2:
        '' + i[0]+ ''
        sql += ''','''+ i[0]
    sql += ''')'''
    valSql = '''VALUES(?,?,?,?'''

    for i in range(result+1):
        originalSql.append(0)
        valSql += ''',?'''
    valSql += ''')'''
    sql +=valSql
    # originalSql = [word,transWord,0,0,0]

    cur.execute(sql, tuple(originalSql))
    conn.commit()

def quiz_attempt(conn, lang, word):
    if lang in "ChineseWordschinaChi":
        lang = '''ChineseWords'''
        langInd = '''Chinese'''
    else: 
        lang = '''PolishWords'''
        langInd = '''Polish'''
    cur = conn.cursor()
    return

def excel_to_sql(conn, filename):
    excelSheet = pd.read_excel("data.xlsx")
    tupWords = excelSheet.to_numpy().tolist()
    for word in tupWords:
        try:
            insert_word(conn, "ChineseWord", word[0], word[1])
        except sqlite3.IntegrityError:
            pass


def main():
    conn = sqlite3.connect('practice.db')
    create_db(conn)
    try:
        create_user(conn,("maxwell",generate_password_hash("password", method='sha256'),0,0,0,0))
    except sqlite3.IntegrityError:
        pass
    
    # question_attempt(conn, "chinese", "'English'", INCORRECT)
    # insert_word(conn,"ChineseWords", "Things", "Englishs")
    
    # question_attempt(conn, "ChineseWords", """Thingo""", CORRECT,"maxwell")

    excel_to_sql(conn,"l")
if __name__ == '__main__':
    main()