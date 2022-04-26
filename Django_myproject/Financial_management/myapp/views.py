from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from myapp.models import assets,income,bigexpend,expend,endMeets,debt
from myapp.Date_compute import MMonthago,YMonthago
import pandas as pd
import datetime as dt
import os

import django_tables2 as tables
from django_tables2 import RequestConfig

import json

from django.contrib import auth

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())
def index(request):
    return render(request, 'index.html')
def insertAssetsByExcel():
    assetsdf=pd.read_excel(r'myapp\assets_init.xlsx')
    assetsary=assetsdf.values
    assetsaryShape=assetsary.shape
    print(assetsaryShape)
    for i in range(assetsaryShape[0]):
        owner=assetsary[i][0]
        date=assetsary[i][1]
        assets_debt=assetsary[i][2]
        account_type=assetsary[i][3]
        account=assetsary[i][4]
        TWD_exchange=assetsary[i][5]
        assets_QTY=assetsary[i][6]
        unit=assets.objects.create(
                            owner=owner,
                            date=date,
                            assets_debt=assets_debt,
                            account_type=account_type,
                            account=account,
                            TWD_exchange=TWD_exchange,
                            assets_QTY=assets_QTY,)
    unit=unit.save()
def deleteAssets():
    assets.objects.all().delete()
def insertIncomeByExcel():
    incomedf=pd.read_excel(r'myapp\income_init.xlsx')
    incomeary=incomedf.values
    incomearyShape=incomeary.shape
    for i in range(incomearyShape[0]):
        owner=incomeary[i][0]
        date=incomeary[i][1]
        income_type=incomeary[i][2]
        TWD_exchange=incomeary[i][3]
        income_QTY=incomeary[i][4]
        unit=income.objects.create(
                            owner=owner,
                            date=date,
                            income_type=income_type,
                            TWD_exchange=TWD_exchange,
                            income_QTY=income_QTY,)
    unit=unit.save()
def deleteIncome():
    income.objects.all().delete()
def initAssetsByURL(request):#重置資料庫
    deleteAssets()
    insertAssetsByExcel()
    return render(request,"insertAssetsByURL.html",locals())
def initIncomeByURL(request):#重置資料庫
    deleteIncome()
    insertIncomeByExcel()
    return render(request,"insertIncomeByURL.html",locals())
def makeendMeetDf(assets,income,debt):
    assets_date=assets['date'].astype(str).str.split('-',5, True)
    assets['Y']=assets_date[0]
    assets['M']=assets_date[1]
    assets['assets_TWD']=assets['assets_QTY']*assets['TWD_exchange']
    assets.head()
    assetsM=assets.groupby(['Y','M'])['assets_TWD'].sum().to_frame().reset_index()

    debt_date=debt['date'].astype(str).str.split('-',5, True)
    debt['Y']=debt_date[0]
    debt['M']=debt_date[1]
    debt['debt_TWD']=debt['debt_QTY']*debt['TWD_exchange']
    debtM=debt.groupby(['Y','M'])['debt_TWD'].sum().to_frame().reset_index()
    print(debtM)
    income_date=income['date'].astype(str).str.split('-',5, True)
    income['Y']=income_date[0]
    income['M']=income_date[1]
    income['income_TWD']=income['income_QTY']*income['TWD_exchange']
    income.head()
    incomeM=income.groupby(['Y','M'])['income_TWD'].sum().to_frame().reset_index()
    
    endMeets=pd.merge(assetsM,incomeM,how='left')
    endMeets1=pd.merge(endMeets,debtM,how='left')
    endMeets_dropfirstM=endMeets1.drop([0]).reset_index()
    endMeets_dropfirstM['assets_TWD_lastmonth']=endMeets['assets_TWD']
    endMeets_dropfirstM['expend_TWD']=endMeets_dropfirstM['income_TWD']-(endMeets_dropfirstM['assets_TWD']-endMeets_dropfirstM['assets_TWD_lastmonth'])
    endMeets_dropfirstM['end_meets']=endMeets_dropfirstM['income_TWD']-endMeets_dropfirstM['expend_TWD']
    return endMeets_dropfirstM
    
def base(request):
    x=0
    return render(request,"base.html",locals())
def test(request):
    x=0
    return render(request,"test.html",locals())


class assetsTable(tables.Table):
    class Meta:
        model = assets
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
def querytable_assets(request):
    mask1=Q(owner='Leon')
    assets_set=assets.objects.filter(mask1)
    table = assetsTable(assets_set)
    RequestConfig(request).configure(table)
    return render(request,"querytable_assets.html",{'table':table})

class incomeTable(tables.Table):
    class Meta:
        model = income
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
def querytable_income(request):
    mask1=Q(owner='Leon')
    income_set=income.objects.filter(mask1)
    table = incomeTable(income_set)
    RequestConfig(request).configure(table)
    return render(request,"querytable_income.html",{'table':table})

class endMeetsTable(tables.Table):
    class Meta:
        model = endMeets
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
def querytable_endMeets(request):
    mask1=Q(owner='Leon')
    endMeets_set=endMeets.objects.filter(mask1)
    table = endMeetsTable(endMeets_set)
    RequestConfig(request).configure(table)
    return render(request,"querytable_endMeets.html",{'table':table})

def updateEndMeetsByURL(request):
    myIDmask=Q(owner='Leon')
    myassets=assets.objects.filter(myIDmask)
    myassetsdf=pd.DataFrame(list(myassets.values()))

    mydebt=debt.objects.filter(myIDmask)
    mydebtdf=pd.DataFrame(list(mydebt.values()))

    myincome=income.objects.filter(myIDmask)
    myincomedf=pd.DataFrame(list(myincome.values()))

    endMeetDf=makeendMeetDf(myassetsdf,myincomedf,mydebtdf)
    endMeetDf.to_excel(r'endMeet.xlsx')
    print(endMeetDf)

    endMeets.objects.all().delete()
    endMeetAry=endMeetDf.values
    endMeetshape=endMeetAry.shape
    print(endMeetAry)
    for i in range(endMeetshape[0]):
        unit=endMeets.objects.create(
                    owner='Leon',
                    Y=endMeetAry[i][1],
                    M=endMeetAry[i][2],
                    year_month=dt.datetime.strptime('{}-{}-01'.format(endMeetAry[i][1],endMeetAry[i][2]), '%Y-%m-%d'),
                    assets_TWD=endMeetAry[i][3],
                    debt_TWD=endMeetAry[i][5],
                    income_TWD=endMeetAry[i][4],
                    expend_TWD=endMeetAry[i][7],
                    end_meets=endMeetAry[i][8])
        unit=unit.save()
    mask1=Q(owner='Leon')
    endMeets_set=endMeets.objects.filter(mask1)
    table = endMeetsTable(endMeets_set)
    RequestConfig(request).configure(table)
    return render(request,"updateEndMeetsByURL.html",locals())
def lazyupdate_assets(request):
    if request.method=="POST":
        date=request.POST['date']
        assets_debt=request.POST['assets_debt']
        account_type=request.POST['account_type']
        account=request.POST['account']
        TWD_exchange=request.POST['TWD_exchange']
        assets_QTY=request.POST['assets_QTY']
        unit=assets.objects.create(owner="Leon",date=date,assets_debt=assets_debt,account=account,account_type=account_type,TWD_exchange=TWD_exchange,assets_QTY=assets_QTY)
        unit.save()#寫入sqllite
    else:
        message='please key something'
    mask1=Q(owner='Leon')
    assets_set=assets.objects.filter(mask1)
    table = assetsTable(assets_set)
    RequestConfig(request).configure(table)
    return render(request,"lazyupdate_assets.html",locals())

def lazyupdate_income(request):
    if request.method=="POST":
        date=request.POST['date']
        income_type=request.POST['income_type']
        TWD_exchange=request.POST['TWD_exchange']
        income_QTY=request.POST['income_QTY']
        unit=income.objects.create(owner="Leon",date=date,income_type=income_type,TWD_exchange=TWD_exchange,income_QTY=income_QTY)
        unit.save()#寫入sqllite
    else:
        message='please key something'
    
    mask1=Q(owner='Leon')
    income_set=income.objects.filter(mask1)
    table = incomeTable(income_set)
    RequestConfig(request).configure(table)

    return render(request,"lazyupdate_income.html",locals())

def lazydelete_income(request):
    if request.method=="POST":
        id=request.POST['ID']
        unit=income.objects.filter(id=id)
        unit.delete()#刪除
    else:
        message='please key something'
    
    mask1=Q(owner='Leon')
    income_set=income.objects.filter(mask1)
    table = incomeTable(income_set)
    RequestConfig(request).configure(table)
    
    return render(request,"lazydelete_income.html",locals())

def lazydelete_assets(request):
    if request.method=="POST":
        id=request.POST['ID']
        unit=assets.objects.filter(id=id)
        unit.delete()#刪除
    else:
        message='please key something'
    
    mask1=Q(owner='Leon')
    assets_set=assets.objects.filter(mask1)
    table = assetsTable(assets_set)
    RequestConfig(request).configure(table)
    
    return render(request,"lazydelete_assets.html",locals())

def lazy_borad_data(request):
    mask1=Q(owner="Leon")
    income_set=income.objects.values().filter(mask1)
    income_list=list(income_set)
    for i in range(len(income_list)):
        income_list[i]["date"]=dt.datetime.strftime(income_list[i]["date"], "%Y-%m-%d")

    assets_set=assets.objects.values().filter(mask1)
    assets_list=list(assets_set)
    for i in range(len(assets_list)):
        assets_list[i]["date"]=dt.datetime.strftime(assets_list[i]["date"], "%Y-%m-%d")
    
    endMeets_set=endMeets.objects.values().filter(mask1)
    endMeets_list=list(endMeets_set)
    for i in range(len(endMeets_list)):
        endMeets_list[i]["year_month"]=dt.datetime.strftime(endMeets_list[i]["year_month"], "%Y-%m-%d")
    return JsonResponse({'income_data':income_list,'assets_data':assets_list,'endMeets_data':endMeets_list})

def lazy_board(request):
    x=1
    return render(request,"lazy_board.html",locals())

class debtTable(tables.Table):
    class Meta:
        model = debt
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
def lazyupdate_debt(request):
    if request.method=="POST":
        date=request.POST['date']
        assets_debt=request.POST['assets_debt']
        account_type=request.POST['account_type']
        account=request.POST['account']
        TWD_exchange=request.POST['TWD_exchange']
        debt_QTY=request.POST['debt_QTY']
        unit=debt.objects.create(owner="Leon",date=date,assets_debt=assets_debt,account=account,account_type=account_type,TWD_exchange=TWD_exchange,debt_QTY=debt_QTY)
        unit.save()#寫入sqllite
    else:
        message='please key something'
    mask1=Q(owner='Leon')
    debt_set=debt.objects.filter(mask1)
    table = debtTable(debt_set)
    RequestConfig(request).configure(table)
    return render(request,"lazyupdate_debt.html",locals())
def lazydelete_debt(request):
    if request.method=="POST":
        id=request.POST['ID']
        unit=debt.objects.filter(id=id)
        unit.delete()#刪除
    else:
        message='please key something'
    
    mask1=Q(owner='Leon')
    debt_set=debt.objects.filter(mask1)
    table = debtTable(debt_set)
    RequestConfig(request).configure(table)
    
    return render(request,"lazydelete_debt.html",locals())