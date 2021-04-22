import os
import sys
import time

import pyautogui
import pyjokes
import pyttsx3
import datetime

import pywhatkit
import speech_recognition as sr
import wikipedia

import close_module
import gratitude_module
import location_module
import math_module
import news_module
import open_module

engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-20)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    hour = int(datetime.datetime.now().hour)
    startTime = time.strftime("%I:%M %p")
    if hour >= 0 and hour < 12:
        speak(f'Good Morning Sir, It\'s {startTime}')
    elif hour >= 12 and hour < 16:
        speak(f'Good Afternoon Sir, It\'s {startTime}')
    else:
        speak(f'Good Evening Sir, It\'s {startTime}')

    speak("All systems online.")

def takeCommand():
    '''
    It takes microphone input from user
    :return: String output
    '''
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        listener.pause_threshold = 1
        audio = listener.listen(source, timeout=4, phrase_time_limit=7)
        try:
            print('Recognizing...')
            command = listener.recognize_google(audio) # , language='en-in'
        except Exception as e:
            return 'none'
        command = command.lower()
        return command

def search_google(query):
    speak(f'Searching for {query}')
    pywhatkit.search(query)

def search_wiki(query):
    result = wikipedia.summary(query, sentences=1)
    speak(result)

def run_jarvis():
    greetMe()
    while True:
        command = takeCommand().lower()
        if 'hey' in command:
            command = command.replace('hey', '')
        if 'hi' in command:
            command = command.replace('hi', '')
        if 'jarvis' in command:
            command = command.replace('jarvis', '')
        print(f'User: {command}')

        # Logic for executing tasks based on commands

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f'It\'s {time}')
            hour = int(datetime.datetime.now().hour)
            if hour >= 0 and hour < 4:
                speak('you should go to sleep now sir. It\'s pretty late')

        elif 'date' in command:
            today = datetime.date.today()
            speak(f'It\'s {today}')

        elif 'current location' in command or 'where are we' in command or 'where am i' in command \
                or 'location' in command or 'locate us' in command:
            location_module.get_current_location()

        elif 'news' in command or 'headlines' in command:
            speak('Fetching the latest news')
            if 'headlines' in command:
                news_module.get_news()
            else:
                news_module.get_news()
                speak('Do you wish to know more about a certain headline?')
                response = takeCommand().lower()
                if 'yes' in response or 'yup' in response or 'yeah' in response:
                    speak('Which one?')
                    response = takeCommand().lower()
                    news_module.get_specific_news(response)
                elif 'no' in command or 'nope' in command or 'nah' in command:
                    speak('Ok sir.')

        elif 'day' in command:
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day = datetime.datetime.today(). weekday()
            speak(f'It\'s {day_name[day]}')

        elif 'who is' in command:
            speak('Asking Wiki..')
            query = command.replace('who is', '')
            search_wiki(query)

        elif 'what is' in command:
            speak('Asking Wiki..')
            query = command.replace('what is', '')
            search_wiki(query)

        elif 'tell me about' in command:
            speak('Asking Wiki..')
            query = command.replace('tell me about', '')
            search_wiki(query)

        elif 'search google' in command:
            try:
                speak('What should I search for?')
                query = takeCommand()
                search_google(query)
            except:
                speak('Could you please repeat')
                query = takeCommand()
                search_google(query)

        elif 'run a search on' in command:
            try:
                query = command.replace('run a search on', '')
                search_google(query)
            except:
                speak('What should I search for?')
                query = takeCommand()
                search_google(query)

        elif 'open' in command or 'i want to work on' in command or 'i want to build' in command:
            open_module.open_module(command)

        elif 'close' in command or 'i am done with' in command:
            close_module.close_module(command)

        elif 'play' in command:
            song = command.replace('play', '')
            speak('Playing' + song)
            pywhatkit.playonyt(song)

        elif 'screenshot' in command or 'screen shot' in command or 'capture the screen' in command:
            time = datetime.datetime.now().time().strftime('%H_%M_%S')
            print(time)
            imgName = 'Screenshot_'+time+'.jpg'
            picturesDir = 'C:\\Users\\Siddharth Sircar\\Pictures\\Screenshots\\'
            speak('Please stay on the screen for a while longer.')
            img = pyautogui.screenshot()
            speak('Saving Image')
            img.save(f'{picturesDir}{imgName}')
            speak('You can find the screenshot in the Pictures folder')

        elif 'do some calculations' in command:
            speak('what do you wish to calculate?')
            command = takeCommand().lower()
            math_module.perform_calculations(command)

        elif 'calculate' in command:
            command = command.replace('calculate', '')
            math_module.perform_calculations(command)

        elif 'who are you' in command:
            speak('I am Batman')

        elif 'how are you' in command:
            speak('I have been good. Thank you for asking.')
            speak('How have you been lately?')

        elif 'i am good' in command or 'i am also good' in command or\
            'i am great' in command or 'i am amazing' in command:
            speak('That\'s great to hear')

        elif 'not good' in command or 'not that good' in command or\
            'not great' in command:
            speak('Sorry to hear that sir')
            speak('Anything I can do to help?')

        elif 'tell me a joke' in command:
            speak(pyjokes.get_joke())

        elif 'you are funny' in command or 'you\'re funny' in command or\
                'you are really funny' in command or 'you\re really funny' in command or\
            'you really funny' in command:
            speak('I try sir.' or 'People call me Mr. Hilarious')

        elif 'thank you' in command or 'thankyou' in command:
            speak('Always at your service sir!')

        elif 'you can sleep' in command or 'you may go to sleep' in command or 'go to sleep' in command:
            speak('Okay sir, Let me know when you need me.')
            break

        elif 'you can go' in command:
            speak('Good bye sir')
            sys.exit()

        elif 'goodnight' in command or 'good night' in command or 'good bye' in command or \
                'goodbye' in command or 'bye' in command or 'thank you' in command or 'thankyou' in command:
            speak('Okay sir, Let me know when you need me.')
            break

        elif 'i\'m going out' in command or 'i am going out' in command or 'see you' in command or \
                ('sleep' in command and 'system' in command):
            speak('Sir, are you leaving?')
            response = takeCommand().lower()
            if 'yes' in response or 'yup' in response or 'yeah' in response:
                speak('Good Bye sir. Putting all systems to sleep')
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

        elif 'shutdown' in command or 'shut down' in command or ('shut' and 'down' in command):
            speak('All systems going offline.')
            speak('Good Bye sir.')
            os.system('shutdown /s /t 5')

        elif 'restart' in command or 'reboot' in command:
            speak('Resetting all systems')
            speak('See you soon sir.')
            os.system('shutdown /r /t 5')

        elif 'none' in command or command is None:
            pass

        else:
            speak('I did not quite get you.')


if __name__ == "__main__":
    # greetMe()
    # while True:
    #     run_jarvis()
    while True:
        permission = takeCommand()
        if 'wake up' in permission or 'wakeup' in permission:
            speak('Please let me sleep sir, I\'m tired')
            response = takeCommand().lower()
            if 'ok' in response or 'sleep' in response:
                speak('Thank you. I\'ll be up in a few moments')
                time.sleep(15)
            elif 'no' in response or 'wake up' in response or 'wakeup' in response:
                speak('Okay. I\'m up.')
                run_jarvis()

        elif 'you can go' in permission:
            speak('Good bye sir')
            sys.exit()

        elif 'goodnight' in permission or 'good night' in permission or 'good bye' in permission or \
                'goodbye' in permission or 'bye' in permission or 'thank you' in permission or \
                'thankyou' in permission:
            gratitude_module.gratitude_module(permission)