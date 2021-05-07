# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:00:43 2021

@author: HP
"""
import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
import datetime
import wikipedia as wiki
import pyjokes
import os
import smtplib
from tmodel import chat
from nltk.stem.lancaster import LancasterStemmer
from basicCalculator import calculate
from notes import save_note

stemmer = LancasterStemmer()

def create_instances():
    global listener
    global engine
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
    engine.say('Hello Sir,what can i do for you?')
    engine.runAndWait()
    
def reply(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    # global voice
    try:
        with sr.Microphone() as source:
            command  = "nothing"
            
            while 'sofia' not in command:
                print('listening...')
                listener.energy_threshold = 2000
                listener.pause_threshold = 1
                voice = listener.listen(source,timeout=5,phrase_time_limit=10)
                command = listener.recognize_google(voice)
                command = command.lower()
                print(command)
                
                
            if 'sofia' in command:
                command = command.replace('sofia','')
            if 'sophia' in command:
                command = command.replace('sophia','')
            
                    
    except Exception as e:
        print(e)
    return command

def start_recognition():
    command = take_command()
    resp = chat(command)
    res = perform_task(resp,command)
    return res

def perform_task(classification,command):
    if 'youtube' in classification:
        song = command.replace('play','')
        reply('playing '+song)
        pk.playonyt(song)
        return "playing" + song
    
    elif 'google' in classification:
        search_str = command.replace('google', '')
        reply('searching' + search_str)
        pk.search(search_str)
        return "searching" + search_str
    
    elif 'wiki' in classification:
        thing = command.replace('wikipedia','')
        info = wiki.summary(thing, 3)
        reply(info)
        return info
    
    elif 'joke' in classification:
        joke = pyjokes.get_joke() 
        reply(joke)
        return joke

    elif 'mail' in classification:
        recipient = command.split('to')[1]
        if 'utsav' in recipient:
            mailid = "utsavbheda2001138@gmail.com"
        if 'jay' in recipient:
            mailid = "jaygoru03@gmail.com"
        
        reply("please provide the message")
        with sr.Microphone() as source:
            voice = listener.listen(source,timeout=5,phrase_time_limit=20)
        command = listener.recognize_google(voice)
        command = command.lower()
        message = command
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("pantomath77@gmail.com","l8b@0ma5h77")
        server.sendmail("pantomath77@gmail.com",mailid, "Hello!! This is a test message")
        return "sending mail"
    
    elif 'whatsapp' in classification:
        recipient = command.split('to')[1]
        if "dad" in recipient:
            number = "+919427730782"
        if "mom" in recipient:
            number = "+919427916840"
        
        reply("please provide the message")
        with sr.Microphone() as source:
            voice = listener.listen(source,timeout=5,phrase_time_limit=20)
        command = listener.recognize_google(voice)
        command = command.lower()
        message = command
        
        current_time = datetime.datetime.now()
        h = current_time.hour
        m = current_time.minute
        pk.sendwhatmsg(number, message, h, m+2)
        reply("message sent")
        return "message sent"
    
    elif 'time' in classification:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        reply('The Time is '+ current_time)
        return "The Time is" + current_time
    
    elif 'drive c' in classification:
        reply("opening c drive")
        os.startfile("C:")        
        return "opening c drive"
    
    elif 'shut me' in classification:
        reply('shutting down in about a minute')
        pk.shutdown(60)
        return "shutting down"
    
    elif 'canacel shutdown' in classification:
        reply('Cancelling shut down')
        pk.cancelShutdown()
        return "cancelling shutdown"
    
    elif ('shut yourself' in classification) or ('Goodbye!' in classification) or ('Sad to see you go' in classification) or ('Talk to you later' in classification) or ('hopeing to see you again' in classification) or ('the pleasure was mine' in classification):
        reply("Have a Good Day, Sir!!!")
        return 'quit'

    elif command == 'nothing':
        return ''
    
    elif 'calculator' in classification :
        reply("Give me numbers and I will try it.")
        results = calculate()
        reply(results)
        return results
    
    elif 'add_note' in classification :
        save_note()
        return "Note added"
    
    else:
        reply(classification)
        return classification
    