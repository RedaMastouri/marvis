#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import * 
window=Tk() 
##window.geometry("1280*720")


# In[2]:


def sum():
    a=int(entry1.get())
    b=int(entry2.get())
    c=a+b
    entry3.insert(0,c) ##insert(index,value)

def clearing():
    entry1.delete(0,END)##delete(0,END)
    entry2.delete(0,END)
    entry3.delete(0,END)


# In[3]:


label1=Label(window,text="Enter number 1: ",padx=20,pady=10)
label2=Label(window,text="Enter number 2: ",padx=20,pady=10)
entry1=Entry(window,width=30,borderwidth=5)
entry2=Entry(window,width=30,borderwidth=5)
entry3=Entry(window,width=30,borderwidth=5)
add=Button(window,text="Add",padx=20,pady=10,command=sum)
clear=Button(window,text="Clear",padx=20,pady=10,command=clearing)


# In[4]:


label1.grid(row=0,column=0)
label2.grid(row=1,column=0)
entry1.grid(row=0,column=1)
entry2.grid(row=1,column=1)
add.grid(row=2,column=0)
entry3.grid(row=3,column=0)
clear.grid(row=2,column=1)


# In[5]:


window.mainloop()

