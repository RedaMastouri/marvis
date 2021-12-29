#!/usr/bin/env python
# coding: utf-8

# In[6]:


from csv import *


# In[2]:


fieldnames=["Name","Age","Contact"]


# In[3]:


file=open("my_first_file.csv","w")  ##create a csv file


# In[7]:


Writer=writer(file)


# In[8]:


Writer.writerow(fieldnames)


# In[9]:


file.close()


# In[ ]:




