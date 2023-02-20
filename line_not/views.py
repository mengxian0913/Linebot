
import requests
from bs4 import BeautifulSoup as bs

url = "https://www.iecs.fcu.edu.tw/news/?category=speech"
dash = "\n*********************************"
url_news = "https://www.iecs.fcu.edu.tw/news/"

total = ""


def catch(now): 
    global total

    main = now.find("table")
    text = main.get_text(strip=True)
    # 解析演講資訊
    info = text.split("：")

    date = info[1].split("演講時間")[0]
    time = info[2].split("演講者")[0]
    speaker = info[3].split("服務單位")[0]
    affiliation = info[4].split("演講題目")[0]
    topic = info[5].split("演講地點")[0]
    place = info[6].split("值日生")[0]

    # 格式化輸出
    output = f"Date     : {date}\nTime     : {time}\nSpeaker  : {speaker}\nAffiliation : {affiliation}\nTopic    : {topic}\nPlace    : {place}\n"
    
    total += output + dash + "\n"
    print(total)

#    print(output, dash)


def start_catch():
    posts = []
    title = []

    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    post = soup.find_all(class_="post", limit=10)
        
    global total

    total = ""

    for i in post:
        link = i.select_one(".post-image")
        link = link.select_one("a").get("href")
        title.append(link)
        link = url_news +  link + "/"
        posts.append(link)


    for i in range(0, len(posts)):
        total += "\n" + title[i] + "\n"
        speech = requests.get(posts[i])
        soup2 = bs(speech.text, "html.parser")
        catch(soup2)

    print(total)
    return total

#------------------------------------------------------------------------------------------------------------------------




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

Input = ["act", "活動", "news", "Act"]

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
                text = event.message.text
                
                for i in Input:
                    if text == i:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=start_catch()),
                        )
                        break


        return HttpResponse()
    else:
        return HttpResponseBadRequest()



#------------------------------------------------------------------------------------------------------------------------




