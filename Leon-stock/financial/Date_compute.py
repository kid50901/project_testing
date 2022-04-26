#!/usr/bin/env python
# coding: utf-8

# In[3]:


def MMonthago(M,D):
    Mlist=list(range(D))
    Mlist[0]=M
    for i in range(D-1):
        if M==1:
            M=12
            Mlist[i+1]=M
        else:
            M=M-1
            Mlist[i+1]=M
    return Mlist
def YMonthago(Y,M,D):
    Ylist=list(range(D))
    Mlist=list(range(D))
    Mlist[0]=M
    Ylist[0]=Y
    for i in range(D-1):
        if M==1:
            M=12
            Y=Y-1
            Mlist[i+1]=M
            Ylist[i+1]=Y
        else:
            M=M-1
            Y=Y
            Ylist[i+1]=Y
            Mlist[i+1]=M
    return Ylist


# In[ ]:




