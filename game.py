from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import call
from PIL import ImageTk
import pymysql


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("smiley_game")
        self.root.geometry("1280x720+0+0")
        self.root.resizable(False, False)

        # background image
        self.bg = ImageTk.PhotoImage(file="Image/R.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        logout = Button(root, text="Log Out",command=self.logout_function, font=(
            "Helvetica 15 underline"), bd=0)
        logout.place(x=1120, y=20, width=120)
        
        title = Label(root, text="Welcome to the Game",
                      font=("Impact", 40, "bold"), fg="#d77337", bg="white")
        title.place(x=350, y=80)
        
    def logout_function(self):
        self.root.destroy()
        call(["python", "login.py"])


root = Tk()
obj = Game(root)
root.mainloop()
