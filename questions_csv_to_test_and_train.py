#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
data=pd.read_csv('F:\ChatBot\stack_overflow Data\Questions.csv',encoding="ISO-8859-1")


# In[2]:


import pandas as pd
answer=pd.read_csv('F:\ChatBot\stack_overflow Data\Answers.csv',encoding="ISO-8859-1")


# In[3]:


answer.shape


# In[4]:


data.shape


# In[5]:


data.head(5)


# In[6]:


raw_data= data[data['Id'].isin(answer['ParentId'])]


# In[7]:


raw_data.shape


# In[8]:


data.iloc[:,4].values


# In[9]:


data['Id'].values


# In[12]:


test_done = False
if not test_done:
    with open('train.from','a', encoding='utf8') as f:
        for content in raw_data.iloc[100000:]['Title'].values:
            f.write(content+'\n')
test_done = True


# In[10]:


test_done = False
if not test_done:
    with open('test.from','a', encoding='utf8') as f:
        for content in raw_data.iloc[:100000]['Title'].values:
            f.write(content+'\n')
test_done = True

