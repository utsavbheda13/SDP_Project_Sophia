# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:11:53 2020

@author: HP
"""

import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
import datetime
import wikipedia as wiki
import pyjokes
import site

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('Hello Sir,what can i do for you?')
engine.runAndWait()

def reply(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'sofia' in command:
                command = command.replace('sofia','')
    except Exception as e:
        print(e)
    return command

def start_recognition():
    command = take_command()
    
    if 'play' in command:
        song = command.replace('play','')
        reply('playing '+song)
        pk.playonyt(song)
    
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        reply('The Time is '+ time)
    
    elif 'who' in command:
        thing = command.replace('who is','')
        info = wiki.summary(thing, 3)
        reply(info)
    
    elif 'joke' in command:
        reply(pyjokes.get_joke())
    
    elif 'quit' in command:
        reply("Have a Good Day, Sir!!!")
        return
        
    else:
        reply('I am sorry, I did not get it, Can you repeat?')

while True:
    start_recognition()