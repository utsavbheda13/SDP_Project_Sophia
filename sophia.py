# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 18:58:46 2021

@author: HP
"""
from recognizer import start_recognition,create_instances
from tmodel import load_data,load_model
 
create_instances()
load_data()
load_model()

while True:
    res = start_recognition()
    if 'quit' in res:
        break
        
        