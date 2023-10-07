from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
today_ymd = datetime.now().strftime('%Y-%m-%d')
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://v0.yiketianqi.com/api?unescape=1&version=v62&appid=63333691&appsecret=4P5xzNwb&city=" + city
  res = requests.get(url).json()
  return res['wea'], res['tem']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"today":{"value":today_ymd, "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
