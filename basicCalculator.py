# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:30:22 2021

@author: HP
"""
import speech_recognition as sr
#import pyttsx3


def calculate():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.energy_threshold = 2000
            listener.pause_threshold = 1
            #voice = listener.adjust_for_ambient_noise(source,1)
            voice = listener.listen(source,timeout=5,phrase_time_limit=10)
            cmd = listener.recognize_google(voice)
            cmd = cmd.lower()
            print(cmd)
            nums=cmd.split( )
            n1=int(nums[0])
            n2=int(nums[2])
            if(nums[1]=="+"):
                return str(n1+n2)
            elif(nums[1]=="-"):
                return str(n1-n2)
            elif(nums[1]=="into" or nums[1]=="×") :
                return str(n1*n2)
            elif(nums[1]=="/" or "divi" in nums[1] or "by" in nums[1]):
                if(n2==0):
                    return "Number can't be divided by zero."
                else:
                    return str(n1/n2)
            else:
                return "I can only do addition, subtraction, multiplication and division!"
    except Exception as e:
        print(e)