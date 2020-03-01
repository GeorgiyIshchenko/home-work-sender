import requests
from bs4 import BeautifulSoup
import browser_cookie3
import telebot
import random
def inputSN():
    subject=int(input("""Введте предмет:
    1)Алгебра
    2)Русский язык\n"""))
    number = input("Введте номер\n")
    requestdata={"subject":subject,"number":number}
    return requestdata
def chooseURL(data,exception=False):
    global URL
    global copyURL
    if data.get("subject")==1:
        URL+="%d0%b0%d0%bb%d0%b3%d0%b5%d0%b1%d1%80%d0%b0-8-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%bc%d0%be%d1%80%d0%b4%d0%ba%d0%be%d0%b2%d0%b8%d1%87/"
        URL+=data.get("number").split(".")[0]+"-"+data.get("number").split(".")[1]
        if exception:
            copyURL += "%d0%b0%d0%bb%d0%b3%d0%b5%d0%b1%d1%80%d0%b0-8-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%bc%d0%be%d1%80%d0%b4%d0%ba%d0%be%d0%b2%d0%b8%d1%87/"
            copyURL += data.get("number").split(".")[0] + "-" + data.get("number").split(".")[1]
            copyURL+="-"+"2"
            getPicture(copyURL)
        else:
            URL+="-3"
    elif data.get("subject")==2:
        URL += "%d1%80%d1%83%d1%81%d1%81%d0%ba%d0%b8%d0%b9-%d1%8f%d0%b7%d1%8b%d0%ba/"
def getUrl():
    URL="https://xn----7sbbtbnv6bvx1b4d.xn--p1ai/"
    return URL
def getPicture(URL):
    global data
    print(URL)
    request=requests.get(URL).text
    soap=BeautifulSoup(request,"html.parser")
    try:
        article=soap.find("article")
        title=article.find("h1").text
    except:
        title=soap.find("h1")
        title=title.text
        print(title)
    if "Алгебра 8 класс Мордкович" in title:
        print(title)
        div=soap.find("div",class_="entry-attachment")
        ea=div.find("a")
        print(ea.get("href"))
    else:
        chooseURL(data,True)
data=inputSN()
URL=getUrl()
copyURL=URL
chooseURL(data)
print(data)
getPicture(URL)
