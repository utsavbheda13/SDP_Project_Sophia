# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:09:33 2021

@author: HP
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import socket_client
import os
import sys
import threading
from recognizer import perform_task,create_instances
from tmodel import load_data,load_model,chat
kivy.require("1.10.1")

import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
import datetime
import wikipedia as wiki
import pyjokes
import smtplib
from tmodel import chat
from nltk.stem.lancaster import LancasterStemmer
from basicCalculator import calculate
from notes import save_note

stemmer = LancasterStemmer()

import numpy
import tflearn
import json
import random
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer


class ScrollableLabel(ScrollView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)
        
        self.chat_history = Label(size_hint_y=None,markup = True)
        self.scroll_to_point = Label()
        
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)
    
    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message
        
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98,None)
        
        self.scroll_to(self.scroll_to_point)
        
    def update_chat_history_layout(self,_=None):
        self.layout.height = self.chat_history.texture_size[1]+15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)
        

class ConnectPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt","r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
        else:
            prev_ip = ""
            prev_port = ""
            prev_username = ""           
                
        self.add_widget(Label(text="IP:"))
        
        self.ip = TextInput(text=prev_ip,multiline=False)
        self.add_widget(self.ip)
        
        self.add_widget(Label(text="Port:"))
        
        self.port = TextInput(text=prev_port,multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text="Username:"))
        
        self.username = TextInput(text=prev_username,multiline=False)
        self.add_widget(self.username)
        
        self.join = Button(text="Join")
        self.join.bind(on_press = self.join_button)
        self.add_widget(Label())
        self.add_widget(self.join)        

    def join_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text
        
        with open("prev_details.txt","w") as f:
            f.write(f"{ip},{port},{username}")
        
        info = f"Attempting to join {ip}:{port} as {username}"
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = "Info"
        Clock.schedule_once(self.connect, 1)
        
    def connect(self, _):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text
        
        if not socket_client.connect(ip, port, username, show_error):
            return
        chat_app.create_chat_page()
        chat_app.screen_manager.current = "Chat"
        
class InfoPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1 
        self.message = Label(halign="center", valign="middle",font_size=30)
        self.message.bind(width = self.update_text_width)
        self.add_widget(self.message)
    
    def update_info(self,message):
        self.message.text = message
    
    def update_text_width(self,*_):
        self.message.text_size = (self.message.width*0.9,None)
 
class ChatPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.cols = 1 
        self.rows = 2

        
        self.history = ScrollableLabel(height = Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)
        

        
        self.new_message = TextInput(width = Window.size[0]*0.8,size_hint_x=None,multiline = False)
        #self.send = Button(text="Send")
        #self.send.bind(on_press=self.send_message)
        self.speak = Button(text = "Speak")
        self.speak.bind(on_press = self.start_recognizing)
        
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        #bottom_line.add_widget(self.send)
        bottom_line.add_widget(self.speak)
        self.add_widget(bottom_line)
        
        Window.bind(on_key_down=self.on_key_down)
        
        Clock.schedule_once(self.focus_text_input,1)
        socket_client.start_listening(self.incoming_message, show_error)
        self.bind(size=self.adjust_fields)
        
    def adjust_fields(self, *_):
        
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height
        
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width
        
        Clock.schedule_once(self.history.update_chat_history_layout,0.01)
        
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_message(None)


    def start_recognizing(self, _):
        
        global listener
        global engine
        listener = sr.Recognizer()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 180)
        #engine.say('Hello Sir,what can i do for you?')
        engine.runAndWait()
        
        create_instances()
        load_data()                
        load_model()
        
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
                        self.new_message.text = command
                        self.send_message(None)
                        
                        
                    if 'sofia' in command:
                        command = command.replace('sofia','')
                    if 'sophia' in command:
                        command = command.replace('sophia','')
                    
                            
            except Exception as e:
                print(e)
            return command
        
        # def reply(text):
        #     print(text)
        #     engine.say(text)
        #     engine.runAndWait()
        
        # def perform_task(classification,command):
        #     if 'youtube' in classification:
        #         song = command.replace('play','')
        #         reply('playing '+song)
        #         pk.playonyt(song)
        #         return "playing" + song
            
        #     elif 'google' in classification:
        #         search_str = command.replace('google', '')
        #         reply('searching' + search_str)
        #         pk.search(search_str)
        #         return "searching" + search_str
            
        #     elif 'wiki' in classification:
        #         thing = command.replace('wikipedia','')
        #         info = wiki.summary(thing, 3)
        #         reply(info)
        #         return info
            
        #     elif 'joke' in classification:
        #         joke = pyjokes.get_joke() 
        #         reply(joke)
        #         return joke
        
        #     elif 'mail' in classification:
        #         recipient = command.split('to')[1]
        #         if 'utsav' in recipient:
        #             mailid = "utsavbheda2001138@gmail.com"
        #         if 'jay' in recipient:
        #             mailid = "jaygoru03@gmail.com"
                
        #         reply("please provide the message")
        #         with sr.Microphone() as source:
        #             voice = listener.listen(source,timeout=5,phrase_time_limit=20)
        #         command = listener.recognize_google(voice)
        #         command = command.lower()
        #         message = command
                
        #         server = smtplib.SMTP('smtp.gmail.com', 587)
        #         server.starttls()
        #         server.login("pantomath77@gmail.com","l8b@0ma5h77")
        #         server.sendmail("pantomath77@gmail.com",mailid, "Hello!! This is a test message")
        #         return "sending mail"
            
        #     elif 'whatsapp' in classification:
        #         recipient = command.split('to')[1]
        #         if "dad" in recipient:
        #             number = "+919427730782"
        #         if "mom" in recipient:
        #             number = "+919427916840"
                
        #         reply("please provide the message")
        #         with sr.Microphone() as source:
        #             voice = listener.listen(source,timeout=5,phrase_time_limit=20)
        #         command = listener.recognize_google(voice)
        #         command = command.lower()
        #         message = command
                
        #         current_time = datetime.datetime.now()
        #         h = current_time.hour
        #         m = current_time.minute
        #         pk.sendwhatmsg(number, message, h, m+2)
        #         reply("message sent")
        #         return "message sent"
            
        #     elif 'time' in classification:
        #         current_time = datetime.datetime.now().strftime('%I:%M %p')
        #         reply('The Time is '+ current_time)
        #         return "The Time is" + current_time
            
        #     elif 'drive c' in classification:
        #         reply("opening c drive")
        #         os.startfile("C:")        
        #         return "opening c drive"
            
        #     elif 'shut me' in classification:
        #         reply('shutting down in about a minute')
        #         pk.shutdown(60)
        #         return "shutting down"
            
        #     elif 'canacel shutdown' in classification:
        #         reply('Cancelling shut down')
        #         pk.cancelShutdown()
        #         return "cancelling shutdown"
            
        #     elif ('shut yourself' in classification) or ('Goodbye!' in classification) or ('Sad to see you go' in classification) or ('Talk to you later' in classification) or ('hopeing to see you again' in classification) or ('the pleasure was mine' in classification):
        #         reply("Have a Good Day, Sir!!!")
        #         return 'quit'
        
        #     elif command == 'nothing':
        #         return ''
            
        #     elif 'calculator' in classification :
        #         reply("Give me numbers and I will try it.")
        #         results = calculate()
        #         reply(results)
        #         return results
            
        #     elif 'add_note' in classification :
        #         save_note()
        #         return "Note added"
            
        #     else:
        #         reply(classification)
        #         return classification
        
        def start_recognition():
            command = take_command()
            resp = chat(command)
            res = perform_task(resp,command)
            return res
        
        def boot():
            
            res = start_recognition()
            if 'quit' in res:
                return
            else: 
                self.new_message.text = str(res)                
                self.message_from_assistant(None)
        
        t4 = threading.Thread(target=boot(),args=(None))
        t4.start()
        t4.join()
    
    def message_from_assistant(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(f"[color=ff2020]sophia[/color] > {message}")
            socket_client.send(message)
            
        Clock.schedule_once(self.focus_text_input,0.1)
    
    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(f"[color=dd2020]{chat_app.connect_page.username.text}[/color] > {message}")
            socket_client.send(message)
            
        Clock.schedule_once(self.focus_text_input,0.1)
    
    def focus_text_input(self, _):
        self.new_message.focus = True
    
    def incoming_message(self,username,message):
        self.history.update_chat_history(f"[color=20dd20]{username}[/color] > {message}")
        return True
        
class EpicApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.connect_page = ConnectPage()
        screen = Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)
 
        self.info_page = InfoPage()
        screen = Screen(name = "Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager

    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name = "Chat")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)

def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 10)
    

if __name__ == "__main__":
    chat_app = EpicApp()
    chat_app.run()