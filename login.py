# It's a class that creates a login window with a background image, a frame, a title, two labels, two
# entries, two buttons, and a checkbutton

# Import the required libraries
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from subprocess import call
import time
import hashlib
import pymysql


# main loop
class Login():
    def __init__(self, root):
        self.root = root
        self.root.title("login")
        self.root.geometry("1265x720+0+0")
        self.root.resizable(False, False)

        # background image
        self.bg = ImageTk.PhotoImage(file="Image/R.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=700, y=120, height=450, width=500)

        # label & entry
        title = Label(Frame_login, text="Login Here",
                      font=("Impact", 36, "bold"), fg="#d77337", bg="white")
        title.place(x=150, y=20)

        title = Label(Frame_login, text="Log in to play Smiley Game",
                      font=("Goudy old style", 14, "bold"), fg="#d25d17", bg="white")
        title.place(x=155, y=85)

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

        # button
        self.show_pass= IntVar()
        check = Checkbutton(
            Frame_login, text="Show password",variable=self.show_pass, command=self.toggle, bg="white", fg="black", cursor="hand2", bd=0, font=("times new Roman", 10))
        check.place(x=80, y=320)

        forget = Button(Frame_login, command=self.forget_password, text="Forget Passoword?", bg="white",
                        fg="black", activebackground="white", cursor="hand2", bd=0, font=("times new Roman", 10))
        forget.place(x=320, y=320)

        login = Button(Frame_login, command=self.login_function, text="Log In", cursor="hand2", bg="#d25d17",
                       fg="white", font=("times new Roman", 14))
        login.place(x=80, y=375, width=120)

        signup = Button(Frame_login, command=self.signup_function, text="Create New Account", cursor="hand2", bg="green",
                        fg="white", font=("times new Roman", 14))
        signup.place(x=225, y=375, width=200)
    
       

    # functionality
    def toggle(self):
        if self.show_pass.get() == 1:
            self.password.config(show= '')
        else:
            self.password.config(show= '*')
            
    # this function is for reseting password
    def forget_password(self):
        self.root.destroy()
        call(["python", "forgetpassword.py"])
        

    # this function will run to game page
    def login_function(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror(
                "Error", "Username and password are required", parent=self.root)
        else:
            try:
                # connect to database
                con = pymysql.connect(
                    host="localhost", user="root", password="", database="player")
                cur = con.cursor()
                # hashing password with algorithm sha1
                passwd = hashlib.sha1(bytes(self.password.get(), encoding='utf-8'))
                password = passwd.hexdigest()
                cur.execute("select password from player where username =%s",
                            (self.username.get(),))

                row=cur.fetchone()
                if row[0] != password:
                    messagebox.showerror(
                        "Error", "Invalid username or password", parent=self.root)
                else:
                    username=self.username.get()
                    self.root.destroy()
                    call(["python", "game.py",f"{username}"])

                con.close()

            except Exception as es:
                messagebox.showerror(
                    "Error", f"Error due to: {str(es)}", parent=self.root)

    # this is the function to call registration file
    def signup_function(self):
        self.root.destroy()
        time.sleep(0)
        call(["python", "register.py"])
        

if  __name__ == '__main__':
    root=Tk()
    img=PhotoImage(file="Image\icon.png")
    root.iconphoto(False, img)
    obj=Login(root)
    root.mainloop()
