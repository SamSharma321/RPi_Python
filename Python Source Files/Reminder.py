#reminder.py

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import googlesearch
import smtplib

reminder_script_path = r'remind.txt'

def take_remind(reminder, time_str, priority, recurring):
    if "p.m." in time_str:
        time_str = time_str.replace(" p.m.", "")
        offset = 12
    else:
        if '12' in time_str:
            time_str = time_str.replace("12", "0") # 12 a.m becomes o in datetime() module
        if "a.m." in time_str:
            time_str = time_str.replace(" a.m.", "")
    # Example input 11 p.m.
    if len(time_str)==2:
        time = time_str + ":00"
    # example input 11:30 p.m.
    else:
        if ':' not in time_str:
            if len(time_str) == 3:
                time = time_str[0] + ':' + time_str[1:2]
            elif len(time_str) == 4:
                time = time_str[0:1] + ':' + time_str[2:3]
        else:        
            time = time_str # Input is as expected
    store_reminder(reminder, time, priority,recurring)
    return reminder

def store_reminder(reminder, time, priority = 'N',recurring='N'):
    data = f'{reminder.strip()};{str(time).strip()};P{priority.strip()};R{recurring.strip()}'
    print(data)
    with open(reminder_script_path, 'r+') as file:
        contents = file.readlines()
        contents.append(data+'\n')   # Read all data, and append the new reminder at last
        file.seek(0)                 # Go back to the beginning of the file
        file.writelines(contents)    # Write the modified list back to the file


def delete_all_reminders():
    with open(reminder_script_path, 'w') as reminds:
        # just pass will clear the file
        pass


def remind():        # TODO a pop up window is better if screen connnected
    info = None
    try:
        with open(reminder_script_path, 'r+') as reminds:
            write_content = []
            contents = reminds.readlines()
            hour = int(datetime.datetime.now().hour)
            if hour > 12:
                hour = hour - 12
            # Get time in mins and secs
            mins = int(datetime.datetime.now().minute)
            now = str(hour) + ':' + str(mins) # format = hh:mm
            # print(now)
            for line in contents:
                line_data = line.split(';')
                # Check if the reminder was deleted
                if line_data != '':
                    # Get the time from the reminder info
                    time = line_data[1]
                    # Check if it is not a priority task
                    if line_data[2] != 'PY':
                        if str(now)==time:
                            # GPIO Remibder alert TODO
                            info = ("Reminder Alert: " + line_data[0])
                    else:
                        time_val = hour + mins/60
                        rec_time = line_data[1].split(':')
                        rec_time_val = int(rec_time[0]) + int(rec_time[1])/60
                        # Check if the reminder is a priority reminder so that it can be reminded 15 mins before the task
                        print(f'{time_val} {rec_time_val} {line_data[1]} {time_val - rec_time_val}')
                        if time_val - rec_time_val <= 0.25:
                            if time_val > 0:
                                # GPIO Reminder alert TODO
                                info = ("Priority Reminder Alert: " + line_data[0]) 
                            line = line.replace(';PY', ';PN')
                    if (line_data[3] == 'RN') and (info != None): # delete reminder if it is not recurring
                        line = r''
                write_content.append(line)
        
        # Write to the file the updated data
        with open(reminder_script_path, 'w') as file:
            file.writelines(write_content)
    except Exception as suspect:
        info = f'{suspect} occured. Clearing all reminders'
        print(info)
        delete_all_reminders()

    return info

def read_reminders():
    reminders = []
    with open(reminder_script_path, 'r') as file:
        content = file.readlines()
        for lines in content:
            if lines != '':
                line_data = lines.split(';')
                reminders.append(f'Reminder at {line_data[1]} to {line_data[0]}')
    return reminders
                



