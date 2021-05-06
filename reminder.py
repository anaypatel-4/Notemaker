import speech_recognition as sr
import pyttsx3
import datetime as dt
import tkinter as tk
from tkinter import *
import os
import calendar
from bs4 import BeautifulSoup 
from geopy.geocoders import Nominatim
import requests


root = tk.Tk()
root.geometry('300x400+1050+300')
root.title("Amy")
root.resizable(False, False)

# FILE MODULE

my_path = os.path.join("Documents","Tasks.txt")

def writeToFile(text):
    try: 
        with open(my_path,mode = 'a', encoding = 'cp1252') as f:
            f.write(text)
    finally:
        f.close()

def readRem():
    try:
        r= open(my_path, mode = 'r')
        for x in r:
            engine.say(x)
        engine.runAndWait()
    finally:
        r.close()

def cList():
    if os.path.exists(my_path):
        os.remove(my_path)
        engine.say("File deleted")
        engine.runAndWait()
    else:
        engine.say("The file does not exist")
        engine.runAndWait()


# SPEECH MODULE

listener = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate',190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

def setRem():
    engine.say('HI.....I am Amy.......')
    engine.say('How may I help you?')
    engine.runAndWait()
        
    try:
        print('listening....')
        with sr.Microphone() as source:
            voice = listener.listen(source)
            text = listener.recognize_google(voice)
            text = text.replace('remind me to',' ')
            text = text+'\n'
            writeToFile(text)  
            print(text)          

    except speech_recognition.RequestError:
        print('ERROR')    

# WEATHER MODULE
 
label = tk.Label(root, text = 'Enter Location', font = ("times new roman", 18)).pack()
e = Entry(root,font = ("times new roman",15), bd=5, relief=GROOVE)
e.config(fg='black')
e.pack()

def get_weather():
    geolocator = Nominatim(user_agent='Jaimin')
    location = geolocator.geocode(e.get())
    lat = location.latitude
    lon = location.longitude 

    page = requests.get("https://weather.com/en-IN/weather/today/l/{},{}?par=google&temp=c".format(lat,lon))

    soup = BeautifulSoup(page.text, "html.parser") 

    temp = soup.find("span", class_='CurrentConditions--tempValue--3KcTQ')
    print_t = 'Temperature is ' +  temp.text
    engine.say(print_t)
  
    weather = soup.find("div", class_='CurrentConditions--phraseValue--2xXSr')
    print_w = 'Currently ' + weather.text
    engine.say(print_w)
    
    humidity = soup.find("span", attrs={'data-testid':'PercentageValue'})
    print_h = 'Humidity is '+ humidity.text
    engine.say(print_h)

    air_qual_index = soup.find("text", class_='DonutChart--innerValue--k2Z7I')
    print_a = 'Air Quality Index is '+ air_qual_index.text
    engine.say(print_a)

    air_qual = soup.find("p", class_='AirQualityText--severityText--3QoOU')
    print_q = 'Air Quality ' + air_qual.text
    engine.say(print_q)
    engine.runAndWait()

# GUI MODULE

sett = tk.Button(root,text = 'ADD TO LIST', relief = 'groove', command = setRem, fg = "blue", font = "Verdana 14",bd = 2, bg = "sky blue")
sett.pack(pady=15)

readt = tk.Button(root,text = 'READ LIST', relief = 'groove', command = readRem, fg = "blue", font = "Verdana 14",bd = 2, bg = "sky blue")
readt.pack(pady=15)

cleart = tk.Button(root,text = 'CLEAR LIST', relief = 'groove', command = cList, fg = "blue", font = "Verdana 14",bd = 2, bg = "sky blue")
cleart.pack(pady=15)

weather = tk.Button(root,text = 'WEATHER', relief = 'groove', command = get_weather, fg = "blue", font = "Verdana 14",bd = 2, bg = "sky blue")
weather.pack(pady=15)

root.mainloop()
