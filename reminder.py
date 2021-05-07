# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:53:26 2021

@author: HP
"""
from win10toast import ToastNotifier

ICON_PATH = "reminderIcon.png"

toast = ToastNotifier()
toast.show_toast("Reminder","Body",duration=20,icon_path=ICON_PATH)