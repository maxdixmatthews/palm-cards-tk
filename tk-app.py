import tkinter as tk


def search(frame1,frame2):
    frame1.pack_forget()
    frame2.pack()
def main():
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
    win.geometry('1000x1000')
    win.resizable(False,False)
    frame1 = tk.Frame(height=1000,width=1000, bg="green")
    frame1.canvas = tk.Canvas(frame1,width=1000,height=1000)
    frame1.canvas.place(x=1000,y=1000)

    tag_label = tk.Label(frame1,text = "Enter Search Tag:", font=('courier',12))
    tag_label.place(x=350, y=100)
    tag_label.pack(pady=10)

    frame2 = tk.Frame(win, bg="red")
    frame2.canvas = tk.Canvas(win,width=780,height=850)
    frame2.canvas.place(x=100,y=50)

    search_but = tk.Button(win,text='Search', width=12,command=search(frame1,frame2))
    search_but.pack()
    frame1.pack()
    win.mainloop()


if __name__ == '__main__':
    main()
