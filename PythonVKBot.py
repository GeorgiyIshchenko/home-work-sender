import vk_api
from vk_api.longpoll import VkLongPoll,VkEventType
import time
import random
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
import json
def upload_photo(upload, url):
    print("фото загружается...")
    img = requests.get(url).content
    f = BytesIO(img)
    response = upload.photo_messages(f)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    return owner_id, photo_id, access_key
def send_photo( vk, peer_id, owner_id, photo_id, access_key, title):
    print("фото отправляется...")
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        message=title,
        attachment=attachment
    )
    print("фото отправлено")
def chooseURL(data):
    global isSend
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

    elif subject == 4:
        if isSend:
            pass
        else:
            isSend=True
            getHistoryStudentBook()
            return
    elif subject==5:
        if isSend:
            pass
        else:
            isSend=True
            getHistoryWorkBook()
            return
    if exception>2:
        subjectURL += "-" + str(exception)
        getPicture(subjectURL)
    else:
        subjectURL += "-"+str(exception)
def getHistoryStudentBook():
    global data
    global upload
    URL="https://resheba.me/gdz/istorija/8-klass/arsentev/"+data.get("number")
    vk.method("messages.send",
              {"peer_id": id, "attachment": URL, "random_id": random.randint(1, 2147483647)})
    return
def getHistoryWorkBook():
    global data
    global upload
    URL="https://www.euroki.org/gdz/ru/istoriya/8_klass/rabochaya-tetrad-po-istorii-rossii-8-klass-artasov-fgos-663/zadanie-str-"+data.get("number")
    request=requests.get(URL).text
    soap=BeautifulSoup(request,"html.parser")
    article=soap.find("a",class_="fancybox")
    send_photo(vk_session, id, *upload_photo(upload, article.get("href")),"История (рабочая тетрадь)")
    return

def getUrl(data):
    URL="https://xn----7sbbtbnv6bvx1b4d.xn--p1ai/"
    return URL
def getPicture(URL):
    global data
    global upload
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
        href=ea.get("href")
        send_photo(vk_session, id, *upload_photo(upload, href),title)
        return
    else:
        exception+=1
        chooseURL(data)

token = "5d35cfe3e0de35412e8a930b8e9004736b239e504c06fa74b379abd7951e6c55d861fd5de3983f26e89f8"

vk = vk_api.VkApi(token=token)
vk._auth_token()
vk_session = vk.get_api()
longpoll = VkLongPoll(vk)
upload = VkUpload(vk_session)
subjects = {"алгебра":1,"геометрия":2,"физика":3,"история (учебник)":4,"история (рабочая тетрадь)":5}
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            try:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    body = messages["items"][0]["last_message"]["text"]
                    message=body.lower()
                    if  message== "привет":
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "понял ", "random_id": random.randint(1, 2147483647)})
                        print(vk.method("photos.getMessagesUploadServer").get("upload_url"))
                        response = requests.post('http://example.com/', data={'photo': 'value'})
                        if response:
                            print('Success!')
                        else:
                            print('An error has occurred.')
                    elif message== "info" or message=="инфо":
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "Хорошо, определимся с упражнением", "random_id": random.randint(1, 2147483647)})
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "Отправь мне предмет и номер упражнения через пробел", "random_id": random.randint(1, 2147483647)})
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "Доступные предметы: Алгебра, Геометрия, Физика, История (учебник), История (рабочая тетрадь).", "random_id": random.randint(1, 2147483647)})

                    elif " ".join(message.split(" ")[0:-1]) in subjects.keys():
                        isSend=False
                        subject=" ".join(message.split(" ")[0:-1])
                        number=message.split(" ")[-1]
                        exception=2
                        data={"subject":subjects.get(subject),"number":number}
                        print(data)
                        exception=2
                        URL=getUrl(data)
                        subjectURL=URL
                        chooseURL(data)
                        getPicture(subjectURL)

            except Exception as E:
                time.sleep(1)
