import webbrowser 
def calenderURL(title,texts,date):
    #cal_url = 'https://www.google.com/calendar/render?action=TEMPLATE&text=請輸入text&details=請輸入details&dates=20220527T000000Z/20220527T090000Z'
    
    text = title
    details = texts
    dates = date

    cal_url = 'https://www.google.com/calendar/render?action=TEMPLATE&text=' + title + '&details=' + texts + '&dates=' + dates 
    #&title=請輸入title
    return cal_url

"""
urL= calenderURL()
chrome_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new(urL)
"""