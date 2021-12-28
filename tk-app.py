import tkinter as tk
from tkinter.constants import *
from werkzeug.security import generate_password_hash, check_password_hash
# import MySQLdb as mdb
import sqlite3
import mysqlDbManager as db
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import mysql.connector
from decouple import config


TEXTCOL = "white"
BACKCOLF1 = "white"
INCORRECT = 0
CORRECT = 1
conn = mysql.connector.connect(
    host="localhost",
    # host=config('IP'),
    user="root",
    password=config('PASS'),
    database = "learnLang"
    )

AuthUser = "" 
Authenticated = FALSE

def search():
    global frame1
    global frame2

    frame1.pack_forget()
    frame2.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
def login():
    global frame1
    global frame2
    global pass_input
    global user_input
    global popup
    global LoginAttem
    global usrnam
    global AuthUser
    global Authenticated

    ## Creates a popup for if the password is wrong
    popup = tk.Tk()
    popup.title("Popup")
    popup.geometry('180x100')

    cleanUserName = str(user_input.get())
    errString=""
    #TODO make sure to stop SQL injection in cleanUserName
    if len(cleanUserName) < 5:
        errString = "Enter a valid Username"
    
    try:
        cur = conn.cursor()
        sqlGetUsername = '''SELECT PassHash FROM Users WHERE Username = '{}' '''.format(cleanUserName)
        cur.execute(sqlGetUsername)
        passHash = cur.fetchone()[0]
        conn.commit()
    except:
        errString = "Enter a valid Username: not in database"

    if check_password_hash(passHash, pass_input.get()):
        errString = "Welcome {}!".format(cleanUserName)
        AuthUser = cleanUserName
        Authenticated = TRUE
    else:
        errString += " Incorrect Password"

    # TODO: Change frames after a successfull login
    popupLab = tk.Label(popup,text = errString + '\n', font=('courier',10))
    popupLab.place(x=20,y=20)
    popupLab.pack()
    if Authenticated:
        frame1.pack_forget()
        frame2.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
        print(AuthUser)

    B1 = tk.Button(popup, text="Close", command = popup.destroy)
    B1.place(x=20,y=80)
    B1.pack()
    popup.mainloop()

def get_stats():
    # Get the previous stats from the quizes
    # Put the previous stats into a graph
    return

def start_quiz():
    return
    ##
def main():
    global frame1
    global frame2
    global user_input
    global pass_input
    global popup
    global LoginAttem
    global usrnam
    global AuthUser

    win = tk.Tk()
    ## The app will have four main frames
    ## Frame 1 is login: have a welcome message and a username & password input 
    ## Frame 2 is the options to view either stats or start the palm card quetions, also select language, ?maybe also style?
    ## Frame 3 is the stats 
    ## Frame 4 is the actual testing of words 

    ## Connect the whole this to a database that saves username, passwords, scores, possibly words that they got wrong 
    ## Make it possible to add new words to the app through the database, so csv into the database
    ## database with multiple tables
    ## use mysql
    win.title("Palm Cards")
    win.geometry('500x500')
    # win.resizable(False,False)

    usrnam = "USER"
    quest_number_options=[5,10,15,20,25,40,50,100]

    #Frame1
    frame1 = tk.Frame(win, bg=BACKCOLF1)
    title_label = tk.Label(frame1,text = "Welcome!", font=('courier',20), bg=TEXTCOL)
    title_label.place(x=350, y=100)
    title_label.pack(pady=10)

    explain_label = tk.Label(frame1, bg=TEXTCOL,text = "This app will teach you other languages." + '\n' + "It currently features Chinese and Polish." + '\n' + "For you progress to get tracked please login:", font=('courier',10))
    explain_label.place(x=350, y=100)
    explain_label.pack(pady=10)

    username = tk.Label(frame1, bg=TEXTCOL,text = "Username:", font=('courier',10))
    username.place(x=500, y=150)
    username.pack()
    user_input = tk.StringVar()
    input_usr = tk.Entry(frame1,textvariable=user_input)
    input_usr.place(x=300, y=150)
    input_usr.pack()

    password = tk.Label(frame1, bg=TEXTCOL,text = "Password:", font=('courier',10))
    password.place(x=200, y=250)
    password.pack()
    pass_input = tk.StringVar()
    input_pass = tk.Entry(frame1,textvariable=pass_input,show="*")
    input_pass.place(x=300, y=150)
    input_pass.pack()

    search_but = tk.Button(frame1,text='Login', width=12,command=login)
    search_but.place(x=250,y=300)

    # Frame2
    
    frame2 = tk.Frame(win, bg=BACKCOLF1)
    title_label = tk.Label(frame2,text = "Welcome "+ AuthUser, font=('courier',20), bg=TEXTCOL)
    title_label.place(x=350, y=100)
    title_label.pack(pady=10)

    get_stat = tk.Button(frame2,text='Stats', width=12,command=get_stats)
    get_stat.place(x=200,y=200)

    start_quiz = tk.Button(frame2,text='Quiz', width=12,command=search)
    start_quiz.place(x=160,y=300)

    quiz_size = tk.IntVar()
    num_quiz_quest = tk.OptionMenu(frame2,quiz_size,*quest_number_options)
    num_quiz_quest.place(x=260,y=298)

    # frame2.canvas.place(x=100,y=50)

    # search_but = tk.Button(frame1,text='Search', width=12,command=search)
    # search_but.place(x=100,y=300)

    # Frame3 Statistics
    frame3 = tk.Frame(win, bg=BACKCOLF1)
    title_label = tk.Label(frame3,text = "Statistics for Max"+ AuthUser, font=('courier',20), bg=TEXTCOL)
    title_label.place(x=350, y=100)
    title_label.pack(pady=10)

    chinesePercent = 0
    chinesePercent = db.get_lang_score(conn, "chinese", AuthUser)

    figChinese = plt.figure(figsize = (5, 5), dpi = 20)
    ax = figChinese.add_axes([0,0,1,1])
    scoreNames = ['Your Score','Average']
    scores = [4,15]
    ax.bar(scoreNames,scores)
    canvas = FigureCanvasTkAgg(figChinese, master = frame3)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,frame3)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

    frame1.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
    win.mainloop()


if __name__ == '__main__':
    main()
