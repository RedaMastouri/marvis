#!/usr/bin/env python
# coding: utf-8

# In[1]:


from csv import *
from tkinter import *
from tkinter import messagebox


# In[2]:


window=Tk()
window.title("Data entry")
main_lst=[]


# In[3]:


'''[["Sujith",19,37798127398] , ["MASK",25,247097403],["john",27,372893629838]]'''
def Add():
    lst=[name.get(),age.get(),contact.get()]
    main_lst.append(lst)
    messagebox.showinfo("Information","The data has been added succesfully")


# In[4]:


def Save():
    with open("data_entry.csv","w") as file:
        Writer=writer(file)
        Writer.writerow(["Name","Age","Contact"])
        Writer.writerows(main_lst)
        messagebox.showinfo("Information","Saved succesfully")


# In[5]:


def Clear():
    name.delete(0,END)
    age.delete(0,END)
    contact.delete(0,END)


# ## 3 labels, 4 buttons,3 entry fields 

# In[6]:


label1=Label(window,text="Name: ",padx=20,pady=10)
label2=Label(window,text="Age: ",padx=20,pady=10)
label3=Label(window,text="Contact: ",padx=20,pady=10)
name=Entry(window,width=30,borderwidth=5)
age=Entry(window,width=30,borderwidth=5)
contact=Entry(window,width=30,borderwidth=5)
save=Button(window,text="Save",padx=20,pady=10,command=Save)
add=Button(window,text="Add",padx=20,pady=10,command=Add)
clear=Button(window,text="Clear",padx=18,pady=10,command=Clear)
Exit=Button(window,text="Exit",padx=20,pady=10,command=window.quit)


# In[7]:


label1.grid(row=0,column=0)
label2.grid(row=1,column=0)
label3.grid(row=2,column=0)
name.grid(row=0,column=1)
age.grid(row=1,column=1)
contact.grid(row=2,column=1)
save.grid(row=4,column=0,columnspan=2)
add.grid(row=3,column=0,columnspan=2)
clear.grid(row=5,column=0,columnspan=2)
Exit.grid(row=6,column=0,columnspan=2)


# In[8]:


window.mainloop()


# In[9]:


print(lst)


# In[ ]:


print(main_lst)


# In[11]:


##messagebox.showerror("Oops!","An error has occured")


# In[ ]:




