import tkinter as tk
from tkinter.constants import *
from werkzeug.security import generate_password_hash, check_password_hash
# import MySQLdb as mdb
import sqlite3

TEXTCOL = "white"
BACKCOLF1 = "white"

def create_db(conn):
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS Users
            (users INT NOT NULL PRIMARY KEY,
            Username TEXT ,
            PassHash TEXT ,
            ChinsesScore INT,
            PolishScore INT,
            NumberOfQuestions INT,
            Rank INT
            );''')

        conn.execute('''CREATE TABLE IF NOT EXISTS ChineseWords (
            WordID INT NOT NULL PRIMARY KEY,
            English TEXT ,
            Chinese TEXT,
            Average INT);''')

        conn.execute('''CREATE TABLE IF NOT EXISTS PolishWords (
            WordID TEXT NOT NULL PRIMARY KEY,
            English TEXT,
            Chinese TEXT,
            Average INT);''')
            
        conn.commit()
        print("Table created successfully")
    except:
        pass
def search():
    global frame1
    global frame2

    frame1.pack_forget()
    frame2.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
def login():
    global frame1
    global frame2
    global user_input
    global pass_input
    global popup
    global LoginAttem
    global usrnam

    ## Creates a popup for if the password is wrong
    popup = tk.Tk()
    popup.title("Popup")
    popup.geometry('180x100')
    LoginAttem = ""
    LoginAttem = "Incorrect password" + '\n'
    popupLab = tk.Label(popup,text = LoginAttem, font=('courier',10))
    popupLab.place(x=20,y=20)
    popupLab.pack()
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
    input_usr = tk.Entry(frame1,textvariable=user_input,text="Username...")
    input_usr.place(x=300, y=150)
    input_usr.pack()

    password = tk.Label(frame1, bg=TEXTCOL,text = "Password:", font=('courier',10))
    password.place(x=200, y=250)
    password.pack()
    pass_input = tk.StringVar()
    input_pass = tk.Entry(frame1,textvariable=pass_input)
    input_pass.place(x=300, y=150)
    input_pass.pack()

    search_but = tk.Button(frame1,text='Login', width=12,command=login)
    search_but.place(x=250,y=300)

    # Frame2
    
    ## TODO get usrnam from database
    frame2 = tk.Frame(win, bg=BACKCOLF1)
    title_label = tk.Label(frame2,text = "Welcome "+usrnam, font=('courier',20), bg=TEXTCOL)
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

    search_but = tk.Button(frame1,text='Search', width=12,command=search)
    search_but.place(x=100,y=300)
    frame1.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
    win.mainloop()


if __name__ == '__main__':
    main()
