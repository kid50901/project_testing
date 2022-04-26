from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from covid19BotApp.models import covid7dayInfo 


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import pandas as pd
import datetime as dt
import os

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

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

########excel餵資料待刪
def rowdataclean(dfgl):
    countrymapping=pd.read_excel(r'contry_mapping.xlsx')
    countrymapping=countrymapping.rename(columns={'English_name':'location'})
    dfgl1=pd.merge(dfgl,countrymapping,how='left')
    dfgl1.to_excel('.\myrawdata.xlsx',index=False)
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
        path=os.getcwd()
        x = date_chinese_country.split(",")
        date=x[1]
        chinese_country=x[2]
        print(chinese_country)
        myrawdata2month=pd.read_excel(r'myrawdata2month.xlsx')
        #date='2021-08-18'
        #chinese_country='泰國'
        maskdata=myrawdata2month['date']==date
        maskcountry=myrawdata2month['Chinese_name']==chinese_country
        filterdata=myrawdata2month[(maskdata&maskcountry)]
        newcaseary=filterdata['new_cases'].values
        return (chinese_country+date + ' : '+str(newcaseary[0])+'人確診')
    except :
        return '找不到確診數,可能是資料還未更新或格式打錯嘍~!查詢確診數的輸入範例:新增確診,2021-08-18,泰國'
def fiternewcaseEN(date_country):
    try:
        path=os.getcwd()
        x = date_country.split(",")
        date=x[1]
        country=x[2]
        print(country)
        myrawdata2month=pd.read_excel(r'myrawdata2month.xlsx')
        #date='2021-08-18'
        #chinese_country='泰國'
        maskdata=myrawdata2month['date']==date
        maskcountry=myrawdata2month['location']==country
        filterdata=myrawdata2month[(maskdata&maskcountry)]
        newcaseary=filterdata['new_cases'].values
        return (country+' '+date + ' : '+str(newcaseary[0])+' confirmed case')
    except :
        return 'I can not find confirmed case,maybe key wrong~!search newcases input example:newcases,2021-08-18,Thailand'
########excel餵資料待刪



def clean7dayData():
    dfgl=getdata()
    countrymapping=pd.read_excel(r'contry_mapping.xlsx')
    countrymapping=countrymapping.rename(columns={'English_name':'location'})
    dfgl=pd.merge(dfgl,countrymapping,how='left')
    covidInfoDf=pd.DataFrame(columns=['location','date'])
    covidInfoDf['location']=dfgl['location']
    covidInfoDf['date']=dfgl['date']
    covidInfoDf['total_cases']=dfgl['total_cases']
    covidInfoDf['new_cases']=dfgl['new_cases']
    covidInfoDf['total_deaths']=dfgl['total_deaths']
    covidInfoDf['new_deaths']=dfgl['new_deaths']
    covidInfoDf['total_vaccinations']=dfgl['total_vaccinations']
    covidInfoDf['people_vaccinated']=dfgl['people_vaccinated']
    covidInfoDf['people_fully_vaccinated']=dfgl['people_fully_vaccinated']
    covidInfoDf['new_vaccinations']=dfgl['new_vaccinations']
    covidInfoDf['total_vaccinations_per_hundred']=dfgl['total_vaccinations_per_hundred']
    covidInfoDf['people_vaccinated_per_hundred']=dfgl['people_vaccinated_per_hundred']
    covidInfoDf['Chinese_name']=dfgl['Chinese_name']
    covidInfoDf['date_str']=dfgl['date']
    today=dt.date.today()
    oneday = dt.timedelta(days=1)
    wantday=today-oneday
    wantdaylist=[]
    masklist=[]
    for i in range(7):
        today=dt.date.today()
        deltaday = dt.timedelta(days=i)
        wantday=today-deltaday
        wantdaylist.append(wantday.strftime("%Y-%m-%d"))
        masklist.append(covidInfoDf['date']==wantday.strftime("%Y-%m-%d"))#篩選條件
    covidInfo7dayDf=covidInfoDf[(masklist[0]|masklist[1]|masklist[2]|masklist[3]|masklist[4]|masklist[5]|masklist[6])]
    #covidInfo7dayDf['date']=pd.to_datetime(covidInfo7dayDf['date'],format="%Y-%m-%d")
    covidInfo7dayDf1=covidInfo7dayDf.fillna(0)
    return covidInfo7dayDf1
def insertCovid7dayInfo():
    covidInfo7dayDf=clean7dayData()
    covidInfo7dayary=covidInfo7dayDf.values
    covidInfo7dayshape=covidInfo7dayary.shape
    for i in range(covidInfo7dayshape[0]):
        location=covidInfo7dayary[i][0]
        date=dt.datetime.strptime(covidInfo7dayary[i][1], '%Y-%m-%d')
        #datetime.datetime.strptime(covidInfo7dayary[i][1], '%Y-%m-%d')
        total_cases=covidInfo7dayary[i][2]
        new_cases=covidInfo7dayary[i][3]
        total_deaths=covidInfo7dayary[i][4]
        new_deaths=covidInfo7dayary[i][5]
        total_vaccinations=covidInfo7dayary[i][6]
        people_vaccinated=covidInfo7dayary[i][7]
        people_fully_vaccinated=covidInfo7dayary[i][8]
        new_vaccinations=covidInfo7dayary[i][9]
        total_vaccinations_per_hundred=covidInfo7dayary[i][10]
        people_vaccinated_per_hundred=covidInfo7dayary[i][11]
        Chinese_name=covidInfo7dayary[i][12]
        date_str=covidInfo7dayary[i][13]
        unit=covid7dayInfo.objects.create(
                            location=location,
                            date=date,
                            total_cases=total_cases,
                            new_cases=new_cases,
                            total_deaths=total_deaths,
                            new_deaths=new_deaths,
                            total_vaccinations=total_vaccinations,
                            people_vaccinated=people_vaccinated,
                            people_fully_vaccinated=people_fully_vaccinated,
                            new_vaccinations=new_vaccinations,
                            total_vaccinations_per_hundred=total_vaccinations_per_hundred,
                            people_vaccinated_per_hundred=people_vaccinated_per_hundred,
                            Chinese_name=Chinese_name,
                            date_str=date_str)
        unit=unit.save()
def deleteCovid7dayInfo():
    covid7dayInfo.objects.all().delete()
def filterDateCNcontry(date_CNcountry):
    x = date_CNcountry.split(",")
    date=x[1]
    chinese_country=x[2]
    print(chinese_country)
    #date='2021-08-18'
    #chinese_country='泰國'
    maskdata=Q(date_str=date)
    maskcountry=Q(Chinese_name= chinese_country)
    filterDateCNcontry_table=covid7dayInfo.objects.filter(maskdata&maskcountry)
    for i in filterDateCNcontry_table:
        mydate_str=i.date_str
        myChinese_name=i.Chinese_name
        mynew_cases=i.new_cases
        mytotal_cases=i.total_cases
        mynew_deaths=i.new_deaths
        mytotal_deaths=i.total_deaths
        mytotal_vaccinations=i.total_vaccinations
        mypeople_vaccinated=i.people_vaccinated
        mypeople_fully_vaccinated=i.people_fully_vaccinated
        mynew_vaccinations=i.new_vaccinations
        mypeople_vaccinated_per_hundred=i.people_vaccinated_per_hundred
    return (mydate_str,myChinese_name,mynew_cases,
                                    mytotal_cases,
                                    mynew_deaths,
                                    mytotal_deaths,
                                    mytotal_vaccinations,
                                    mypeople_vaccinated,
                                    mypeople_fully_vaccinated,
                                    mynew_vaccinations,
                                    mypeople_vaccinated_per_hundred)
def filterDateENcontry(date_ENcountry):
    x = date_ENcountry.split(",")
    date=x[1]
    english_country=x[2]
    print(english_country)
    #date='2021-08-18'
    #chinese_country='泰國'
    maskdata=Q(date_str=date)
    maskcountry=Q(location = english_country)
    filterDateENcontry_table=covid7dayInfo.objects.filter(maskdata&maskcountry)
    for i in filterDateENcontry_table:
        mydate_str=i.date_str
        myEnglish_name=i.location
        mynew_cases=i.new_cases
        mytotal_cases=i.total_cases
        mynew_deaths=i.new_deaths
        mytotal_deaths=i.total_deaths
        mytotal_vaccinations=i.total_vaccinations
        mypeople_vaccinated=i.people_vaccinated
        mypeople_fully_vaccinated=i.people_fully_vaccinated
        mynew_vaccinations=i.new_vaccinations
        mypeople_vaccinated_per_hundred=i.people_vaccinated_per_hundred
    return (mydate_str,myEnglish_name,mynew_cases,
                                    mytotal_cases,
                                    mynew_deaths,
                                    mytotal_deaths,
                                    mytotal_vaccinations,
                                    mypeople_vaccinated,
                                    mypeople_fully_vaccinated,
                                    mynew_vaccinations,
                                    mypeople_vaccinated_per_hundred)


def insertCovid7dayInfoByURL(request):
    insertCovid7dayInfo()
    return render(request,"insertCovid7dayInfoByURL.html",locals())
def deleteCovid7dayInfoByURL(request):
    deleteCovid7dayInfo()
    return render(request,"deleteCovid7dayInfoByURL.html",locals())
def updateCovid7dayInfoByURL(request):
    deleteCovid7dayInfo()
    print('delete')
    insertCovid7dayInfo()
    return render(request,"updateCovid7dayInfoByURL.html",locals())
def filterDateCNcontryByHTML(request):
    if request.method=="POST":
        date_CNcountry=request.POST['date_CNcountry_template']
        filterDateCNcontryResult=filterDateCNcontry(date_CNcountry)
        date_Templates=filterDateCNcontryResult[0]
        chineseCN__Templates=filterDateCNcontryResult[1]
        newcases_Templates=filterDateCNcontryResult[2]
        responseCaseToTemplates=chineseCN__Templates+date_Templates + ' : '+str(newcases_Templates)+'人確診'
    else:
        message='請輸入資料'
    return render(request,"filterDateCNcontryByHTML.html",locals())
def LineBotrelyDateCNcontryNewcases(date_CNcountry):
    try:
        filterDateCNcontryResult=filterDateCNcontry(date_CNcountry)
        date_Templates=filterDateCNcontryResult[0]
        chineseCN_Templates=filterDateCNcontryResult[1]
        newcases_Templates=filterDateCNcontryResult[2]
        responseCaseToTemplates=chineseCN_Templates+date_Templates + ' : '+str(newcases_Templates)+'人確診'
    except:
        responseCaseToTemplates = '找不到確診數,可能是資料還未更新或格式打錯嘍~!查詢確診數的輸入範例:新增確診,2021-08-18,泰國'
    return responseCaseToTemplates
def LineBotrelyDateENcontryNewcases(date_ENcountry):
    try:
        filterDateENcontryResult=filterDateENcontry(date_ENcountry)
        date_Templates=filterDateENcontryResult[0]
        englishEN_Templates=filterDateENcontryResult[1]
        newcases_Templates=filterDateENcontryResult[2]
        responseCaseToTemplates=englishEN_Templates+date_Templates + ' : '+str(newcases_Templates)+' confirmed case'
    except:
        responseCaseToTemplates = 'I can not find confirmed case,maybe key wrong~!search newcases input example:newcases,2021-08-18,Thailand'
    return responseCaseToTemplates
def LineBotrelyDateCNcontryInfo(date_CNcountry):
    try:
        filterDateCNcontryResult=filterDateCNcontry(date_CNcountry)
        date_Templates=filterDateCNcontryResult[0]
        chineseCN_Templates=filterDateCNcontryResult[1]
        newcases_Templates=filterDateCNcontryResult[2]
        total_cases_templates=filterDateCNcontryResult[3]
        new_deaths_templates=filterDateCNcontryResult[4]
        total_deaths_templates=filterDateCNcontryResult[5]
        total_vaccinations_templates=filterDateCNcontryResult[6]
        people_vaccinated_templates=filterDateCNcontryResult[7]
        people_fully_vaccinated_templates=filterDateCNcontryResult[8]
        new_vaccinations_templates=filterDateCNcontryResult[9]
        people_vaccinated_per_hundred_templates=filterDateCNcontryResult[10]
        responseCaseToTemplates=chineseCN_Templates+'  '+date_Templates + ' : \n'+'新增 '+str(newcases_Templates)+' 人確診\n'+'累計 '+str(total_cases_templates)+' 人確診\n'+'新增 '+str(new_deaths_templates)+' 人確診後死亡\n'+'累計 '+str(total_deaths_templates)+' 人確診後死亡\n'+'累計疫苗施打 '+str(total_vaccinations_templates)+' 劑\n'+'累計疫苗施打 '+str(people_vaccinated_templates)+' 人\n'+'累計疫苗施打(2劑) '+str(people_fully_vaccinated_templates)+' 人\n'+'新增疫苗施打 '+str(new_vaccinations_templates)+' 劑\n'+'已施打疫苗人口涵蓋率 '+str(people_vaccinated_per_hundred_templates)+' %\n\n數據為0可能是資料還未更新，請改為查詢早幾天的資料~!'
    except:
        responseCaseToTemplates = '找不到資訊,可能是資料還未更新或格式打錯嘍~!查詢確診數的輸入範例:新增確診,2021-08-18,泰國'
    return responseCaseToTemplates
def LineBotrelyDateENcontryInfo(date_ENcountry):
    try:
        filterDateENcontryResult=filterDateENcontry(date_ENcountry)
        date_Templates=filterDateENcontryResult[0]
        englishCN_Templates=filterDateENcontryResult[1]
        newcases_Templates=filterDateENcontryResult[2]
        total_cases_templates=filterDateENcontryResult[3]
        new_deaths_templates=filterDateENcontryResult[4]
        total_deaths_templates=filterDateENcontryResult[5]
        total_vaccinations_templates=filterDateENcontryResult[6]
        people_vaccinated_templates=filterDateENcontryResult[7]
        people_fully_vaccinated_templates=filterDateENcontryResult[8]
        new_vaccinations_templates=filterDateENcontryResult[9]
        people_vaccinated_per_hundred_templates=filterDateENcontryResult[10]
        responseCaseToTemplates=englishCN_Templates+'  '+date_Templates + ' : \n'+'increase '+str(newcases_Templates)+' cases,\n'+'Cumulative '+str(total_cases_templates)+' cases,\n'+'increase '+str(new_deaths_templates)+' death,\n'+'Cumulative '+str(total_deaths_templates)+' death,\n'+'vaccinated '+str(total_vaccinations_templates)+' vaccines,\n'+'vaccinated '+str(people_vaccinated_templates)+' people,\n'+'vaccinated(2 vaccine) '+str(people_fully_vaccinated_templates)+' people,\n'+'new vaccinated '+str(new_vaccinations_templates)+' vaccines,\n'+'vaccinated per hundred '+str(people_vaccinated_per_hundred_templates)+' %\n\nIf data is 0,please research early time~!'
    except:
        responseCaseToTemplates = '找不到資訊,可能是資料還未更新或格式打錯嘍~!查詢確診數的輸入範例:新增確診,2021-08-18,泰國'
    return responseCaseToTemplates
@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                messageText=event.message.text
                print(messageText)
                
                if messageText.find('新增確診')!=-1:
                    sendtext=LineBotrelyDateCNcontryNewcases(messageText)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,                        
                        TextSendMessage(text=sendtext)
                    )
                elif messageText.find('newcases')!=-1:
                     sendtext=LineBotrelyDateENcontryNewcases(messageText)
                     line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,                        
                        TextSendMessage(text=sendtext)
                    )
                elif messageText.find('新冠肺炎資訊')!=-1:
                     sendtext=LineBotrelyDateCNcontryInfo(messageText)
                     line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,                        
                        TextSendMessage(text=sendtext)
                    )
                elif messageText.find('Covid-19 information')!=-1:
                     sendtext=LineBotrelyDateENcontryInfo(messageText)
                     line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,                        
                        TextSendMessage(text=sendtext)
                    )
                elif messageText=='ADMIN_updateCovid7dayInfo':
                    print('重置資料...')
                    deleteCovid7dayInfo()
                    print('重置資料成功')
                    print('插入資料...')
                    insertCovid7dayInfo()
                    print('插入資料成功')
                
                elif (messageText.find('covid')!=-1)|(messageText.find('Covid')!=-1)|(messageText.find('新冠')!=-1)|(messageText.find('肺炎')!=-1):
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='嗨~!我可以告訴你一些 covid-19 的訊息喔🧐🧐🧐')
                    )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()