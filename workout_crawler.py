from ast import Num
import requests
from bs4 import BeautifulSoup
from opencc import OpenCC

num = 0
def pos_crawler(goal):
    num = 0
    if goal == "chest":
        num =  9
    elif goal =="back":
        num = 11 
    elif goal =="leg":
        num = 14 
    elif goal =="abs":
        num = 20 
    base = "https://www.hiyd.com"
    url  = "https://www.hiyd.com/dongzuo/?muscle="+str(num)
    re   = requests.get(url)

    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("div", {"class": "cont"})

    content = []
    result = []
    cc = OpenCC('s2t')

    for index, d in enumerate(data):
        if index <4:
            title = d.a.span.getText()
            c_title=cc.convert(title)

            href  = base + d.a.get("href")

            text = d.div.getText().strip()
            c_text = cc.convert(text)

            #imgurl = 
            content = [c_title , href,c_text]
            result.append(content)
        else:
            break

    return result

def cra(input,count,page):
    user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
    headers = {'User-Agent': user_agent}
    global num
    


    base = "https://icook.tw/"
    url  = "https://icook.tw/search/" + input + "/?page=" + str(page)
    response   = requests.get(url, headers=headers)
    r = requests.get(url, headers=headers)
    print(url)

    #print(response.encoding)
    print(r.status_code)
    print(response.headers)
    #print(response.text)

    if response.status_code == 200:
        print(f"successfully connected to: {url}")
    else:
        print(f"error while crawling: {url}")

    content = []
    result = []

    soup = BeautifulSoup(response.text, "html.parser")
    h2_tag = soup.find_all("h2",{"class":"browse-recipe-name"})
    data = soup.find_all("li", {"class": "browse-recipe-item"})
    #print(data)
    """test output

    ???
    #print(h2_tag)

    for d in h2_tag:
       #print(d.text)
        print(d.string)
    for d in data:
      #print(d.text)
       #print(d.text)
       print(base+d.a.get("href"))

    """
    print(count)
    for index, d in enumerate(data): #index -> i , d -> data , count = 初始位置.
        if index < 18 :
            title = d.h2.getText()
            href  = base + d.a.get("href")
            image  = d.img.get("data-src")
            text = d.div.getText().strip()
            print(image)

            #imgurl = 
            content = [title , href, text, image]
            result.append(content)
            print(content)
        else:
            break



    return result

