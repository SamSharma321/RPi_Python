# import pyttsx3
from datetime import datetime
import speech_recognition as sr # type: ignore
# import wikipedia
import subprocess
import os
import random
import googlesearch
import smtplib
import pyttsx3
# from TimeTable import timetable TODO not required
from Reminder import remind, take_remind, read_reminders, delete_all_reminders
from Weather import weather_report
import speedtest # module for getting internet speed
import pyowm
# import RealtimeSTT
#trying out gTTS
from gtts import gTTS
gTTS_lang = 'en'
from Data import chrome_path, clean_up_query, get_curr_location
from global_data import visibility
import regex as re

# API keys
owm = pyowm.OWM('1481183c75501986d143a344d9785a00')

# Weather App
observation = owm.weather_manager()
w = observation.weather_at_place('Bangalore, India')

r = sr.Recognizer()



def time():
    """
    Returns the current time in decimal hours (e.g., 14.5 for 2:30 PM)
    """
    hour = int(datetime.now().hour)
    min = int(datetime.now().minute)
    now = hour + (min / 60)
    return now


class VoiceEngine:
    """
    Main class for Jarvis voice assistant functionality.
    Handles speech recognition, text-to-speech, and command processing.
    """
    def __init__(self):
        self.engine = pyttsx3.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate)  
        self.engine.setProperty('volume', 1)  
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

    def speak(self, audio, block = False):
        """
        Converts text to speech and plays it using gTTS.
        
        Args:
            audio (str): Text to be spoken
            block (bool): If True, blocks until speech completes
        """
        self.engine.say(audio)
        self.engine.runAndWait()
        

    def wish_me(self, salutation="sir"):
        '''
        Greets the user based on current time of day.
        
        Args:
            salutation (str): How to address the user (default: "sir")
        '''
        hour = int(datetime.now().hour)
        if 0 <= hour < 12:
            time_day = 'morning'
        elif 12 <= hour < 16:
            time_day = 'afternoon'
        elif 16 <= hour < 19:
            time_day = 'evening'
        else:
            time_day = None

        if time_day is not None:
            self.speak(f"good {time_day} {salutation}!", True)
        else:
            self.speak("Oh hello Sir!", True)

    def takeCommand(self):
        '''
        Listens to microphone input and returns recognized text.
        
        Returns:
            str: Recognized speech text or "None" if recognition fails
        '''
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                print("Recogising...")
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}\n")

            except Exception as e:
                if e != '':
                    print(e)
                return "None"
            return query

    def sendEmail(self, to, content):
        '''
        Sends an email using SMTP protocol.
        
        Args:
            to (str): Recipient email address
            content (str): Email message content
        '''
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Email works on SMTP
        server.ehlo()
        server.starttls()  # server is initiated
        server.login('sharmasameera91@gmail.com', 'Samram123!')  # To login
        server.sendmail('sharmasameera91@gmail.com', to, content)  # sends mail
        server.close()  # Closes the server

    def clean_up_cmd(self, query):
        """
        Cleans up voice command by removing predefined phrases.
        
        Args:
            query (str): Original voice command
        """
        for item in clean_up_query:
            if item in query:
                query = query.replace(item, '')

# Constants for object detection
detection_timeout = 60 # 60 seconds
detect_cnt_limit = 5

def run_jarvis(jarvis):
    """
    Main execution loop for Jarvis voice assistant.
    Handles command processing and response generation.
    
    Args:
        jarvis (VoiceEngine): Instance of the VoiceEngine class
    """
    detect_incr_cnt = 0
    
    jarvis.wish_me()
    now = time()
    if now < 10:
        weather_rpt = weather_report()
        print(weather_rpt)
        jarvis.speak(weather_rpt)
    else:
        jarvis.speak("how may I help you?")
    
    # Check if jarvis has found me for timeout
    if visibility is True:
        capture_time = datetime.now()

    while True:
        # check for reminders
        remind_info = remind()
        if remind_info is not None:
            jarvis.speak(remind_info)
        
        query = ''
        query = jarvis.takeCommand().lower()
        jarvis.clean_up_cmd(query)
        
        if query == "none":
            continue
        
        elif "videos" in query:
            jarvis.speak("What is your specific interest Sir?")
            query = jarvis.takeCommand()
            jarvis.speak("I hope this is what you were looking for!")
            query = query.replace(r" ", '+') # Required for YouTube search
            subprocess.Popen([chrome_path, f"youtube.com/results?search_query={query}"])

        elif all(x in query for x in ['search', 'amazon']):
            query = query.replace("search ", "")
            query = query.replace("amazon ", "")
            if "for" in query:
                query = query.replace("for ", "")
            jarvis.speak("I dug up some results for you. Have a look!")
            query.replace(r" ", '+', query) # Required for search
            subprocess.Popen([chrome_path, f"amazon.in/s?k={query}&ref=nb_sb_noss_1"])

        elif "google meet" in query:
            subprocess.Popen([chrome_path, "https://meet.google.com/wom-hvbj-ubi?pli=1"])

        elif "amazon" in query:
            jarvis.speak("I can do only so much sir!")
            subprocess.Popen([chrome_path, googlesearch.lucky("Amazon")])   # TODO turn any kinda unknown into google search

        elif "introduce me" in query:  # TODO update this to read from a text file
            my_info = open(r'info.txt', 'r').read()
            jarvis.speak(my_info)

        elif "take me to my classes" in query:
            # timetable()
            exit()

        elif (('clear' in query) or ('delete' in query)) and ('reminders' in query):
            delete_all_reminders()
            jarvis.speak("All reminders cleared.")

        elif ("remind me" in query) or all(x in query for x in ['add', 'remind']): # Use REGEX to get data bro
            # initialize priority reminder as no
            priority = 'N'
            # check if keyword priority already present in request
            if 'priority' in query:
                priority = 'Y'
                query = query.replace("priority ", "")
            clean_query_pattern = [r"(remind me )", r"(add a reminder )", r"(to )", r'(at )', r'(should be\s*\w*)']
            for patterns in clean_query_pattern:
                query = re.sub(patterns, '', query, flags=re.IGNORECASE)
            # check if time already mentioned in the query and get time 
            time_str = None
            pattern = r'\d{1,2}(:\d{2})?\s*(a\.m\.|p\.m\.)?'
            matches = re.finditer(pattern, query, re.IGNORECASE)
            if matches is not None:
                for mem_match in re.finditer(pattern, query, re.IGNORECASE):
                    time_str = mem_match.group()
                    query = re.sub(pattern, '', query, flags=re.IGNORECASE)
            else:
                jarvis.speak("Sure sir. When shall I remind you sir?")
                time_str = jarvis.takeCommand()
            # check if priority info already given in query before asking again
            if priority != 'Y':
                jarvis.speak("And is this a priority reminder?")
                priority_data = jarvis.takeCommand()
                yes_pattern = r'(ye)\w'
                yes_matches = re.finditer(yes_pattern, priority_data, re.IGNORECASE)
                if yes_matches is not None:
                    priority = 'Y'
            # ask if the reminder is daily one
            jarvis.speak("Shall I add this as a daily reminder sir?")
            reccuring_data = jarvis.takeCommand()
            reccuring = 'N'
            yes_pattern = r'(ye)\w'
            yes_matches_2 = re.finditer(yes_pattern, reccuring_data, re.IGNORECASE)
            if yes_matches_2 is not None:
                reccuring = 'Y'
            take_remind(query, time_str, priority, reccuring)
            jarvis.speak("Reminder noted.")

        elif 'reminders' in query or any(x in query for x in ['fogotten', 'forgetting']):
            reminders = read_reminders()
            if len(reminders) != 0:
                for reminder in reminders:
                    jarvis.speak(reminder)
            else:
                jarvis.speak("No reminders logged sir.")

        elif ("emails" in query) or ("email" in query):
            jarvis.speak("Just a moment sir!")
            print("Logging in as sharmasameera@gmail.com")
            subprocess.Popen([chrome_path, "gmail.com"])

        elif all(x in query for x in ['google', 'search']):
            query = query.replace("search google ", "")
            if "for" in query:
                query = query.replace("for ", "")
            jarvis.speak("Here you go sir")
            subprocess.Popen([chrome_path,
                              f"https://www.google.co.in/search?safe=active&ei=HLJ-X6-bJbS38QPl7pmYDw&q={query}&oq={query}&gs_lcp=CgZwc3ktYWIQAzIKCC4QyQMQDRCTAjIECAAQDTIECAAQDTIECAAQDTIECAAQDTIECAAQDTIECAAQDTIECAAQDTIECAAQDTIECAAQDToOCAAQ6gIQtAIQmgEQ5QI6CggAELEDEMkDEEM6BAgAEEM6BAguEEM6CAgAELEDEIMBOgUIABCxAzoCCAA6AgguOgcIABDJAxBDOgoILhDHARCjAhBDOg0ILhCxAxDHARCjAhBDOgUILhCxAzoQCC4QxwEQowIQyQMQQxCTAjoHCC4QsQMQQzoNCC4QsQMQyQMQQxCTAjoICC4QsQMQgwE6CwguELEDEMkDEJMCUNaRD1itsg9gu7cPaAFwAXgAgAHWAYgBpBGSAQYzLjE0LjGYAQCgAQGqAQdnd3Mtd2l6sAEGwAEB&sclient=psy-ab&ved=0ahUKEwivmZTKr6TsAhW0W3wKHWV3BvMQ4dUDCA0&uact=5"])

        elif ("messages" in query) or ("whatsapp" in query):
            jarvis.speak("Sure sir, opening whatapp.")
            subprocess.Popen([chrome_path, "https://web.whatsapp.com/"])
            
        elif "listen to me" in query:
            jarvis.speak("Yes Sir!")

        elif ("weather" in query) or ("outside" in query):
            weather_rpt = weather_report()
            print(weather_rpt)
            jarvis.speak(weather_rpt)

        elif r'are you' in query:
            jarvis.speak("For you sir, always!")
            
        elif 'check' in query and any(x in query for x in ['connection', 'network']):
            jarvis.speak("Sure. Running internet diagnostics. This will take a moment sir.")
            st = speedtest.Speedtest(secure = True)
            dl = st.download()/1000000
            ul = st.upload()/1000000
            print(f'Upload Speed: {round(ul,1)}, Download Speed: {round(dl,1)}')
            jarvis.speak(f"Sir, download is {round(dl,1)} Megabytes per second and \
            upload is {round(ul,1)} Megabytes per second.")
        
        elif r'volume' in query:
            clean_up = ["set", "increase", "decrease", "the", "volume", "to", " "]
            for wrds in clean_up:
                if wrds in query:
                    query = query.replace(wrds, "")
            print(f"Volume set to {query}")
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", \
            query])
            jarvis.speak(f"Volume set to {query}.")
        
        # Set volume to 0 - for reminders
        elif 'mute' in query:
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", 0])
        
        elif ("where am i" in query) or ("current location" in query):
            location = get_curr_location()
            if location is not None:
                jarvis.speak(f"Your are currently located in {location}")
                
        elif 'play some music' in query:
            music_dir = "C:\\Users\\Indusface\\Desktop\\Downloads"
            songs = os.listdir(music_dir)
            print(songs)
            query2 = "no"
            while (query2 == "no"):
                jarvis.speak("Are you interested in this song sir?")
                n = random.randint(0, 15)
                # print(songs[n])
                jarvis.speak(songs[n])
                query2 = jarvis.takeCommand().lower()
                if "stop" in query2:
                    break
            if "stop" not in query2:
                os.startfile(os.path.join(music_dir, songs[n]))  # N is the max songs in the playlist

        elif "the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            jarvis.speak(f"Sir, it is {strTime} in Bengaluru, India")

        elif 'who are you' in query:
            jarvis.speak("You have a nice sense of humour sir!")

        elif "thanks" in query:
            jarvis.speak("For you, anything sir")

        elif 'create a presentation' in query:
            jarvis.speak('Sure sir. Opening Microsoft PowerPoint!')
            try:
                path = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.exe"
                os.startfile(path)

            except Exception as e:
                print(e)
                jarvis.speak("Sorry sir, I may be malfunctioning")

        elif "send an email" in query:
            jarvis.speak("To whom sir?")
            name = jarvis.takeCommand().lower()
            try:
                jarvis.speak("What should I write sir?")
                content = jarvis.takeCommand()
                to = jarvis.emails[name]
                jarvis.sendEmail(to, content)
                jarvis.speak("Email has been sent!")

            except Exception as e:
                print(e)
                jarvis.speak("Sorry sir, I think I'm malfunctioning!")

        elif "sing happy" in query:
            jarvis.speak("I'm H A P P Y!    I'm H A P P Y!    I know I  am I'm sure I  am I'm H A P P Y!")

        elif 'look up' in query:
            jarvis.speak('Let me think sir...')
            query = query.replace("look up ", "")
            results = chatgpt_api.get_chatgpt_response(query)
            print(results)
            jarvis.speak(results)

        elif ("shutdown" in query) or ("sleep" in query) or ("quit" in query):
            jarvis.speak("Alright Sir, I think I'll sleep now!")     # TODO add Iron Man anecdotes
            jarvis.speak("")
            break

        elif all(x in query for x in ['locally', 'search']) or any(x in query for x in ['open', 'folder']):
            try:
                query = query.replace('locally', '')
                query = query.replace('search', '')
                query = query.replace('open', '')
                query = query.replace('folder', '')
            except Exception as e:
                pass
            query = query.strip()
            print(query)
            home_dir = r'C:\Users\sharm\Desktop'
            search_and_open(query, home_dir)
            pass

        else:
            pass

def open_with_default_app(path):
    import sys
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.call(('open', path))
    elif os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # Linux
        subprocess.call(('xdg-open', path))
    else:
        print("Unsupported OS")

def search_and_open(target_name, search_dir):
    found = None
    for root, dirs, files in os.walk(search_dir):
        # Search for matching folders
        for d in dirs:
            if target_name.lower() in d.lower():
                found = os.path.join(root, d)
                break
        # Search for matching files
        for f in files:
            if target_name.lower() in f.lower():
                found = os.path.join(root, f)
                break
        if found:
            break

    if found:
        print(f"Found: {found}")
        open_with_default_app(found)
    else:
        print("File or folder not found.")


if __name__ == "__main__":
    """
    Main entry point for Jarvis voice assistant.
    Initializes hardware and starts the main execution loop.
    """
    # Initialization for pigpio library
    print('Initializing...')
    jarvis = VoiceEngine()
    run_jarvis(jarvis)