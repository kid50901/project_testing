#!/usr/bin/env python
# coding: utf-8

# In[1]:


import change_assets 
import ends_meet_month
import datetime as dt
import os
def want_todoF():
    want_todo=input('key about what do you want to do?(A.update_assests, B.delete_assest, C.update ends_meet)')
    return want_todo
def update():
    thislvPATH=os.getcwd()
    lastlvPATH=os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    asserts_excelpath  = r'{}\data\assets.xlsx'.format(lastlvPATH)
    want_asserts_excelpath  = r'{}\input\assets_input.xlsx'.format(lastlvPATH)
    datahistory  = r'{}\data\history'.format(lastlvPATH)
    todo=want_todoF()
    if  todo == 'A':
        print('please go to append assets EXCEL,just write the data you want to append({}\input\assets_input.xlsx)'.format(lastlvPATH))
        step=input(' update assets EXCEL finish?(Y/back)')
        if step == 'Y' :
            change_assets.append_byexcel(asserts_excelpath,want_asserts_excelpath,datahistory)
            update()
        else :
            update()
    elif todo == 'B' :
        step=input('Do or back?(Do/back)')
        if step == 'Do':
            Ystr=input('Year you want to delete:')
            Mstr=input('Month you want to delete:')
            Y=int(Ystr)
            M=int(Mstr)
            change_assets.delete_bymonth(Y,M,asserts_excelpath,datahistory)
            update()
        else :
            update()
    elif todo == 'C' :
        print('please go to update income EXCEL({}\input\income_input.xlsx)'.format(lastlvPATH))
        step=input(' update income EXCEL finish?(Y/back)')
        if step == 'Y' :
            ends_meet_month.update_ends_meet()
            update()
        else :
            update() 
    else :
        update()  




