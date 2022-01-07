import tkinter as tk
from tkinter.constants import *
from werkzeug.security import generate_password_hash, check_password_hash
# import MySQLdb as mdb
import sqlite3
import numpy as np
import pandas as pd
import mysql.connector
from decouple import config
from sshtunnel import SSHTunnelForwarder
# import MySQLdb as db
import pymysql
pymysql.install_as_MySQLdb()


INCORRECT = 0
CORRECT = 1
INITCOLNUM = 6

def create_db(conn):
    # try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Users(
            Username VARCHAR(255) PRIMARY KEY,
            PassHash TEXT(255),
            ChineseScore INT,
            PolishScore INT,
            NumberOfQuestions INT,
            Ranking INT)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS ChineseWords(
            WordID VARCHAR(255) PRIMARY KEY,
            Chinese TEXT(255),
            CorrectAttempts INT(255),
            WrongAttempts INT(255),
            Average INT(255)
            )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS PolishWords(
            WordID VARCHAR(255) PRIMARY KEY,
            Polish TEXT(255),
            CorrectAttempts INT,
            WrongAttempts INT,
            Average INT
            )''')
            
        conn.commit()
        print("Table created successfully")
    # except:
    #     pass

def create_user(conn, userInfo):
    sql = ''' INSERT INTO Users(Username,PassHash,ChineseScore,PolishScore,NumberOfQuestions,Ranking) VALUES(%s, %s, %s, %s, %s, %s)'''
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
    
    if lang in "ChineseWordschinaChchinesei":
        lang = "ChineseWords"
        langInd = '''ChineseScore'''

    else: 
        lang = "PolishWords"
        langInd = '''PolishWords'''
    # lang = "ChineseWords"
    cur = conn.cursor()  
    cur.execute("UPDATE {} SET {} ={}+1 WHERE WordID = '{}'".format(lang,score,score,word))

    cur2 = conn.cursor()
    cur2.execute("UPDATE {} SET {} = {} WHERE WordID = '{}'".format(lang,userName,int(scoreOnQu),word))
    # print("UPDATE {} SET {} = {}+1 WHERE WordID ={}".format(lang,score,score,word))

    cur3 = conn.cursor()  
    cur3.execute("UPDATE {} SET {} ={}+1 WHERE WordID = '{}'".format(lang,score,score,word))

    cur4 = conn.cursor()  
    cur4.execute("UPDATE users SET {} ={}+1 WHERE username = '{}'".format(langInd,langInd,userName))


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
    valSql = '''VALUES(%s,%s,%s,%s'''

    for i in range(result+1):
        originalSql.append(0)
        valSql += ''',%s'''
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
        except mysql.connector.errors.IntegrityError:
            pass

def get_lang_score(conn, lang, username):
    if lang in "ChineseWordschinaChichinese":
        lang = '''ChineseWords'''
        langInd = '''ChineseScore'''
    else: 
        lang = '''PolishWords'''
        langInd = '''PolishScore'''
    score = 0
    cur3 = conn.cursor()
    try:
        cur3.execute("SELECT {} FROM users WHERE Username = '{}'".format(langInd,username))
        score = cur3.fetchone()[0]
    except:
        score=0
    return score



def main():
    # conn = sqlite3.connect('practice.db')
    # conn = mysql.connector.connect(
    # host="localhost",
    # # host=config('IP'),
    # user="root",
    # password=config('PASS'),
    # database = "learnLang"
    # )

    host = '13.236.95.148'
    localhost = '127.0.0.1'
    ssh_username = 'ubuntu'
    ss_private_key = '/Users/maxdi/OneDrive/Desktop/Website/test.key'

    user='user'
    password=config('PASS')
    database="learnLang"

    with SSHTunnelForwarder(
        (host, 22),
        ssh_username=ssh_username,
        ssh_private_key=ss_private_key,
        remote_bind_address=(localhost, 3306)
    ) as server:
        conn = db.connect(host=localhost,
                               port=server.local_bind_port,
                               user=user,
                               passwd=password,
                               db=database)

    create_db(conn)
    try:
        create_user(conn,("maxwell",generate_password_hash("password", method='sha256'),0,0,0,0))
    except mysql.connector.errors.IntegrityError:
        print("didnt work")
        pass

    create_user(conn,("max",generate_password_hash("Language123!", method='sha256'),0,0,0,0))
    
    # excel_to_sql(conn,"l")
    # insert_word(conn,"ChineseWords", "English", "Chinese")
    # insert_word(conn,"ChineseWords", "Thingo", "Chinese")

    # question_attempt(conn, "chinese", "English", CORRECT,"maxwell")
    # insert_word(conn,"ChineseWords", "Thingo", "Englishs")
    # question_attempt(conn, "ChineseWords", "Thingo", CORRECT,"maxwell")
    # cur3 = conn.cursor()

    # print(get_lang_score(conn, "chinese", "maxwell"))
    # cur3 = conn.cursor()
    # try:
    # cur3.execute("SELECT ChinsesScore FROM learnlang.users WHERE Username = 'maxwell' ")
    # score = cur3.fetchone()
    # # except:
    # #     score=0
    # print(score)


    # excel_to_sql(conn,"l")
if __name__ == '__main__':
    main()