import requests
from bs4 import BeautifulSoup
def inputSN():
    subject=int(input("""Введте предмет:
    1)Алгебра
    2)Геометрия
    3)Физика\n"""))
    number = input("Введте номер\n")
    requestdata={"subject":subject,"number":number}
    return requestdata
def chooseURL(data):
    global exception
    global URL
    global subjectURL
    subject=data.get("subject")
    if subject==1:
        if exception:
            subjectURL=URL
        subjectURL+="%d0%b0%d0%bb%d0%b3%d0%b5%d0%b1%d1%80%d0%b0-8-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%bc%d0%be%d1%80%d0%b4%d0%ba%d0%be%d0%b2%d0%b8%d1%87/"
        subjectURL+=data.get("number").split(".")[0]+"-"+data.get("number").split(".")[1]
    elif subject==2:
        if exception:
            subjectURL=URL
        subjectURL+="%d0%b3%d0%b5%d0%be%d0%bc%d0%b5%d1%82%d1%80%d0%b8%d1%8f-7-9-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%b0%d1%82%d0%b0%d0%bd%d0%b0%d1%81%d1%8f%d0%bd-%d1%83%d1%87%d0%b5%d0%b1%d0%bd%d0%b8%d0%ba/"
        subjectURL+=data.get("number")
    elif subject==3:
        if exception:
            subjectURL=URL
        subjectURL+="%d1%81%d0%b1%d0%be%d1%80%d0%bd%d0%b8%d0%ba-%d0%b7%d0%b0%d0%b4%d0%b0%d1%87-%d0%bf%d0%be-%d1%84%d0%b8%d0%b7%d0%b8%d0%ba%d0%b5-7-9-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%bb%d1%83%d0%ba%d0%b0%d1%88%d0%b8/"
        subjectURL+=data.get("number")
    if exception>2:
        subjectURL += "-" + str(exception)
        getPicture(subjectURL)
    else:
        subjectURL += "-"+str(exception)
def getUrl(data):
    URL="https://xn----7sbbtbnv6bvx1b4d.xn--p1ai/"
    return URL
def getPicture(URL):
    global data
    global exception
    request=requests.get(URL).text
    soap=BeautifulSoup(request,"html.parser")
    try:
        article=soap.find("article")
        title=article.find("h1").text
    except:
        title=soap.find("h1")
        title=title.text
        print(title)
    if ("Алгебра 8 класс Мордкович" in title and data.get("subject")==1) or ("Геометрия 7-9 класс Атанасян" in title and data.get("subject") == 2) or("7-9 класс Лукашик В.И." in title and data.get("subject")==3):
        print(title)
        div=soap.find("div",class_="entry-attachment")
        ea=div.find("a")
        print(ea.get("href"))
    else:
        exception+=1
        chooseURL(data)
exception=2
data=inputSN()
URL=getUrl(data)
subjectURL=URL
chooseURL(data)
getPicture(subjectURL)
