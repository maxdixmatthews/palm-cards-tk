import tkinter as tk
from tkinter.constants import *
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb as mdb

TEXTCOL = "white"
BACKCOLF1 = "white"
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

    ##
def main():
    global frame1
    global frame2
    global user_input
    global pass_input
    global popup
    global LoginAttem
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
    frame2 = tk.Frame(win, bg="white")
    frame2.canvas = tk.Canvas(win,width=780,height=850)
    # frame2.canvas.place(x=100,y=50)

    search_but = tk.Button(frame1,text='Search', width=12,command=search)
    search_but.place(x=100,y=300)
    frame1.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)
    win.mainloop()


if __name__ == '__main__':
    main()
