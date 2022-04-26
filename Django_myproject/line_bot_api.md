# LINE message API
## Introduce
建立一個 line bot 帳號，利用 HTTPS 與 Message API 建立你的系統與 Line bot 間的通訊。你可以 request  LINE Platform 獲取 line bot 的聊天室訊息。也可以 response LINE Platform 請 line bot 推送訊息。
![1](https://github.com/kid50901/Django_myproject/blob/main/img/MessageAPI.PNG)
## Prepare
* Line Developer Providers : line bot 的提供者
* Line Developer Channels : line bot 帳號
* Web server : 負責與 Message API 溝通的 server。
## Outline
1. 申請 Line Developer,建立 Line Channel

2. 架設一個 Web server

3. 發佈 Web server 於公開的 https url

4. Web server 與 Message API 連線設定
## Demo-reply_message
* 申請 Line Developer,建立 Line Channel，在 Line Developer 找到 Channel secret、Channel access token
* 建立 Django 專案。 
* 在 Django 專案下的 view.py 設定Channel secret、Channel access token 撰寫回應訊息的邏輯函式。
```python
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

#LINE_CHANNEL_ACCESS_TOKEN、LINE_CHANNEL_SECRET設定
line_bot_api = LineBotApi('your LINE_CHANNEL_ACCESS_TOKEN')
parser = WebhookParser('your LINE_CHANNEL_SECRET')
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #接收訊息
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)              
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        #回復訊息
        for event in events:
            if isinstance(event, MessageEvent):#觸發事件  
                line_bot_api.reply_message(  #回復訊息
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
            print("check,",event)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
```
* 在 Django 專案下 url.py 設定回應訊息函式 url
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/'), #回應訊息函式 url
]
```
* 啟動 web server，需有公開的 https url。
* 到 Line Developer 把 callback url 填入 webhook url

![2](https://github.com/kid50901/Django_myproject/blob/main/img/webhook_URL.PNG)
* 掃 QR code 加入好友即可對話

![3](https://github.com/kid50901/Django_myproject/blob/main/img/reply_message_single.PNG)
* 建立群組加入 line bot 好友也可對話

![4](https://github.com/kid50901/Django_myproject/blob/main/img/reply_message_group.PNG)
## Demo-push_message(by html)
* 在 Django 專案下 mkdir template,裡面新增 html 並撰寫輸入介面
```html
<html>
    <head>
        <title> Welcome </title>
    </head>
    <body>
        <form action="/welcome/" method="get">
            <label for="user_name">您的名字</label>
            <input id="user_name" type="text" name="user_name">
            <input type="submit" value="傳送到line">
        </form>
    </body>
</html>
```
* 在 Django 專案下 view.py 新增主動發送訊息的函式
```python
def postfromhtmltoline(request):
    if 'user_name' in request.GET:
        yourID = 'U7faec16e7a5a6eaa992737c557655363'#欲推送的id(可以是個人也可以是群組)
        htmlinput=request.GET['user_name']#取得前端 html 的 input 內容
        # 主動推播訊息
        line_bot_api.push_message(yourID, TextSendMessage(text=))#傳送前端 html 的 input 內容到line chat
        return HttpResponse('傳送成功!~'+request.GET['user_name'])
    else:
        return render(request,'welcome.html',locals())
```
* 在 Django 專案下 url.py 設定主動發送訊息函式 url
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', views.callback), #回應訊息函式 url
    path('welcome/', views.postfromhtmltoline),#主動發送訊息函式 url
]
```
* 開啟網頁輸入訊息,此訊息可發送在 line chat room。
![5](https://github.com/kid50901/Django_myproject/blob/main/img/line_api_pushmessage.gif)
## Fee
* Message API 並不是完全免費，reply_message 完全免費，push_message 有條件收費

![6](https://github.com/kid50901/Django_myproject/blob/main/img/lineAPIfee1.PNG)

![7](https://github.com/kid50901/Django_myproject/blob/main/img/lineAPIfee2.PNG)



