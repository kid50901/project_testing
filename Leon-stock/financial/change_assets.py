
import pandas as pd
import datetime as dt
import configparser
import logging
import os
def append_byexcel(asserts_excelpath,want_asserts_excelpath,datahistory):
    now=dt.datetime.now()
    formatted_now=now.strftime("%Y_%m_%d_%H%M%S")
    init_asserts=pd.read_excel(r'{}'.format(asserts_excelpath))
    want_asserts=pd.read_excel(r'{}'.format(want_asserts_excelpath))
    append_asserts=pd.concat([init_asserts,want_asserts]).reset_index(drop=True)
    append_asserts.to_excel(r'{}'.format(asserts_excelpath),index=False)
    append_asserts.to_excel(r'{}\asserts_{}.xlsx'.format(datahistory,formatted_now),index=False)
    return append_asserts
def delete_bymonth(Y,M,asserts_excelpath,datahistory):
    now=dt.datetime.now()
    formatted_now=now.strftime("%Y_%m_%d_%H%M%S")
    init_asserts=pd.read_excel(r'{}'.format(asserts_excelpath))
    mask=init_asserts['time']!=dt.datetime(Y, M, 1)
    keep_asserts=init_asserts[mask]
    keep_asserts['TWD']=keep_asserts['TWD_exchange']*keep_asserts['QTY']
    keep_asserts['THB']=keep_asserts['THB_exchange']*keep_asserts['QTY']
    keep_asserts.to_excel(r'{}'.format(asserts_excelpath),index=False)
    keep_asserts.to_excel(r'{}\asserts_{}.xlsx'.format(datahistory,formatted_now),index=False)
    return keep_asserts
