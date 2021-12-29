import  random
from tkinter import *
import string
import pandas as pd

def generate_password():
    password=[]
    for i in range(5):
        alpha=random.choice(string.ascii_letters)
        symbol=random.choice(string.punctuation)
        numbers=random.choice(string.digits)
        password.append(alpha)
        password.append(numbers)
        password.append(symbol)

    y=''.join(str(x) for x in password)
    lbl.config(text=y)
    return y


def copy_password():
    df=pd.DataFrame([generate_password()], columns=['generate_password()_values'])
    df.to_clipboard(index=False,header=False)

#create my window  
window =Tk(className='Reda\'s passowrd generator- v1.0')
#window['bg']='#856ff8'
canv = Canvas(window, width=350, height=80, bg='Green')
canv.grid(row=2, column=3)

#button to copy the generated string 
btn=Button(window, text="Generate & Copy Password", command=copy_password)
btn.grid(row=2,column=3)

#this is the label that needs to be copied after generation
lbl=Label(window,font=("Helvetica",24,"bold"))
lbl.grid(row=3,column=3)

window.mainloop()



