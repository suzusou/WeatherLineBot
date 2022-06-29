#-*- coding: utf-8 -*-

# jsonのインポート
import json

# linebotのインポート
from linebot import LineBotApi
from linebot.models import TextSendMessage

# スクレイピング関係のインポート
import requests
from bs4 import BeautifulSoup
# 自分の地域のURLをurlに貼る
url = "https://tenki.jp/forecast/〇/〇/〇/〇/3hours.html"
r = requests.get(url)

bsobject = BeautifulSoup(r.content,"html.parser")
# classの名前forecast-point-3hの情報をとってくる
town_3h = bsobject.find(class_="forecast-point-3h")

# classの名前hourの情報をとってくる
hour = town_3h.find(class_="hour")
# 属性spanの情報を全部取ってくる
h_span = hour.find_all("span")
# とってきた情報を配列に入れる
h = [int(h_span[x].string) for x in range(len(h_span))]

temp = town_3h.find(class_="temperature")
t_span = temp.find_all("span")
t = [float(t_span[x].string) for x in range(len(t_span))]

rainy_p = town_3h.find(class_="prob-precip")
p_span = rainy_p.find_all("span")
p = [p_span[x].string for x in range(len(p_span))]

rainy_a = town_3h.find(class_="precipitation")
a_span = rainy_a.find_all("span")
a = [a_span[x].string for x in range(len(a_span))]


file=open('info.json','r')
info=json.load(file)
CHANNEL_ACCESS_TOKEN=info['CHANNEL_ACCESS_TOKEN']
line_bot_api=LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    USER_ID=info['USER_ID']
    messages=TextSendMessage(text="〇\n"
                                 +str(h[1])+"時："+str(t[1])+"℃ "+str(p[1])+"％ "+str(a[1])+"(mm/h)\n"
                                 +str(h[3])+"時："+str(t[3])+"℃ "+str(p[3])+"％ "+str(a[3])+"(mm/h)\n"
                                 +str(h[5])+"時："+str(t[5])+"℃ "+str(p[5])+"％ "+str(a[5])+"(mm/h)"
                                 )
                                 
    line_bot_api.push_message(USER_ID,messages=messages)

if __name__ == "__main__":
    main()