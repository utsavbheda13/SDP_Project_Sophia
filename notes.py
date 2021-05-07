# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:24:26 2021

@author: HP
"""
import datetime
import speech_recognition as sr
import pyttsx3
import os

def initialize():
    global listener
    global engine
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)


def save_note():
    title=''
    text=''
    initialize()
    ts = str(datetime.datetime.now().time())
    ts = ts.split('.')
    x = ts[0].split(':')
    fn=""
    for c in x:
        fn+=c
    fn+=ts[1]
    
    try:
        with sr.Microphone() as source:
            listener.energy_threshold = 2000
            listener.pause_threshold = 1
            #voice = listener.adjust_for_ambient_noise(source,1)
            engine.say('Speak that you want me to add to the note.')
            engine.runAndWait()
            voice = listener.listen(source,timeout=5,phrase_time_limit=10)
            cmd = listener.recognize_google(voice)
            cmd = cmd.lower()
            print(cmd)
            text=cmd
            engine.say('Give The Title of the Note.')
            engine.runAndWait()
            voice = listener.listen(source,timeout=5,phrase_time_limit=10)
            ttl = listener.recognize_google(voice)
            ttl = ttl.lower()
            print(ttl)
            title=ttl        
            
    except Exception as e:
        print(e)
    
    
    if(title==""):
        title=fn
    title+=".txt"
    with open(title,"w") as file:
        file.write(text)
        
