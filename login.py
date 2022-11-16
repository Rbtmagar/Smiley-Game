from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from tkinter import messagebox
from subprocess import call
import pymysql


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("smiley_game")
        self.root.attributes('-fullscreen', True)

        # background image
        self.bg = ImageTk.PhotoImage(file="Image/R.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=700, y=120, height=450, width=500)

        title = Label(Frame_login, text="Login Here",
                      font=("Impact", 36, "bold"), fg="#d77337", bg="white")
        title.place(x=150, y=20)

        title = Label(Frame_login, text="Log in to play Smiley Game",
                      font=("Goudy old style", 14, "bold"), fg="#d25d17", bg="white")
        title.place(x=150, y=80)

        title = Label(Frame_login, text="Username:",
                      font=("Goudy old Style", 14,))
        title.place(x=80, y=140)
        self.username = Entry(Frame_login, font=(
            "times new Roman", 15), bg="lightgray")
        self.username.place(x=80, y=180, width=350, height=35)

        title = Label(Frame_login, text="Password:",
                      font=("Goudy old Style", 14,))
        title.place(x=80, y=240)
        self.password = Entry(Frame_login, font=(
            "times new Roman", 15), bg="lightgray", show="*")
        self.password.place(x=80, y=280, width=350, height=35)

        check = Checkbutton(
            Frame_login, text="Remember password", bg="white", fg="black", bd=0, font=("times new Roman", 10))
        check.place(x=80, y=320)

        forget = Button(Frame_login, text="Forget Passoword?", bg="white",
                        fg="black", bd=0, font=("times new Roman", 10))
        forget.place(x=320, y=320)

        login = Button(Frame_login, command=self.login_function, text="Log In", bg="#d25d17",
                       fg="white", font=("times new Roman", 14))
        login.place(x=80, y=375, width=120)

        signup = Button(Frame_login, command=self.signup_function, text="Create New Account", bg="green",
                        fg="white", font=("times new Roman", 14))
        signup.place(x=225, y=375, width=200)

    def login_function(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror(
                "Error", "Username and password are required", parent=self.root)
        else:
            try:
                con = pymysql.connect(
                    host="localhost", user="root", password="", database="player")
                cur = con.cursor()
                cur.execute("select * from player where username =%s and password =%s",
                            (self.username.get(), self.password.get()))
                row = cur.fetchone()
                print(row)
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid username or password", parent=self.root)

                else:
                    self.root.destroy()
                    call(["python", "game.py"])

                con.close()

            except Exception as es:
                messagebox.showerror(
                    "Error", f"Error due to: {str(es)}", parent=self.root)

    def signup_function(self):
        self.root.destroy()
        call(["python", "register.py"])


root = Tk()
obj = Login(root)
root.mainloop()
