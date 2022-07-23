from __future__ import unicode_literals
import os
from random import random
from tokenize import Double
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import configparser
import requests
import json
import random
import numpy

def where_eat(message,food):
    GOOGLE_API_KEY = "AIzaSyCjBO3RjIUR9qyLQGRyP7cweNk1VsLV7Wk"
    '''if message[0:3] == "隨便吃":
        address = ""
        lineMes = message
        if lineMes[4:-1] == "":
            address = "台中市西屯區文華路100號"
        else:
            address = lineMes[4:-1]'''
    address = message
    addurl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY,address)

    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()
    ##temp = json.loads(addressDoc.text)
    text = addressReq.text
    #print(text)
    lat = addressDoc['results'][0]['geometry']['location']['lat']
    lng = addressDoc['results'][0]['geometry']['location']['lng']

    foodStoreSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW&keyword={}".format(GOOGLE_API_KEY,lat,lng,food)

    foodReq = requests.get(foodStoreSearch)
    nearby_restaurant_dict = foodReq.json()
    text = foodReq.text
    print(text)
    top20_restaurant = nearby_restaurant_dict["results"]
    res_num = (len(top20_restaurant))
    print(res_num)
    #取得高於3.9的
    bravo=[]
    for i in range(res_num):
        try:
            if top20_restaurant[i]['rating'] > 3.9:
                #print('rate: ',top20_restaurant[i]['rating'])
                bravo.append(i)
        except:
            KeyError
    if len(bravo) < 0:
        content = "沒東西可以吃"
        #restaurant = random.choice(top20_restaurant)沒有的話隨便選一間
    #從高於3.9隨便選一間
    a = numpy.array(top20_restaurant)
    restaurant = a[numpy.random.choice(bravo,3,False)]
    print(restaurant[0])
    #檢查餐廳有無照片
    i=0
    map_url2=[]
    details2=[]
    thumbnail_image_url2=[]
    for i in range(3):
        print(i)
        
        if restaurant[i].get("photos") is None:
            thumbnail_image_url = None
            thumbnail_image_url2.append(thumbnail_image_url)
        else:
            #根據文件，最多一張照片
            photo_reference = restaurant[i]["photos"][0]["photo_reference"]
            photo_width = restaurant[i]["photos"][0]["width"]
            thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(GOOGLE_API_KEY,photo_reference,photo_width)
            thumbnail_image_url2.append(thumbnail_image_url)
        #print(thumbnail_image_url2)
        
        #組裝餐廳資訊
        rating = "無" if restaurant[i].get("rating") is None else restaurant[i]["rating"]
        address = "沒有資料" if restaurant[i].get("vicinity") is None else restaurant[i]["vicinity"]
        details = "Google Map評分 : {}\n地址 : {}".format(rating,address)
        details2.append(details)
        #print(details2)

        #取得餐廳的網址
        map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(lat=restaurant[i]["geometry"]["location"]["lat"],long=restaurant[i]["geometry"]["location"]["lng"],place_id=restaurant[i]["place_id"])
        map_url2.append(map_url)
        #print(map_url2)

    reply = TemplateSendMessage(
        ##alt_text=restaurant[0]["name"],
        alt_text='餐廳資訊',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url = thumbnail_image_url2[0],
                    title=restaurant[0]["name"],
                    text=details2[0],
                    actions=[
                        URITemplateAction(
                            label = '查看地圖',
                            uri = map_url2[0]
                        ),
                    ]),
                CarouselColumn(
                    thumbnail_image_url = thumbnail_image_url2[1],
                    title=restaurant[1]["name"],
                    text=details2[1],
                    actions=[
                        URITemplateAction(
                            label = '查看地圖',
                            uri = map_url2[1]
                        ),
                    ]),
                CarouselColumn(
                    thumbnail_image_url = thumbnail_image_url2[2],
                    title=restaurant[2]["name"],
                    text=details2[2],
                    actions=[
                        URITemplateAction(
                            label = '查看地圖',
                            uri = map_url2[2]
                        ),
                    ])
            ]
        )
    )

    return reply








