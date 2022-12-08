# It creates a GUI that displays a smiley face and asks the user to guess the emotion. 
# The user has 20 seconds to answer. 
# If the user answers correctly, the score increases by 1. 
# If the user answers incorrectly, the score remains the same. 
# The user can log out at any time. 
# The user's score is displayed at the bottom of the GUI.
# Import the required libraries
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from PIL import Image, ImageTk
from urllib.request import urlopen
import json
from tkinter import END, Image
import urllib.request
import base64
import io
from PIL import ImageTk, Image
import time
import sys


root = tk.Tk()
root.title("smiley_game")
root.geometry("1265x720+0+0")
root.resizable(False, False)


class Smiley_Game:
    def __init__(self, ques, soln) :
        self.ques = ques
        self.soln = soln
        self.score = 0
        self.username = sys.argv[1]
        self.imagelab = tk.Label(root)
        self.imagelab.grid(padx=275, pady=130)
        
       
        # logout button
        logout = Button(root, text="Log Out", command=self.logout_function, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="#d77337", fg="white", activebackground="white", bd=0)
        logout.place(x=1120, y=20, width=120)

        # label
        title = Label(root, text=f"Welcome {self.username}",
                      font=("Impact", 36, "bold"), fg="#d77337")
        title.place(x=425, y=10)
        
        title = Label(root, text="You get 30 seconds to answer for every questions:",
                      font=("Impact", 16, "bold"), fg="#d77337")
        title.place(x=380, y=80)

        # Entry Input
        self.answer = Entry(root,  font=(
            "times new Roman", 14), bg="lightgray")
        self.answer.place(x=410, y=520, width=200, height=50)

        result = Button(root, text="Submit", cursor="hand2", command=self.result_function,
                        font=("times new Roman", 14), bg="#d25d17", fg="white")
        result.place(x=660, y=525, width=120)
        
        num = IntVar()
        num = None
        self.score_res = tk.Label(root,font=(
            "times new Roman", 22), textvariable=num)
        self.score_res.place(x=500, y=600)
        self.score_res.config(text=f'Your score is {str(self.score)}')
        self.show_image()
        

    # functionality   
    def show_image(self):
        self.ques, self.soln = Smiley_Game.create_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)
        self.imagelab.config(image=self.image)
        root.after(1000*30, self.show_image)
 
    #b this function is to logout and move to login page
    def logout_function(self):
        time.sleep(0)
        root.destroy()
        call(["python", "login.py"])
        
    @staticmethod
    def create_image():
        api_url = "https://marcconrad.com/uob/smile/api.php"
        response = urlopen(api_url)
        smileJson = json.loads(response.read())
        question = smileJson['question']
        solution = smileJson['solution']
        return question, solution

    # this is result function for user gameplay
    def result_function(self):
        if self.answer.get() == "":
            messagebox.showerror(
                "Error", "Please submit the answer", parent=root)
        elif self.answer.get() != str(self.soln):
            messagebox.showerror(
                "Error", "Try Again!", parent=root)
            self.answer.delete(0, END)
        else:
            messagebox.showinfo(
                "Success", "Correct Answer!", parent=root)
            self.score += 1
            self.answer.delete(0, END) 
            self.score_res.config(text=f'Your score is {str(self.score)}')
            self.show_image()


if __name__ == '__main__':
    ques, soln= Smiley_Game.create_image()
    img = Smiley_Game(ques, soln)
    
    icon_img = PhotoImage(file="Image\icon.png")
    root.iconphoto(False, icon_img)
    root.mainloop()

    
    
