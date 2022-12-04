# Import the required libraries
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from PIL import Image, ImageTk
from urllib.request import urlopen
from requests import Session
import json
from tkinter import END, Image
import pymysql
import requests
import urllib.request
import bs4
import base64
import io
from PIL import ImageTk, Image
import pickle


root = tk.Tk()
root.title("smiley_game")
root.geometry("1265x720+0+0")
root.resizable(False, False)

api_url = "https://marcconrad.com/uob/smile/api.php"
response = urlopen(api_url)
smileJson = json.loads(response.read())
question = smileJson['question']
solution = smileJson['solution']
link = question
# pickling solution
# file = "solution.pkl"
# fileobj = open(file, 'wb')
# pickle.dump(data, fileobj)
# fileobj.close()
# file = "solution.pkl"
# fileobj = open(file, 'rb')
# serialized = pickle.dumps(fileobj)
# answer = pickle.loads(serialized)
data = solution
serialized = pickle.dumps(data)
smiley_answer = pickle.loads(serialized)
print(smiley_answer)


class Smiley_Game:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)
        
        

        logout = Button(root, text="Log Out", command=self.logout_function, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="#d77337", fg="white", activebackground="white", bd=0)
        logout.place(x=1120, y=20, width=120)

        title = Label(root, text="Welcome to the Game",
                      font=("Impact", 36, "bold"), fg="#d77337")
        title.place(x=375, y=25)

        # Entry Input
        self.answer = Entry(root,  font=(
            "times new Roman", 14), bg="lightgray")
        self.answer.place(x=410, y=500, width=200, height=50)

        result = Button(root, text="Submit", cursor="hand2", command=self.result_function,
                        font=("times new Roman", 14), bg="#d25d17", fg="white")
        result.place(x=660, y=505, width=120)



    def get(self):
        return self.image

    def logout_function(self):
        root.destroy()
        import login

    def result_function(self):
        if self.answer.get() == smiley_answer:
            messagebox.showinfo(
                "Success", "Congratulation You Win!", parent=root)
            answer = Button(root, text="Next", cursor="hand2",
                        font=("times new Roman", 14), bg="green", fg="white")
            answer.place(x=560, y=600, width=120)
            self.answer.delete(0, END)
        elif self.answer.get() == "":
            messagebox.showerror(
                "Error", "Please submit the answer", parent=root)
        else:
            messagebox.showerror(
                "Error", "Try Again!", parent=root)
            self.answer.delete(0, END)

img = Smiley_Game(link).get()
imagelab = tk.Label(root, image=img)
imagelab.grid(padx=275, pady=120)


icon_img = PhotoImage(file="Image\icon.png")
root.iconphoto(False, icon_img)
root.mainloop()
