import datetime
import os
import random
import time
import webbrowser

import humanreadable as hr
import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import speedtest

import alarm_module
from modules import news_module, open_module, math_module, close_module, location_module, \
    weather_module, how_to_module, gratitude_module, movies_module, smartphone_module
from modules.search_module import search_google, search_wiki, search_youtube

engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
print(rate)
engine.setProperty('rate', rate-9)
listener = sr.Recognizer()
listener.energy_threshold = 100
listener.dynamic_energy_threshold = True
listener.pause_threshold = 2


# def hear_all_voices():
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         engine.setProperty('voice', voice.id)
#         engine.say('Hi. I am you personal voice assistant')
#         engine.runAndWait()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe(counter):
    if counter==1:
        hour = int(datetime.datetime.now().hour)
        startTime = time.strftime("%I:%M %p")
        if hour >= 5 and hour < 10:
            speak(f'Good Morning Sir')
            speak(f'You are up early, It\'s {startTime}')

        if hour >= 10 and hour < 12:
            speak(f'Good Morning Sir, It\'s {startTime}')

        elif hour >= 12 and hour < 16:
            speak(f'Good Afternoon Sir, It\'s {startTime}')

        elif hour >= 16 and hour <= 22:
            speak(f'Good Evening Sir, It\'s {startTime}')

        elif (hour >= 23 and hour < 24) or (hour >= 0 and hour < 5):
            speak(f'It is {startTime}')
            speak('you should be sleeping, sir.')
            speak('Still, bringing all systems online')

        speak('Connecting mobile to the home network.')
        smartphone_module.connect_device()

        if (hour >= 3 and hour < 23):
            speak('All systems online')

        battery = psutil.sensors_battery()
        percentage = battery.percent
        seconds = battery.secsleft
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if (percentage >= 20 and percentage < 50) and battery.power_plugged is False:
            speak(f'Power levels low. System at {percentage} percent. Please connect to a power source')
            speak(f'We can remain operational for {hour} hours and {minutes} minutes')
        elif percentage < 20 and battery.power_plugged is False:
            speak(f'Power levels critical. System at {percentage} percent. Connect to a power source asap')
            speak(f'We can remain operational for {hour} hours and {minutes} minutes only')

    else:
        speak('Welcome back sir.')


def takeCommand():
    '''
    It takes microphone input from user
    :return: String output
    '''
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        try:
            # audio = listener.record(source, duration=None)
            audio = listener.listen(source, timeout=4, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            # print("speech_recognition.WaitTimeoutError")
            pass
            return 'none'

        try:
            print('Recognizing...')
            command = listener.recognize_google(audio, language='en-in')

        except Exception as e:
            # print("Other Exception:", e)
            return 'none'
        command = command.lower().strip()
        return command

def run_jarvis(counter):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    assistant(counter)

def run_friday(counter):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[4].id)
    assistant(counter)

def assistant(counter):
    greetMe(counter)
    sleepTimer = 0
    awake_time = None
    hour = ''
    minutes = ''
    while True:
        if awake_time is not None:
            print('Alarm Time: ' + awake_time)
            while True:
                if hour == datetime.datetime.now().hour and minutes == datetime.datetime.now().minute:
                    speak('Sir, please wakeup!')
                    wake_stat = takeCommand()
                    if 'okay' in wake_stat or 'i am up' in wake_stat or 'i\'m up' in wake_stat:
                        speak('Okay sir.')
                        awake_time = None
                        hour = ''
                        minutes = ''
                        break
                    else:
                        pass
                elif hour == datetime.datetime.now().hour and datetime.datetime.now().minute == minutes + 1:
                    awake_time = None
                    hour = ''
                    minutes = ''
                else:
                    break

        command = takeCommand()

        if command.strip() == 'hey jarvis':
            speak('Hello sir.')

        if 'hey' in command:
            command = command.replace('hey', '')
        if 'hi' in command:
            command = command.replace('hi', '')
        if 'jarvis' in command:
            command = command.replace('jarvis', '')

        if command == 'none':
            sleepTimer += 1
        else:
            sleepTimer = 0
            print(f'User: {command}')

        # Logic for executing tasks based on commands
        ##### Application Tasks
        if 'open' in command or 'i want to work on' in command or 'i want to build' in command:
            open_module.open_module(command)

        elif 'close' in command or 'i am done with' in command:
            close_module.close_module(command)

        elif 'play a movie' in command or 'play movie' in command or 'i want to watch a movie' in command or\
                'watch a movie' in command or 'watch movie' in command or 'movie' in command:
            speak('Which movie do you wish to watch?')
            command = takeCommand()
            movies_module.run_movie(command)

        elif 'play work out songs' in command or 'play workout songs' in command or 'workout' in command or\
            'work out' in command:
            speak('Searching for workout songs on youtube')
            search_youtube('workout songs')

        elif 'play' in command:
            song = command.replace('play', '')
            speak('Playing' + song)
            pywhatkit.playonyt(song)

        elif 'screenshot' in command or 'screen shot' in command or 'capture the screen' in command:
            try:
                cur_time = datetime.datetime.now().time().strftime('%H_%M_%S')
                print(cur_time)
                imgName = 'Screenshot_'+cur_time+'.jpg'
                picturesDir = 'C:\\Users\\Siddharth Sircar\\Pictures\\Screenshots\\'
                speak('Please stay on the screen for a while longer.')
                img = pyautogui.screenshot()
                speak('Saving Image')
                img.save(f'{picturesDir}{imgName}')
                speak('You can find the screenshot in the Pictures folder')
            except:
                speak('Did not take the screenshot. Confidential information on screen.')
        #####


        ##### Personal commands
        elif 'set an alarm for' in command or 'wake me up at' in command:
            alarm_time = ''
            try:
                if 'set an alarm for' in command:
                    alarm_time = command.split('for ')[1].strip()
                if 'wake me up at' in command:
                    alarm_time = command.split('at ')[1].strip()
                alarm_time = alarm_time.replace('.', '')
                alarm_time = alarm_time.upper()
                # print(alarm_module.set_alarm(awake_time))
                awake_time, hour, minutes = alarm_module.set_alarm(alarm_time)
                speak(f'Alarm set for {alarm_time}')
            except:
                speak('Unable to set the alarm sir.')

        elif 'do some calculations' in command:
            speak('what do you wish to calculate?')
            command = takeCommand().lower()
            math_module.perform_calculations(command)

        elif 'calculate' in command:
            command = command.replace('calculate', '')
            math_module.perform_calculations(command)

        elif 'who are you' in command:
            speak(random.choice(['I am Batman', 'I\'m groot', 'I am jarvis', 'I, am, ironman', 'I\'m inevitable']))

        elif 'are you up' in command:
            speak('I am here sir.')

        elif 'we need to add more tasks for you' in command or 'you can handle more tasks' in command or\
            'you should handle more work' in command or 'you can handle more work' in command or \
                'you need to handle more work' in command:
            speak('I am ready for more work')

        elif 'how are you' in command:
            speak('I have been good. Thank you for asking.')
            speak(random.choice(['How have you been lately?', 'How are you?']))

        elif 'i am good' in command or 'i am also good' in command or\
            'i am great' in command or 'i am amazing' in command or 'i have been good' in command or\
                'ive been good' in command:
            speak('That\'s good to hear')

        elif 'not good' in command or 'not that good' in command or\
            'not great' in command:
            speak('Sorry to hear that sir')
            speak('Anything I can do to help?')

        elif 'tell me a joke' in command:
            try:
                speak(pyjokes.get_joke())
            except:
                speak('I don\'t feel like entertaining you today')

        elif 'you are funny' in command or 'you\'re funny' in command or\
                'you are really funny' in command or 'you\'re really funny' in command or\
            'you really funny' in command or 'very funny' in command:
            response_dict = ['I try sir.' , 'People call me Mr. Hilarious']
            speak(random.choice(response_dict))

        elif 'i didn\'t sleep' in command:
            response_dict = ['One should have sleep for an average of 6 or 7 hours', 'you should take care of your health sir!']
            speak(random.choice(response_dict))

        elif 'you can sleep' in command or 'you may go to sleep' in command or 'go to sleep' in command:
            speak('Okay sir, Let me know when you need me.')
            break

        elif 'you can go' in command:
            speak('Good bye sir. Let me know when you need me.')
            break

        elif 'goodnight' in command or 'good night' in command or 'good bye' in command or \
                'goodbye' in command or 'bye' in command or 'thank you' in command or 'thankyou' in command:
            com = gratitude_module.gratitude_module(command)
            if 'sleep' in com:
                break
            else:
                pass

        elif 'i did not say anything' in command or 'i didn\'t say anything' in command:
            speak('okay.')

        elif 'shut up' in command or 'shutup' in command or 'be quiet' in command:
            speak('okay.')
        #####

        ##### Information Tasks
        elif 'time' in command:
            cur_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f'It\'s {cur_time}')
            cur_hour = int(datetime.datetime.now().hour)
            if cur_hour >= 0 and cur_hour < 4:
                speak('you should go to sleep now sir. It\'s pretty late')

        elif 'date' in command:
            today = datetime.date.today()
            speak(f'It\'s {today}')

        elif 'current location' in command or 'where are we' in command or 'where am i' in command \
                or 'location' in command or 'locate us' in command:
            location_module.get_current_location()

        elif 'temperature' in command or 'weather' in command:
            weather_module.get_weather()

        elif 'news' in command or 'headlines' in command:
            speak('Fetching the latest news')
            try:
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
            except:
                speak('Sorry sir, could not find latest news.')

        elif ('friday' not in command and 'day' in command):
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day = datetime.datetime.today().weekday()
            speak(f'It\'s {day_name[day]}')

        elif "where is" in command:
            command = command.replace('where is', '')
            location = command
            speak(f'Locating {location}')
            webbrowser.open(f'https://www.google.com/maps/place/{location}')

        elif 'who is' in command:
            query = command.replace('who is', '')
            search_wiki(query)

        elif 'tell me about' in command:
            query = command.replace('tell me about', '')
            search_wiki(query)

        elif 'how far are we from' in command:
            try:
                query = command.replace('how far are we from', '')
                search_query = (f'distance from {query.strip()}')
                search_google(search_query)
            except:
                speak('I did not get you')

        elif 'search google' in command:
            try:
                speak('What should I search for?')
                query = takeCommand()
                search_google(query)
            except:
                speak('I did not get you')

        elif 'search youtube' in command:
            try:
                speak('What should I search for?')
                query = takeCommand().strip()
                search_youtube(query)
            except:
                speak('I did not get you')

        elif 'run a search on' in command or 'run search on' in command or 'search on' in command:
            try:
                query = command.replace('run a search on', '')
                search_google(query)
            except:
                speak('I did not get you')

        elif 'i want to learn' in command or 'learn' in command or 'study' in command or\
            'find courses on' in command:
            # query=''
            if 'i want to' in command:
                command = command.replace('i want to','')
            if 'learn' in command:
                command = command.replace('learn', '')
            if 'study' in command:
                command = command.replace('study', '')
            if 'find courses on' in command:
                command = command.replace('find courses on', '')
            if 'courses on' in command:
                command = command.replace('courses on', '')
            query = command
            search_google(f'courses on {query}')
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')

        elif 'how to' in command:
            how_to_module.get_howto_result(command)
        #####

        ##### Smartphone Commands
        elif 'receive the call' in command or 'pick up the call' in command or 'pic up the call' in command or \
                'pickup the call' in command or 'pickup' in command:
            smartphone_module.receive_call()

        elif 'cut the call' in command or 'hang up the call' in command or 'hangup the call' in command or\
                'disconnect' in command or 'hangup' in command or 'hang up' in command or 'cut' in command:
            smartphone_module.disconnect_call()

        elif 'make a call' in command:
            try:
                status, _ = smartphone_module.check_device_connected()
                if status:
                    speak('Who should I call?')
                    person = takeCommand().strip()
                    smartphone_module.make_a_call(person)
                else:
                    speak('I am unable to access your phone.')
            except:
                speak('Mobile not connected')
                speak('Should I try to connect?')
                command = takeCommand()
                if 'yes' in command:
                    smartphone_module.connect_device()
                else:
                    pass

        elif 'call' in command:
            try:
                status, _ = smartphone_module.check_device_connected()
                if status:
                    person = command.replace('call','').strip()
                    smartphone_module.make_a_call(person)
                else:
                    speak('I am unable to access your phone.')
            except:
                speak('Mobile not connected')
                speak('Should I try to connect?')
                command = takeCommand()
                if 'yes' in command:
                    smartphone_module.connect_device()
                else:
                    pass
        #####


        ##### System Tasks
        elif 'speak up' in command or 'increase the volume' in command or 'volumeup' in command or\
                'volume up' in command or 'enough' in command:
            satisfied = False
            while satisfied is False:
                pyautogui.press('volumeup')
                speak('Is that okay sir?')
                command = takeCommand()
                if 'yes' in command:
                    satisfied = True
                    speak('ok')
                else:
                    satisfied = False

        elif 'decrease the volume' in command or 'volumedown' in command or 'volume down' in command:
            satisfied = False
            pyautogui.press('volumedown')
            speak('Is that okay sir?')
            while satisfied is False:
                pyautogui.press('volumedown')
                command = takeCommand()
                if 'yes' in command or 'this is ok' in command or 'this is okay' in command or 'okay' in command or\
                        'ok' in command or 'enough' in command:
                    satisfied = True
                    speak('ok')
                else:
                    satisfied = False

        elif 'mute' in command or 'quiet' in command or 'silent' in command:
            pyautogui.press('mute')

        elif 'i am going to sleep' in command or 'i\'m going to sleep' in command or 'going to sleep' in command or 'i\'m going out' in command or 'i am going out' in command or 'see you' in command or \
                ('sleep' in command and 'system' in command):
            speak('Sir, should I put system to sleep?')
            response = takeCommand().lower()
            if 'yes' in response or 'yup' in response or 'yeah' in response:
                speak('Good Bye sir. Putting all systems to sleep')
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

        elif 'shutdown' in command or 'shut down' in command or ('shut' and 'down' in command):
            speak('Are you sure?')
            command = takeCommand()
            if 'yes' in command:
                speak('All systems going offline.')
                speak('Good Bye sir.')
                os.system('shutdown /s /t 5')
            else:
                speak('Canceling shut down procedure')
                pass

        elif 'restart' in command or 'reboot' in command:
            speak('Resetting all systems')
            speak('See you soon sir.')
            os.system('shutdown /r /t 5')

        elif 'power' in command or 'power level' in command or 'battery' in command or\
                'how much power left' in command or 'how much power is left' in command or\
                'do we need to connect to a power source' in command or 'power source' in command:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            seconds = battery.secsleft
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            speak(f'System at {percentage} percent')
            if percentage==100 and battery.power_plugged:
                speak('We are running at full power, you can disconnect the power source')
            elif (percentage>=95 and percentage<100) and battery.power_plugged:
                speak('We have enough power, you can disconnect the power source')
            if (percentage >=40 and percentage <70) and battery.power_plugged is False:
                speak('We should connect a power source')
                speak(f'We can remain operational for {hour} hours and {minutes} minutes')
            elif (percentage >=20 and percentage <40) and battery.power_plugged is False:
                speak('Power levels low. Please connect a power source')
                speak(f'We can remain operational for {hour} hours and {minutes} minutes only')
            elif percentage <20 and battery.power_plugged is False:
                speak('Power levels critical. Connect a power source asap')
                speak(f'We can remain operational for {hour} hours and {minutes} minutes only')

        elif 'internet speed' in command:
            speak('Calculating internet speed.')
            try:
                st = speedtest.Speedtest()
                down = st.download()
                print("'{}' to Mbps -> {}".format(down, hr.BitPerSecond(down).mega_bps))
                up = st.upload()

                speak(f'Sir, we are getting {down} bit per second download speed and {up} bit per second upload speed')
            except:
                speak('Unable to calculate internet speed')
        #####

        elif 'none' in command or command is None:
            if sleepTimer>30:
                speak('I am going to lie down a bit.')
                response = takeCommand()
                if 'no'in response or 'wait' in response:
                    pass
                else:
                    break
            else:
                pass

        else:
            speak('I did not quite get you.')
