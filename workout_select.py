from __future__ import unicode_literals
from cgitb import text
import os
from tokenize import Double
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import workout_crawler
import configparser
import mysql
import calender

receive = [[]]

def setting(message):
    if message == '基本資料設定':
        reply = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='基本資料設定',
                text='是否已經設定過資料',
                actions=[
                    MessageTemplateAction(
                        label='已設定，欲修改基本資料',
                        text='已設定，欲修改基本資料'
                    ),MessageTemplateAction(
                        label='未設定，欲創建資料',
                        text='未設定，欲創建資料'
                    )
                ]
            )
        )
    return reply

def select_sport(message,status):
    text = message
    if status == 0:
        reply = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='部位',
                text='請選擇訓練部位',
                actions=[
                    MessageTemplateAction(
                        label='胸部',
                        text='胸部'
                    ),MessageTemplateAction(
                        label='背部',
                        text='背部'
                    ),MessageTemplateAction(
                        label='腿部',
                        text='腿部'
                    ),MessageTemplateAction(
                        label='腹部',
                        text='腹部'
                    )
                ]
            )
        )
    elif status == 1 :
        if message == '胸部':
            text = "chest"
        elif message == '背部':
            text = "back"
        elif message == '腿部':
            text = "leg"
        elif message == '腹部':
            text = "abs"
    
        receive = workout_crawler.pos_crawler(text)
        print(receive)
        link = calender.calenderURL(receive[0][0],receive[0][0],"20220527T10000000Z/20220527T010000Z")

        reply = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title=receive[0][0],
                            text=receive[0][2],
                            actions=[
                                URITemplateAction(                                                     
                                        label='前往詳細解說',
                                        uri=receive[0][1]
                                        ),
                                URITemplateAction(                                                     
                                        label='加入行事曆',
                                        uri=link #receive[0][1] #url_sport(receive[0][0],":::","20220527T10000000Z/20220527T010000Z"),
                                        )
                            ]
                            
                        ),
                        CarouselColumn(
                            title=receive[1][0],
                            text=receive[1][2],
                            
                            actions=[
                                URITemplateAction(                                                     
                                        label='前往詳細解說',
                                        uri=receive[1][1]
                                        ),
                                URITemplateAction(                                                     
                                        label='加入行事曆',
                                        uri=link #receive[0][1] #url_sport(receive[0][1],":::","20220527T10000000Z/20220527T010000Z"),
                                        )
                            ]
                            
                        ),
                        CarouselColumn(
                            title=receive[2][0],
                            text=receive[2][2],
                            actions=[
                                URITemplateAction(                                                     
                                        label='前往詳細解說',
                                        uri=receive[2][1]
                                        ),
                                URITemplateAction(                                                     
                                        label='加入行事曆',
                                        uri=link #receive[0][1] #url_sport(receive[0][0],":::","20220527T10000000Z/20220527T010000Z"),
                                        )
                            ]
                            
                        ),CarouselColumn(
                            title=receive[2][0],
                            text=receive[2][2],
                            actions=[
                                URITemplateAction(                                                     
                                        label='更多選擇',
                                        uri=receive[0][1]
                                        ),
                                URITemplateAction(                                                     
                                        label='更多選擇',
                                        uri=link #receive[0][1] #url_sport(receive[0][0],":::","20220527T10000000Z/20220527T010000Z"),
                                        )
                            ]
                            
                        )
                    ]
                )
            )


    
    return reply
        


    

    
    """
    elif message[:3] == '!目標':
        reply = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='減重',
                text='請選擇減重方式',
                actions=[
                    MessageTemplateAction(
                        label='飲食',
                        text='飲食'
                    ),MessageTemplateAction(
                        label='運動',
                        text='運動'
                    )
                ]
            )
        )
    """
    return reply
 
def select_food(message,status,num):

    if message == "飲食" or status == 0:
        reply = TemplateSendMessage( #用模板回傳
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='菜單',
                text='選擇用餐時段',
                actions=[
                    MessageTemplateAction(
                        label='早餐',
                        text='早餐'
                    ),
                    MessageTemplateAction(
                       label='午餐',
                       text='午餐'
                    ),
                    MessageTemplateAction(
                        label='晚餐',
                        text='晚餐'
                    )
                ]
            )
        )
        return reply
    elif status == 1 :
        reply = TemplateSendMessage( #用模板回傳
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='菜單',
                text='選擇類型',
                actions=[
                    MessageTemplateAction(
                        label='高蛋白值餐',
                        text='高蛋白'
                    ),
                    MessageTemplateAction(
                       label='低熱量餐',
                       text='低熱量'
                    ),
                    MessageTemplateAction(
                        label='低碳水餐',
                        text='低碳水'
                    )
                ]
            )
        )
        return reply
    elif status == 2:

        #print(input)
        global receive
        receive = message

        print(type(receive))
        print("IIIIIIIIIIIIIIIIIIIIIII")
        print(num)
        #link = calender.calenderURL(receive[0][0],receive[0][0],"20220527T10000000Z/20220527T010000Z")


        reply = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title=receive[num][0],
                        thumbnail_image_url=receive[num][3],
                        text="內容",
                        actions=[
                            URITemplateAction(                                                     
                                    label='前往詳細解說',
                                    uri=receive[num][1]
                                    ),
                            URITemplateAction(                                                     
                                    label='加入行事曆',
                                    uri=receive[num][1]
                                    )
                        ]
                            
                    ),
                    CarouselColumn(
                        title=receive[num+1][0],
                        thumbnail_image_url=receive[num+1][3],
                        text="內容",              
                        actions=[
                            URITemplateAction(                                                     
                                    label='前往詳細解說',
                                    uri=receive[num+1][1]
                                    ),
                            URITemplateAction(                                                     
                                    label='加入行事曆',
                                    uri=receive[num+1][1]
                                    )        
                        ]
                            
                    ),
                    CarouselColumn(
                        title=receive[num+2][0],
                        thumbnail_image_url=receive[num+2][3],
                        text="內容",              
                        actions=[
                            URITemplateAction(                                                     
                                    label='前往詳細解說',
                                    uri=receive[num+2][1]
                                    ),
                            URITemplateAction(                                                     
                                    label='加入行事曆',
                                    uri=receive[num+2][1]
                                    )
                        ]
                            
                    ),
                    CarouselColumn(
                        title="更多選擇",
                        thumbnail_image_url=receive[num+4][3],
                        text="內容",              
                        actions=[
                            MessageTemplateAction(
                                    label='更多菜單',
                                    text='更多菜單'
                            ),
                            MessageTemplateAction(
                                    label='重新選擇類型',
                                    text='重新選擇類型'
                            )
                        ]
                            
                    ),
                    
                ]
            )
        )

        for i in range(num,num+2):
            print(receive[i][0].strip())
            print(receive[i][1].strip())
        print(receive[9][0].strip())
        print(receive[10][0].strip())

        print("FFFFFFFFFFFFFFFFFF")
        return reply

    
    

    """
        reply = TemplateSendMessage( #用模板回傳
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='菜單',
                text='選擇菜單',
                actions=[
                    MessageTemplateAction(
                        label='披薩',
                        text='披薩'
                    ),
                    MessageTemplateAction(
                       label='義大利麵',
                       text='義大利麵'
                    ),
                    MessageTemplateAction(
                        label='焗烤',
                        text= '焗烤'
                    )
                ]
            )
        )
    elif status == 3:
        text = message
        receive = workout_crawler.cra(input)

        print(receive[1][0].strip())
        print(receive[1][1].strip())
        reply = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        #thumbnail_image_url=content[0][3],
                        title=receive[0][0],
                        text=receive[0][2],
                        actions=[
                            URITemplateAction(                                                     
                                label='前往詳細解說',
                                uri=receive[0][1]
                            )          
                        ]),
                    CarouselColumn(
                        #thumbnail_image_url=content[0][3],
                        title=receive[1][0],
                        text=receive[1][2],
                        actions=[
                            URITemplateAction(                                                     
                                label='前往詳細解說',
                                uri=receive[1][1]
                            )            
                        ]),
                    CarouselColumn(
                        #thumbnail_image_url=content[0][3],
                        title=receive[2][0],
                        text=receive[2][2],
                        actions=[
                            URITemplateAction(                                                     
                                label='前往詳細解說',
                                uri=receive[2][1]
                            )            
                        ])
                ]
            )
        )
        return reply
    """
"""
def url_sport(type,body,date) :
    return calender.calenderURL(type,body,date)
    print("url_sport")

def url_food(time,menu,date) :
    return calender.calenderURL(type,menu,date)
    print("url_food")
"""