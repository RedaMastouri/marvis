#!/usr/bin/env python
# coding: utf-8

# In[25]:


from tkinter import *
import csv
i=0
file=open("ssk.csv","w")


# In[14]:


root=Tk()
large_font=("Arial","13")


# In[15]:


label=Label(root,text="Calculator!")
text=Entry(root,width=30,borderwidth=5,font=large_font)


# In[16]:


label.grid(row=0,columnspan=4)
text.grid(row=1,columnspan=4,ipadx=15,ipady=15)


# In[17]:


def number(x):
    global i
    text.insert(i,x)
    i+=1
def answer():
    z=text.get()
    y=eval(z)
    text.delete(0,END)
    text.insert(0,y)
def Clear():
    text.delete(0,END)


# In[18]:


button1=Button(root,text="1",command=lambda: number("1"),padx=40,pady=20)
button2=Button(root,text="2",command=lambda: number("2"),padx=40,pady=20)
button3=Button(root,text="3",command=lambda: number("3"),padx=40,pady=20)
button4=Button(root,text="4",command=lambda: number("4"),padx=40,pady=20)
button5=Button(root,text="5",command=lambda: number("5"),padx=40,pady=20)
button6=Button(root,text="6",command=lambda: number("6"),padx=40,pady=20)
button7=Button(root,text="7",command=lambda: number("7"),padx=40,pady=20)
button8=Button(root,text="8",command=lambda: number("8"),padx=40,pady=20)
button9=Button(root,text="9",command=lambda: number("9"),padx=40,pady=20)
button0=Button(root,text="0",command=lambda: number("0"),padx=40,pady=20)
add=Button(root,text="+",command=lambda: number("+"),padx=40,pady=20)
sub=Button(root,text="-",command=lambda: number("-"),padx=40,pady=20)
mult=Button(root,text="x",command=lambda: number("*"),padx=40,pady=20)
div=Button(root,text="/",command=lambda: number("/"),padx=40,pady=20)
value=Button(root,text="=",command=answer,padx=40,pady=20)
clear=Button(root,text="Clear",command=Clear,padx=30,pady=20)


# In[19]:



button7.grid(row=2,column=0)
button8.grid(row=2,column=1)
button9.grid(row=2,column=2)
add.grid(row=2,column=3)


# In[20]:


button4.grid(row=3,column=0)
button5.grid(row=3,column=1)
button6.grid(row=3,column=2)
sub.grid(row=3,column=3)


# In[21]:


button1.grid(row=4,column=0)
button2.grid(row=4,column=1)
button3.grid(row=4,column=2)
mult.grid(row=4,column=3)


# In[22]:


div.grid(row=5,column=0)
button0.grid(row=5,column=1)
value.grid(row=5,column=2)


# In[23]:


clear.grid(row=5,column=3)


# In[24]:


root.mainloop()

