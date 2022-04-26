

import pandas as pd
import datetime as dt
import configparser
import logging
import os
def update_ends_meet():
    thislvPATH=os.getcwd()
    lastlvPATH=os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    conf = configparser.ConfigParser()
    conf.read(r'{}\config.ini'.format(thislvPATH))
    now=dt.datetime.now()
    formatted_now=now.strftime("%Y_%m_%d_%H%M%S")
    asserts_excelpath  = r'{}\data\assets.xlsx'.format(lastlvPATH)
    ends_meet_excelpath  = r'{}\data\ends_meet.xlsx'.format(lastlvPATH)
    datahistory  = r'{}\data\history'.format(lastlvPATH)
    asserts=pd.read_excel(r'{}'.format(asserts_excelpath))
    asserts_month_TWD=asserts.groupby(['time'])['TWD'].sum().to_frame().reset_index()
    asserts_month_TWD=asserts_month_TWD.rename(columns={'TWD':'asserts_NT'})

    income_input=pd.read_excel(r'{}\input\income_input.xlsx'.format(lastlvPATH))
    income_input['TWD']=income_input['QTY']*income_input['TWD_exchange']
    income_month_TWD=income_input.groupby(['time'])['TWD'].sum().to_frame().reset_index()
    income_month_TWD=income_month_TWD.rename(columns={'TWD':'income_month_NT'})
    balancedf=pd.merge(asserts_month_TWD,income_month_TWD,how='left')

    ##的到上個月值欄位
    balancedf2=balancedf[balancedf['time']!=dt.datetime(2018, 10, 1)]#拿掉第一個月
    balancedf2=balancedf2.reset_index()
    balancedf2['asserts_NT_lastmonth']=balancedf['asserts_NT']
    balancedf2['expend_month_NT']=balancedf2['income_month_NT']-(balancedf2['asserts_NT']-balancedf2['asserts_NT_lastmonth'])
    balancedf2['ends_meet']=balancedf2['income_month_NT']-balancedf2['expend_month_NT']
    balancedf2.to_excel(r'{}'.format(ends_meet_excelpath),index=False)
    balancedf2.to_excel(r'{}\ends_meet_{}.xlsx'.format(datahistory,formatted_now),index=False)
    return balancedf2


