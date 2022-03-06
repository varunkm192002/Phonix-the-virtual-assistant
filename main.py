import re
import os
import random
import pprint
import datetime
import requests
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from PIL import Image
from Phoenix import PhoenixAssistant
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Phoenix.config import config
from gui import Ui_Form
from ui_splash_screen import Ui_SplashScreen
import sys
from PyQt5.QtCore import (QRectF)
from PyQt5.QtGui import (QColor, QCursor, QPainterPath, QRegion)
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

counter = 0

obj = PhoenixAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello phoenix", "phoenix", "wake up phoenix", "you there phoenix", "time to work phoenix", "hey phoenix",
             "ok phoenix", "are you there", "how are you phoenix", "how are you"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

# =======================================================================================================================================================

def speak(text):
    obj.tts(text)


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Phoenix. Online and ready.    Please tell me how may I help you")



class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()



    def run(self):
        self.TaskExecution()



    def TaskExecution(self):

        wish()

        while True:
            command = obj.mic_input()


            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                    'notepad': 'C:\\WINDOWS\\system32\\notepad.exe',
                    'pycharm': 'C:\\Program Files (x86)\\JetBrains\\PyCharm Community Edition 2021.1.3\\bin\\pycharm64.exe',
                    'code': 'C:\\Users\\User\\AppData\Local\\Programs\\Microsoft VS Code\\Code.exe'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)

            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)


            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                        "Sorry sir. I couldn't load your query from my database. Please try again")

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            elif "play music" in command or "hit some music" in command:
                music_dir = "Music"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)



            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)


            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:

                    if city:
                        res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                    else:
                        res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                except:
                    res = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                    speak(res)

            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")


            elif "switch the window" in command or "switch window" in command:
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where i am" in command or "current location" in command or "where am i" in command:
                try:
                    city, state, country = obj.my_location()
                    print(city, state, country)
                    speak(
                        f"You are currently in {city} city which is in {state} state and country {country}")
                except Exception as e:
                    speak(
                        "Sorry sir, I coundn't fetch your current location. Please try again")

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"ss\\{name}.png"
                img.save(name)
                speak("The screenshot has been succesfully captured")

            elif "show me the screenshot" in command:
                try:
                    img = Image.open('' + name)
                    img.show(img)
                    speak("Here it is sir")
                    time.sleep(2)

                except IOError:
                    speak("Sorry sir, I am unable to display the screenshot")

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden")

            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")


            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            elif 'search google for' in command:
                obj.search_anything_google(command)
            
            elif "what is" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)


            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright sir, going offline. It was nice working with you")
                sys.exit()


            elif ("wake up" in command) or ("get up" in command):
                speak("boss, I am not sleeping, I am in online, what can I do for u")



            elif ('shutdown the system' in command) or ('down the system' in command):
                speak("Boss shutting down the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /s /t 5")

            elif 'restart the system' in command:
                speak("Boss restarting the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /r /t 5")


            elif 'remember that' in command:
                speak("what should i remember sir")
                rememberMessage = obj.mic_input()
                speak("you said me to remember" + rememberMessage)
                remember = open('data.txt', 'w')
                remember.write(rememberMessage)
                remember.close()

            elif 'do you remember anything' in command:
                remember = open('data.txt', 'r')
                speak("you said me to remember that" + remember.read())

            elif 'it\'s my birthday today' in command:
                print(" Wow! Wish you a very Happy Birthday")
                speak(" Wow! Wish you a very Happy Birthday")

            elif "who made you" in command or "who created you" in command or "who discovered you" in command:
                speak("I was built by Group L1")
                print("I was built by Group L1")

            elif 'who are you' in command or 'what can you do' in command:
                speak(
                    'I am Phoenix version 1 point O your personal assistant. I am programmed to perform tasks like' 'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo, etc. I like to help humans in their endeavours and I would like to be remembered as humanity\'s greatest ally')







startExecution = MainThread()

class Main(QtWidgets.QWidget, Ui_Form):

    def startAnimation(self):
        self.movie.start()
        self.movie2.start()
        self.movie3.start()
        self.movie4.start()

    def stopAnimation(self):
        self.movie.stop()
        self.movie2.stop()
        self.movie3.stop()
        self.movie4.stop()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_minimize_5.clicked.connect(self.hideWindow)

        self.btn_close_5.clicked.connect(self.close)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.movie = QMovie("icons/powersource.gif")
        self.label_3.setMovie(self.movie)

        self.movie2 = QMovie("icons/lines1.gif")
        self.label_4.setMovie(self.movie2)

        self.movie3 = QMovie("icons/in.gif")
        self.label_2.setMovie(self.movie3)

        self.movie4 = QMovie("icons/globe.gif")
        self.label.setMovie(self.movie4)


        self.startAnimation()

        self.pushButton.clicked.connect(self.startTask)

    def startTask(self):
        timer = QTimer(self)
        timer.start(1000)
        startExecution.start()





    def __del__(self):
        sys.stdout = sys.__stdout__





    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # Change window position
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        reg = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(reg)

    def hideWindow(self):
        self.showMinimized()


class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):

        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = Main()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    Phoenix = Main()
    Phoenix.show()
    sys.exit(app.exec_())
    window = SplashScreen()
    sys.exit(app.exec_())


