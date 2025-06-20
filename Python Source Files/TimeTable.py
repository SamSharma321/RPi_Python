import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import googlesearch
import smtplib

chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe %s"

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def NA():
    speak("You are currently scheduled for Network Analysis Class sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/zza-dixt-ndy?authuser=1")
    exit()

def ADDC():
    speak("You are currently scheduled for Analysis and design of digital circuits class sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/hgg-ktzc-jrq?authuser=1")
    exit()

def MATH():
    speak("You are currently scheduled for Mathematics class sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/zqb-yjad-xuy?authuser=1")
    exit()

def AMC():
    speak("You are currently scheduled for Analog Microelectronics class now sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/rda-twrn-zjv?authuser=1")
    exit()

def PEF():
    speak("You are currently scheduled for Principles of Electromagnetic Fields class sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/fho-zdbv-kmo?authuser=1")
    exit()

def BT():
    speak("You are currently scheduled for Environmental Technology class sir!")
    speak("Enjoy your class sir!")
    webbrowser.get(chrome_path).open("https://meet.google.com/bem-qvkj-qwu?authuser=1")
    exit()

def timetable():
    today = datetime.date.today()
    hour = int(datetime.datetime.now().hour)
    min = int(datetime.datetime.now().minute)
    time = hour + (min/60)
    if today.day == 6:

        if time >= 9 and time < 10.16:
            NA()

        elif time >= 10.16 and time < 11.33:
            ADDC()

        elif time >= 11.33 and time < 12.5:
            MATH()

        else:
            speak("There are no classes scheduled for now sir. I'll inform if there are any developments.")

    if today.day == 7:
        if time >= 9 and time < 10.16:
            BT()
        elif time >= 10.16 and time < 11.33:
            AMC()
        elif time >= 11.33 and time < 12.3:
            MATH()
        elif time >= 12.3 and time < 13.5:
            PEF()

    if today.day == 8:
        if time >= 9 and time < 10.16:
            AMC()
        elif time >= 10.16 and time < 11.33:
            NA()
        elif time >= 11.33 and time < 12.3:
            MATH()
        elif time >= 12.5 and time < 13.5:
            ADDC()
        elif time >= 14 and time < 15.16:
            PEF()
        else:
            speak("You are not scheduled for any class now sir!")
