#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import datetime as dt
from Date_compute import MMonthago,YMonthago 
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
def getdata():
    dfgl=pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    dfgl_date=dfgl['date'].str.split('-',5, True)
    dfgl['Y']=dfgl_date[0]
    dfgl['M']=dfgl_date[1]
    dfgl['D']=dfgl_date[2]
    return dfgl
def rowdataclean(dfgl):
    countrymapping=pd.read_excel(r'contry_mapping.xlsx')
    countrymapping=countrymapping.rename(columns={'English_name':'location'})
    dfgl1=pd.merge(dfgl,countrymapping,how='left')
    dfgl1.to_excel(r'myrawdata.xlsx',index=False)
    return dfgl1
def rawdata2month(rawdata,thisyear,thismonth):
    Ylist=YMonthago(thisyear,thismonth,3)
    Mlist=MMonthago(thismonth,3)
    mask1=rawdata['Y']==Ylist[0]
    mask2=rawdata['Y']==Ylist[1]
    mask3=rawdata['M']==Mlist[0]
    mask4=rawdata['M']==Mlist[1]
    rawdata2month=rawdata[(mask1&mask3)|(mask2&mask4)]
    return rawdata2month
def updaterawdatathis2month():
    now=dt.datetime.now()
    today=now.strftime('%Y_%m_%d')
    Y=int(now.strftime('%Y'))
    M=int(now.strftime('%m'))
    rawdata=pd.read_excel(r'myrawdata.xlsx')
    rawdata2monthdf=rawdata2month(rawdata,Y,M)
    rawdata2monthdf.to_excel(r'myrawdata2month.xlsx',index=False)
def fiternewcase(date_chinese_country):
    try:
        x = date_chinese_country.split(",")
        date=x[1]
        chinese_country=x[2]
        myrawdata2month=pd.read_excel(r'myrawdata2month.xlsx')
        #date='2021-08-18'
        #chinese_country='泰國'
        maskdata=myrawdata2month['date']==date
        maskcountry=myrawdata2month['Chinese_name']==chinese_country
        filterdata=myrawdata2month[(maskdata&maskcountry)]
        newcaseary=filterdata['new_cases'].values
        return newcaseary[0]
    except:
        return '錯誤,可能是資料還未更新或格式打錯嘍~!'




