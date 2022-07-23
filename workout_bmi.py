from __future__ import unicode_literals
import os
from tokenize import Double
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,CarouselTemplate,CarouselColumn,URITemplateAction
import configparser

def bmi(message):
    content = list(map(int, message[5:].split()))
    hight = content[0]/100
    weight = content[1]
    bmi = weight/(hight*hight)
    bmiNumber = round(bmi, 1)
    #跟健康體位的差距
    if bmiNumber < 18.5:
        standard_weight = 18.5 * (hight*hight) 
        goal =  standard_weight - weight
        goalNumber = round(goal, 1)
    else:
        standard_weight = 23.9 * (hight*hight) 
        goal = weight - standard_weight
        goalNumber = round(goal, 1)
    # bmi分析
    if bmiNumber<18.5:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n體重過輕，需要多運動，均衡飲食，以增加體能，維持健康!\n"+"距離健康體位還差"+str(goalNumber)+"kg")
    elif bmiNumber<24 and bmiNumber>=18.5:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n恭喜!健康體位，要繼續保持")
    elif bmiNumber<27 and bmiNumber>=24:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n過重要小心囉\n"+"距離健康體位還差"+str(goalNumber)+"kg")
    elif bmiNumber<30 and bmiNumber>=27:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n輕度肥胖要小心囉，趕快力行「健康體重管理」\n"+"距離健康體位還差"+str(goalNumber)+"kg")
    elif bmiNumber<35 and bmiNumber>=30:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n中度肥胖要小心囉，趕快力行「健康體重管理」\n"+"距離健康體位還差"+str(goalNumber)+"kg")
    elif bmiNumber>=35:
        reply = TextSendMessage(text="你的bmi值 : "+ str(bmiNumber)+"\n阿~重度肥胖，需要立刻力行「健康體重管理」囉!\n"+"距離健康體位還差"+str(goalNumber)+"kg")

    return reply, hight, weight, bmi