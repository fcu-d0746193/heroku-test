from cgi import test
import pymysql
from soupsieve import select;
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,CarouselTemplate,CarouselColumn,URITemplateAction

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "88977997",
    "db": "linebot",
    "charset": "utf8"
}


def confirm(user_id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        print("OK")
       
        #user_id = "004" 測試用

        # 建立Cursor物件
        cursor = conn.cursor()
        #with conn.cursor() as cursor:
        #command = "select * from user where id = '%s' " % user_id
        command = " select 1 from user where id = '%s' " % user_id
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        print("------------") 
        #print(type(result)) #tuple 
        #print(type(result[0][0]))
        #print(type(result)) #tuple
        #print(result) #空值
        #print(result[0][0])    

        if len(result) == 0 :
           print("你尚未輸入任何資料過，請先設定基本資料")
           reply = TextSendMessage(text="你尚未輸入任何資料過，請先設定基本資料輸入 身高(cm)空格 體重(kg)")
           flag = 0
        elif result[0][0] == 0 :
            print("???")
        elif result == None:
            print("悾悾")
        elif not result:
            print("564651")
        elif result:
            print("你已經設定過了，請輸入欲更新的資料([身高(cm)] [體重(kg)])")
            reply = TextSendMessage(text="你已經設定過了，請輸入欲更新的資料 身高(cm) 體重(kg)")
            flag = 1
        
        print("NOOOOOOOOOOOOO")
    except Exception as ex:
       print(ex)

    return reply,flag


def bmi(hight,weight,bmi,user_id,flag):

    conn = pymysql.connect(**db_settings)
    print("OK")
    cursor = conn.cursor()
    #command = "SELECT * FROM user  WHERE id = '%s' " % user_id
    #command = "UPDATE user SET height = 200  WHERE id = '%s' " % user_id
    command = ""
    tuple = ()
    print(type(flag))
    print(flag)

    if flag == 0 :
        command = "INSERT INTO user VALUES (%s,%s,%s,%s,%s)"
        tuple = (user_id ,"U_name" , hight, weight, bmi)
    elif flag == 1 :
        command = "UPDATE user SET height = %s, weight = %s, bmi = %s  WHERE id = %s "
        tuple = (hight, weight, bmi, user_id)
    
    #command = "SELECT * FROM user  WHERE id = 1 "
    #command = "SELECT * FROM user  WHERE id = '%s' " % user_id

    # 執行指令
    cursor.execute(command,tuple)
    conn.commit()
    
    command = "SELECT * FROM user  WHERE id = '%s' " % user_id
    cursor.execute(command)

    # 取得所有資料
    result = cursor.fetchall()
    print(result)