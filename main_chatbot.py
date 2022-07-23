from __future__ import unicode_literals
import os
from pickle import TUPLE1, TUPLE2
from sqlite3 import connect
from sys import flags
from time import time
from tkinter import Menu
from tokenize import Double
from unicodedata import name
from unittest import result
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from soupsieve import select
import workout_select
import workout_bmi
import map_food
import map_gym
import configparser
import random
import requests
import mysql
import time
import calender
import workout_crawler
import execjs

app = Flask(__name__)

receive = [[]]

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

status1 = 0
status2 = 0
status3 = 0
status4 = 0
num = 0
imput = ""
page = 1

#mysql.confirm()

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 機器人回覆
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    user_id = event.source.user_id
    global status
    global status1
    global status2
    global status3
    global status4
    global flag
    global food_type
    global num
    global input
    global page
    global receive

    print(user_id)

    global food,tag

    print("o o o ")
    print(status2)

    # bmi改變輸入方式
    # 先檢查在輸入還是先輸入後檢查?
    # 是否用confirm template
    if get_message == "基本資料設定" :
        profile = line_bot_api.get_profile(user_id)
        line_bot_api.push_message(user_id,      #教你如何新增資料
            TextSendMessage(text='Hello ~'+ profile.display_name + ' ! 歡迎使用健康小幫手'))

        result_confirm = workout_select.setting(get_message) #設定資料
        line_bot_api.reply_message(event.reply_token,result_confirm)
        IS_setting = mysql.confirm(user_id) #是否存在資料
        print(IS_setting[0])

    elif get_message == '已設定，欲修改基本資料' or get_message == '未設定，欲創建資料':

        IS_setting = mysql.confirm(user_id) #是否存在資料
        print(IS_setting[1])
        
        #變數 flag   0則需要新增 1則需要更新
        if   IS_setting[1] == 0:            #否則新增
            line_bot_api.reply_message(event.reply_token,IS_setting[0])
            flag = 0
        elif IS_setting[1] == 1:            #是則修改
            line_bot_api.reply_message(event.reply_token,IS_setting[0])
            flag = 1

    elif get_message[:4].lower() == '!bmi':    # 改變輸入方式
        result = workout_bmi.bmi(get_message) #計算BMI
        print(type(flag))
        print(flag)


        """select.(100*result[1],result[2],result[3])將身體數據放入行事曆"""
        #link =  'https://www.google.com/calendar/render?action=TEMPLATE&text=' + '身體資料' + '&details=' + '身高 :' +  result[1] + '體重 :' + result[2] +  'BMI : ' + result[3] + '&dates=' 

        #進入DB修改資料
        user_data = mysql.bmi(100*result[1],result[2],result[3],user_id,flag)

        if flag == 0:
            line_bot_api.push_message(user_id,TextSendMessage(text = '成功新增你基本資料了!現在可以...'))  #修改成功訊息 (bmi 要改成改符點數)
        elif flag == 1:
            line_bot_api.push_message(user_id,TextSendMessage(text = '成功更新你的BMI及數值'))  #修改成功訊息 (bmi 要改成改符點數)
        line_bot_api.reply_message(event.reply_token,result[0]) #回傳健康資訊

    elif get_message == "運動" or status2 != 0:
        if get_message == "運動" :
            select = "健身運動"
            #print("AAAAAAAAAA")
            reply2 = workout_select.select_sport(get_message,status2) #status
            #print("****")#print(status2)
            line_bot_api.reply_message(event.reply_token,reply2)
            status2 = 1

        elif status2 == 1 or status2 == 2:
            if get_message == "胸部" or get_message == "背部" or get_message == "腿部" or get_message == "腹部":
                body_part = get_message
                print(get_message)
                status2 = 1
                reply2 = workout_select.select_sport(get_message,status2)#status
                line_bot_api.reply_message(event.reply_token,reply2)
                status2 = 2
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status2 = 0
        elif status2 == 2:
            """選擇是否加入行事曆"""
            if get_message == "加入行事曆" or status2 == 2 :
                #將儲存參數存入...(部位，運動項目)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "完成加入行事曆!"))
                status2 = 0
                #變數 = "" 設為空字串
            else :
                #若輸入字串不為運動基本參數則狀態要歸零
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status2 = 0
                #變數 = "" 設為空字串

    elif get_message == "飲食" or status3 != 0:
        if get_message == "飲食":
            reply3 = workout_select.select_food(get_message,status3,num) #status
            #print("****")#print(status2)
            line_bot_api.reply_message(event.reply_token,reply3)
            status3 = 1
        elif status3 == 1:
            if get_message == "早餐" or get_message == "午餐" or get_message == "晚餐" :#時段
                eat_time = get_message
                reply3 = workout_select.select_food(get_message,status3,num) #status
                line_bot_api.reply_message(event.reply_token,reply3)
                print("??????")
                status3 = 2
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status3 = 0
                eat_time = ""
        elif status3 == 2 :#選擇菜單
            if get_message == "低熱量" or get_message == "高蛋白" :
                input = get_message
                #爬資料儲存後再印出
                if num == 0 :
                    receive = workout_crawler.cra(input,num,page)
                print("Sdfsdfsdfsdffsdfsdfsdfdfsdfsdfsdfsdfsdfsdfsdfsfsfs")
                print(receive)
                reply3 = workout_select.select_food(receive,status3,num) #status
                #print(reply3)
                print(type(reply3))
                line_bot_api.reply_message(event.reply_token,reply3)
                print("SIFJLDJLSDJLSD")
                food_type = get_message
                #status3 = 0 #3
            elif get_message == "更多菜單":
                num = num + 3
                if num >= 18:
                    print("!!!!!!!!!!")
                    print(input)
                    page = page + 1
                    print("!!!!!!!!!!!!!!!!!@!@@@@@@@@@@@@@@@@@@@@")
                    print(page)
                    receive = workout_crawler.cra(input,num,page)
                    num = 0
                reply3 = workout_select.select_food(receive,status3,num) #status
                line_bot_api.reply_message(event.reply_token,reply3)
                status3 = 2
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status3 = 0
                eat_time = ""
                food_type = ""
        """
        elif status3 == 3  : #選擇種類
            if get_message == "披薩"  :#種類
                reply3 = workout_select.select1(get_message) #status
                menu = get_message
                status3 = 3
            else :
                #若輸入字串不為基本參數則狀態要歸零
                status3 = 0
        elif status3 == 4 :#選擇加入行事曆
            if get_message == "加入行事曆"  :#食譜
                reply3 = workout_select.select1(get_message) #status
                status3 = 0
            else :
                status3 = 0
        """

    #要改用status哦 or 就近尋找?
    elif get_message == '尋找周邊' or status4 != 0 :    
        #reply = map_select.m_select(get_message)
        if get_message == '尋找周邊':
            line_bot_api.push_message(user_id,      #教你如何新增資料
                TextSendMessage(text='輸入餐聽類型或健身房'))
            status4 = 1
        elif status4 == 1:
            if get_message == "健身房":
                tag = 1
            else :
                food = get_message
                tag = 0
            reply3 = TextSendMessage(text="請傳送定位")
            line_bot_api.reply_message(event.reply_token, reply3)
        #可改成查看更多
    
    else : 
        print("請先書入圖文選單功能後進行輸入")


    #附近吃什麼
    ##elif get_message[:3] == "隨便吃":
    ##    reply3 = map_food.where_eat(get_message)
    ##   line_bot_api.reply_message(event.reply_token, reply3)

@handler.add(MessageEvent, message=LocationMessage)
def handle_locmessage(event):
    get_type = event.message.type
    global status4
    print(tag)
    #print(get_type)
    #接收位置訊息
    if event.message.type =='location':
        #print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
        address = event.message.address
        print(address)
        latitude = event.message.latitude
        print(latitude)
        longitude = event.message.longitude
        print(longitude)
        if tag == 0:
            reply4 = map_food.where_eat(address,food)
            line_bot_api.reply_message(event.reply_token, reply4)
            status4 = 0
        elif tag == 1:
            reply5 = map_gym.where_gym(address)
            line_bot_api.reply_message(event.reply_token, reply5)
            status4 = 0
    
#if __name__ == "__main__":
#    app.run()