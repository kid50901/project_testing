from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
            print("check,",event)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
def pushbyurl(request):
    yourID = 'U7faec16e7a5a6eaa992737c557655363'
    # 主動推播訊息
    line_bot_api.push_message(yourID, TextSendMessage(text='安安您好！早餐吃了嗎？'))
    return HttpResponse()
def postfromhtml(request):
    if 'user_name' in request.GET:
        return HttpResponse('Welcome!~'+request.GET['user_name'])
    else:
        return render(request,'welcome.html',locals())

def postfromhtmltoline(request):
    if 'user_name' in request.GET:
        yourID = 'U7faec16e7a5a6eaa992737c557655363'
        # 主動推播訊息
        line_bot_api.push_message(yourID, TextSendMessage(text=request.GET['user_name']))
        return HttpResponse('傳送成功!~'+request.GET['user_name'])
    else:
        return render(request,'welcome.html',locals())


def receivingMessage(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return events
    else:
        return HttpResponseBadRequest()
def replyMessage(events):
    for event in events:
        if isinstance(event, MessageEvent):  # 如果有訊息事件
            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
    return HttpResponse()
def callback2(request):
    events=receivingMessage(request)
    replyMessage(events)
