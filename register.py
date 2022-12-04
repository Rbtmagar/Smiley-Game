# Import the required libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import call
from PIL import ImageTk
import re
import requests
import random
import smtplib
from emailverifier import Client
from emailverifier import exceptions
from validate_email import validate_email
import pymysql

# main loop


class Registration:
    def __init__(self, root):
        self.root = root
        self.root.title("registration")
        self.root.geometry("1265x720+0+0")
        self.root.resizable(False, False)

        # varibales
        self.username = StringVar()
        self.password_var = StringVar()
        self.confirm_password_var = StringVar()
        self.email_var = StringVar()
        self.agree_var = IntVar()

        # background image
        self.bg = ImageTk.PhotoImage(file="Image/R.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # frame
        Frame_register = Frame(self.root, bg="white")
        Frame_register.place(x=400, y=100, height=500, width=500)

        # label & entry
        title = Label(Frame_register, text="Register here to play smiley game", justify=CENTER,
                      font=("Impact", 18, "bold"), fg="#d77337", bg="white")
        title.place(x=50, y=20)

        title = Label(Frame_register, text="Username:",
                      font=("Goudy old Style", 14,))
        title.place(x=30, y=120)
        self.username = Entry(Frame_register, font=(
            "times new Roman", 14), bg="lightgray")
        self.username.place(x=180, y=120, width=300, height=30)

        title = Label(Frame_register, text="Password:",
                      font=("Goudy old Style", 14,))
        title.place(x=30, y=170)
        self.password = Entry(Frame_register, font=(
            "times new Roman", 14), bg="lightgray")
        self.password.place(x=180, y=170, width=300, height=30)

        title = Label(Frame_register, text="Confirm Password:",
                      font=("Goudy old Style", 14,))
        title.place(x=30, y=220)
        self.confirm_password = Entry(Frame_register, font=(
            "times new Roman", 14), bg="lightgray")
        self.confirm_password.place(x=180, y=220, width=300, height=30)

        title = Label(Frame_register, text="Email:",
                      font=("Goudy old Style", 14,))
        title.place(x=30, y=270)
        self.email = Entry(Frame_register, textvariable=self.email_var, font=(
            "times new Roman", 14), bg="lightgray")
        self.email.place(x=180, y=270, width=300, height=30)

        # button
        check = Checkbutton(Frame_register, text="I Agree To The Terms & Conditions", cursor="hand2", variable=self.agree_var, onvalue=1, offvalue=0,
                            bg="white", fg="black", bd=0, font=("times new Roman", 12))
        check.place(x=30, y=320)

        resister = Button(Frame_register, command=self.register_data, text="Resister", cursor="hand2", bg="green",
                          fg="white", font=("times new Roman", 14))
        resister.place(x=120, y=380, width=200)

        title = Label(Frame_register, text="Already a User?",
                      font=("Goudy old Style", 12,))
        title.place(x=140, y=440)

        login = Button(Frame_register, text="Log In", cursor="hand2", command=self.login,
                       font=("Helvetica 12 underline"), bd=0)
        login.place(x=250, y=440, width=60)

    # functionality

    def login(self):
        self.root.destroy()
        import login

    def clear(self):
        self.username.delete(0, END),
        self.password.delete(0, END),
        self.confirm_password.delete(0, END),
        self.email.delete(0, END),

    # checkemail
    def checkemail(self, email):
        if len(email) > 10:
            if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
                return True
            else:
                messagebox.showerror(
                    'Invalid', 'Invalid email. Enter valid email (example:xyz@gmail.com)')
                return False
        else:
            messagebox.showerror(
                "Invalid", "Enter valid email (example:xyz@gmail.com)")

    def register_data(self):
        if self.username.get() == "" or self.password.get() == "" or self.confirm_password.get() == "" or self.email.get() == "":
            messagebox.showerror(
                "Error", "All fields are required.", parent=self.root)
        elif self.password.get() != self.confirm_password.get():
            messagebox.showerror(
                "Error", "Password and confirm password doesn't match.", parent=self.root)
        elif len(self.password.get()) < 6:
            messagebox.showerror(
                "Error", "Password is too short", parent=self.root)
        elif self.email_var.get() != None:
            x = self.checkemail(self.email_var.get())
        if (x == True):
            if self.agree_var.get() == 0:
                messagebox.showerror(
                    "Error", "Please agree our terms and conditions.", parent=self.root)
            else:
                try:
                    con = pymysql.connect(
                        host="localhost", user="root", password="", database="player")
                    cur = con.cursor()

                    cur.execute("select * from player where username =%s",
                                self.username.get())
                    row = cur.fetchone()
                    print(row)
                    if row != None:
                        messagebox.showerror(
                            "Error", "User already exist, Please try with another Username", parent=self.root)

                    cur.execute("select * from player where email =%s",
                                self.email.get())
                    row = cur.fetchone()
                    print(row)
                    if row != None:
                        messagebox.showerror(
                            "Error", "Eamil already in use, Please try with another Email", parent=self.root)

                    else:
                        cur.execute("insert into player (username,password,email) values(%s,%s,%s)",
                                    (self.username.get(),
                                     self.password.get(),
                                     self.email.get()
                                     ))
                        con.commit()
                        con.close()
                        messagebox.showinfo(
                            "Success", f"Congratulaion : {self.username.get()}\nRegisteration is successful", parent=self.root)
                        self.clear()
                        self.root.destroy()
                        import login

                except Exception as es:
                    messagebox.showerror(
                        "Error", f"Error due to: {str(es)}", parent=self.root)


root = Tk()
img = PhotoImage(file="Image\icon.png")
root.iconphoto(False, img)
obj = Registration(root)
root.mainloop()
