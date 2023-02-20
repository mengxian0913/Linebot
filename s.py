import requests
from bs4 import BeautifulSoup as bs

url = "https://www.iecs.fcu.edu.tw/news/?category=speech"
dash = "------------------------------------------------"

response = requests.get(url)

soup = bs(response.text, "html.parser")


post = soup.find_all(class_="post", limit=10)

url_news = "https://www.iecs.fcu.edu.tw/news/"

posts = []
title = []

for i in post:
    link = i.select_one(".post-image")
    link = link.select_one("a").get("href")
    title.append(link)
    link = url_news +  link + "/"
    posts.append(link)



def catch(now):
    main = now.find("table")
    text = main.get_text(strip=True)
#print(text)

    # 解析演講資訊
    info = text.split("：")

#print(info)

    date = info[1].split("演講時間")[0]
    time = info[2].split("演講者")[0]
    speaker = info[3].split("服務單位")[0]
    affiliation = info[4].split("演講題目")[0]
    topic = info[5].split("演講地點")[0]
    place = info[6].split("值日生")[0]

    # 格式化輸出
    output = f"Date     : {date}\nTime     : {time}\nSpeaker  : {speaker}\nAffiliation : {affiliation}\nTopic    : {topic}\nPlace    : {place}\n"

    print(output, dash)

    
for i in range(0, len(posts)):
    print(title[i], "\nLink     :", posts[i])
    speech = requests.get(posts[i])
    soup2 = bs(speech.text, "html.parser")
    catch(soup2)
