# Import the required libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import call
from PIL import ImageTk
import random
import smtplib
from emailverifier import Client
from emailverifier import exceptions
from validate_email import validate_email
import pymysql
import time
import hashlib
import sys
import pickle


# main loop
class Forget_Password:
    def __init__(self, root):
        self.root = root
        self.root.title("forget_password")
        self.root.geometry("1265x720+0+0")
        self.root.resizable(False, False)
        

        # background image
        self.bg = ImageTk.PhotoImage(file="Image/R.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # frame
        Frame_forget = Frame(self.root, bg="white")
        Frame_forget.place(x=400, y=80, height=550, width=500)

        login = Button(root, text="Log In", command=self.login_function, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="#d77337", fg="white", activebackground="white", bd=0)
        login.place(x=1120, y=20, width=120)

        title = Label(Frame_forget, text="Reset Password",
                      font=("Impact", 34, "bold"), fg="#d77337")
        title.place(x=100, y=40)

        title = Label(Frame_forget, text="New Password:",
                      font=("Goudy old Style", 14,))
        title.place(x=100, y=120)
        self.new_password = Entry(Frame_forget, font=(
            "times new Roman", 14), bg="lightgray")
        self.new_password.place(x=100, y=160, width=300, height=30)

        title = Label(Frame_forget, text="Confrim Password:",
                      font=("Goudy old Style", 14,))
        title.place(x=100, y=200)
        self.confirm_password = Entry(Frame_forget, font=(
            "times new Roman", 14), bg="lightgray")
        self.confirm_password.place(x=100, y=240, width=300, height=30)

        title = Label(Frame_forget, text="Email:",
                      font=("Goudy old Style", 14,))
        title.place(x=100, y=280)
        self.email = Entry(Frame_forget, font=(
            "times new Roman", 14), bg="lightgray")
        self.email.place(x=100, y=320, width=300, height=30)

        reset = Button(Frame_forget, text="Submit", cursor="hand2", command=self.otp_pass,
                       font=("times new Roman", 14), bg="green", fg="white")
        reset.place(x=180, y=380, width=120)

    # functionality

    def login_function(self):
        self.root.destroy()
        import login

    def otp_pass(self):
        if self.email.get() == "" or self.new_password.get() == "" or self.confirm_password.get() == "":
            messagebox.showerror(
                "Error", "All fields are required.", parent=self.root)
        elif self.new_password.get() != self.confirm_password.get():
            messagebox.showerror(
                "Error", "Password and confirm password doesn't match.", parent=self.root)
        elif len(self.new_password.get()) < 6:
            messagebox.showerror(
                "Error", "Password is too short", parent=self.root)
        else:
            con = pymysql.connect(
                host="localhost", user="root", password="", database="player")
            cur = con.cursor()

            query = "select * from player where email=%s"
            cur.execute(query, (self.email.get()))
            row = cur.fetchone()
            print(row)
            if row == None:
                messagebox.showerror(
                    "Error", "Incorrect Email!", parent=self.root)
            else:
                con.commit()
                con.close()
                
                # connect to gmail server
                server = smtplib.SMTP('smtp.gmail.com', 587)  # 587: gmail port
                # transfer layer security
                server.starttls()
                server.login('sobitmagar.rbtm@gmail.com',
                             password='ltjipuebyxvjzcxs')
                # generate 4 digit otp code
                self. otp = ''.join([str(random.randint(0, 9))
                               for i in range(4)])
                # If you don't save self.otp in variable you cannot compare to the send otp code in gmail
                data = self.otp
                serialized = pickle.dumps(data)
                self.otp_verification = pickle.loads(serialized)
                msg = 'Hello, Your OTP is ' + str(self.otp)
                server.sendmail('sobitmagar.rbtm@gmail.com',
                                self.email.get(), msg)
                server.quit()
                messagebox.showinfo(
                    "Success", "Please, enter the code sent to you email.", parent=self.root)

                # otp frame
                Frame_otp = Frame(self.root, bg="white")
                Frame_otp.place(x=400, y=430, height=200, width=500)

                title = Label(Frame_otp, text="Enter the code sent to your email:",
                              font=("times new Roman", 12), fg="black")
                title.place(x=100, y=40)
                
                num=IntVar()
                self.otp = Entry(Frame_otp, textvariable=num, font=(
                    "times new Roman", 14), bg="lightgray")
                self.otp.place(x=100, y=80, width=180, height=30)

                resend = Button(Frame_otp, text="Resend", cursor="hand2", command=self.resend,
                                font=("Helvetica 14 underline"), fg="black", activebackground="white", bd=0)
                resend.place(x=300, y=80, width=100)

                confirm = Button(Frame_otp, text="Confirm", cursor="hand2", command=self.reset_password,
                                 font=("times new Roman", 14), bg="green", fg="white")
                confirm.place(x=180, y=140, width=120)

    def resend(self):
        # connect to gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # 587: gmail port
        # transfer layer security
        server.starttls()
        server.login('sobitmagar.rbtm@gmail.com',
                     password='ltjipuebyxvjzcxs')
        # generate 4 digit otp code
        self.re_otp = ''.join([str(random.randint(0, 9)) for i in range(4)])
        # If you don't save self.otp in variable you cannot compare to the send otp code in gmail
        data = self.re_otp
        serialized = pickle.dumps(data)
        self.otp_verification = pickle.loads(serialized)
        msg = 'Hello, Your OTP is ' + str(self.re_otp)
        server.sendmail('sobitmagar.rbtm@gmail.com', self.email.get(), msg)
        server.quit()
        messagebox.showinfo(
            "Success", "Sent successfully.", parent=self.root)
        self.otp.delete(0, END)

    def reset_password(self):
        if self.otp.get() == "":
            messagebox.showerror(
                "Error", "Please enter otp", parent=self.root)
        elif len(self.otp.get()) != 4:
            messagebox.showerror(
                "Error", "Please enter valid otp", parent=self.root)
            self.otp.delete(0, END)
        # elif self.otp.get() != self.otp.get():
        elif self.otp.get() != self.otp_verification:
            messagebox.showerror(
                "Error", "Please enter valid otp", parent=self.root)
            self.otp.delete(0, END)
        else:
            passwd = hashlib.sha1(bytes(self.new_password.get(), encoding='utf-8'))
            password = passwd.hexdigest()
            con = pymysql.connect(
                host="localhost", user="root", password="", database="player")
            cur = con.cursor()
            query = "update player set password=%s where email=%s"
            cur.execute(query, (password, self.email.get()))
            con.commit()
            con.close()
            messagebox.showinfo(
                "Success", "Your password is reset.\nPlease, Login with new Password.", parent=self.root)
            print(self.email.get())
            time.sleep(0)
            self.root.destroy()
            call(["python", "login.py"])
           


root = Tk()
img = PhotoImage(file="Image\icon.png")
root.iconphoto(False, img)
obj = Forget_Password(root)
root.mainloop()
