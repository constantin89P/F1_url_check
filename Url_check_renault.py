import datetime as dt
import requests, sys, tweepy, os
from time import sleep




# Check a webpage every x seconds for tickets opening for an event 
# If any change in the html page, get alerted on my phone by sending a message to my twitter





url1 = "https://atelier.renault.com/evenements/"
url2 = "https://atelier.renault.com/evenements/grand-prix-2021-2-2/"

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
myID = os.getenv('myID')

dic1 = {}
dic1['url'] = "https://atelier.renault.com/evenements/"
dic1['div'] = 0
dic1['class'] = 0
dic1['a'] = 0
dic1['href'] = 0
dic1['span'] = 0
dic1['textes'] = 0


def twitter_api(*text):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    try : 
        api = tweepy.API(auth)
        for string in text :
            api.send_direct_message(myID, string)
    except : 
        for string in text : 
            print("TWITTER ERROR, can't print. Message : ", text)

def check_element(text, element):
    try : 
        nb = text.count(element)
    except : 
        print("Element", element, "not found")

    return nb

def save_values(dic):
    url = dic['url']
    r = requests.get(url)
    full_text = r.text

    # Check the number of div in whole page
    dic['div'] = check_element(full_text, "div")
    dic['class'] = check_element(full_text, "class")
    dic['a'] = check_element(full_text, "/a")
    dic['href'] = check_element(full_text, "href")
    dic['span'] = check_element(full_text, "span")
    dic['textes'] = check_element(full_text, "text")

def search_in_url(dic, *texts):
    url = dic['url']
    r = requests.get(url)
    full_text = r.text
    # check number of specific text
    for string in texts :
        try : 
            nb = full_text.count(string)
            print("Element", string, " found :", nb)
        except :
            print("Element not found")

    # Check the number of div in whole page
    div = check_element(full_text, "div")
    if div != dic['div'] : twitter_api("Changement DIV ! ") ; print("CHANGEMENT")
    classe = check_element(full_text, "class")
    if classe != dic['class'] : twitter_api("Changement CLASS ! ") ; print("CHANGEMENT")
    a = check_element(full_text, "/a")
    if a != dic['a'] : twitter_api("Changement /A ! ") ; print("CHANGEMENT")
    href = check_element(full_text, "href")
    if href != dic['href'] : twitter_api("Changement HREF ! ") ; print("CHANGEMENT")
    span = check_element(full_text, "span")
    if span != dic['span'] : twitter_api("Changement SPAN ! ") ; print("CHANGEMENT")
    textes = check_element(full_text, "text")
    if textes != dic['textes'] : twitter_api("Changement TEXTE ! ") ; print("CHANGEMENT")

# save the original html code and values at the begining
html1 = set(requests.get(url1))
html11 = requests.get(url1)
html2 = set(requests.get(url2))
html22 = requests.get(url2)

save_values(dic1)
# print(dic1['class'])

now = dt.datetime.now()
heure = now.strftime("%H:%M:%S")
print("Début du script", heure)



while True : 

    a = set(requests.get(url1))
    b = set(requests.get(url2))

    search_in_url(dic1)


    now = dt.datetime.now()
    heure = now.strftime("%H:%M:%S")
    print(heure)

    sleep(2)



