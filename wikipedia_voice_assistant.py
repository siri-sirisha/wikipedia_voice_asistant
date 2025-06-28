import datetime,wikipedia,webbrowser,os,random,requests,pyautogui,playsound,subprocess,time
import urllib.request,bs4 as bs,sys,threading
import Annex,wolframalpha
from ttkthemes import themed_tk
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk,Image
import sqlite3,pyjokes,pywhatkit
from functools import partial
import getpass,calendar
import speech_recognition as SR
try:
    app=wolframalpha.Client("JPK4EE-L7KR3XWP9A")  #API key for wolframalpha
except Exception as e:
    pass

#setting chrome path

chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe %s"

def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True

def CommandsList():
    '''show the command to which voice assistant is registered with'''
    os.startfile('Commands List.txt')

def clearScreen():
    ''' clear the scrollable text box'''
    SR.scrollable_text_clearing()


def greet():
    conn = sqlite3.connect('Heisenberg.db')
    mycursor=conn.cursor()
    hour=int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        mycursor.execute('select sentences from goodmorning')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=12 and hour<18:
        mycursor.execute('select sentences from goodafternoon')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=18 and hour<21:
        mycursor.execute('select sentences from goodevening')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    else:
        mycursor.execute('select sentences from night')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    conn.commit()
    conn.close()
    SR.speak("\nMyself SIRI. How may I help you?")


def mainframe():
    """Logic for execution task based on query"""
    SR.scrollable_text_clearing()
    greet()
    query_for_future = None
    try:
        while True:
            query = SR.takeCommand().lower()  # convert to lowercase

            # wikipedia search
            if 'wikipedia' in query:
                SR.speak("Searching Wikipedia...")
                try:
                    wikipedia.set_lang("en")  # Set language to English
                    query = query.replace("search wikipedia for", "")
                    query = query.replace("from wikipedia", "")
                    query = query.replace("wikipedia", "")
                    query = query.strip()
                    results = wikipedia.summary(query, sentences=2)
                    SR.speak("According to Wikipedia:")
                    SR.speak(results)
                except Exception as e:
                    print(f"Wikipedia Error: {e}")
                    SR.speak("Sorry, I couldn't find anything on Wikipedia.")

            # youtube-related commands.
            elif there_exists(['open youtube and play','on youtube'], query):
                SR.speak("Opening YouTube")
                pywhatkit.playonyt(query.replace('on youtube', '').replace('open youtube and play ', ''))
                break

            elif there_exists(['play some songs on youtube','i would like to listen some music','i would like to listen some songs','play songs on youtube'], query):
                SR.speak("Opening YouTube")
                pywhatkit.playonyt('play random songs')
                break

            elif there_exists(['open youtube','access youtube'], query):
                SR.speak("Opening YouTube")
                webbrowser.get(chrome_path).open("https://www.youtube.com")
                break

            elif there_exists(['open google and search','google and search'], query):
                url = 'https://google.com/search?q=' + query[query.find('for') + 4:]
                webbrowser.get(chrome_path).open(url)
                break

            # music
            elif there_exists(['play music','play some music for me','like to listen some music'], query):
                SR.speak("Playing music")
                music_dir = 'D:\\Musics\\vishal'
                songs = os.listdir(music_dir)
                indx = random.randint(0, min(50, len(songs) - 1))
                os.startfile(os.path.join(music_dir, songs[indx]))
                break

            elif there_exists(['open vlc','vlc media player','vlc player'], query):
                SR.speak("Opening VLC media player")
                os.startfile(r"C:\Program Files\VideoLAN\VLC\vlc.exe")
                break

            # voice recorder
            elif there_exists(['record my voice','start voice recorder','voice recorder'], query):
                VR = Annex.VoiceRecorer()
                VR.Record(scrollable_text)
                del VR

            # exit
            elif there_exists(['exit','quit','shutdown','shut up','goodbye','shut down'], query):
                SR.speak("shutting down")
                sys.exit()

            elif there_exists(['none'], query):
                pass

            elif there_exists(['stop the flow','stop the execution','halt','halt the process','stop the process','stop listening','stop the listening'], query):
                SR.speak("Listening halted.")
                break

            # wolframalpha queries
            elif there_exists(['search something for me','to do a little search','search mode','i want to search something'], query):
                SR.speak('What you want me to search for?')
                query = SR.takeCommand()
                SR.speak(f"Showing results for {query}")
                try:
                    res = app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, there was a problem fetching the result.")

            elif there_exists(['what is the capital of','capital of','capital city of'], query):
                try:
                    res = app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, there was a problem fetching the result.")

            elif there_exists(['temperature'], query):
                try:
                    res = app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")

            elif there_exists(['+','-','*','x','/','plus','add','minus','subtract','divide','multiply','divided','multiplied'], query):
                try:
                    res = app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")

            else:
                SR.speak("Sorry, it did not match any registered commands. Please say it again.")
    except Exception as e:
        pass


def gen(n):
    for i in range(n):
        yield i

class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        mainframe()

def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()

if __name__=="__main__":
        #tkinter code
        root=themed_tk.ThemedTk()
        root.set_theme("winnative")
        root.geometry("{}x{}+{}+{}".format(745,360,int(root.winfo_screenwidth()/2 - 745/2),int(root.winfo_screenheight()/2 - 360/2)))
        root.resizable(0,0)
        root.title("WIKIPEDIA")
        root.iconbitmap('Music_29918.ico')
        root.configure(bg='red')
        scrollable_text=scrolledtext.ScrolledText(root,state='disabled',height=15,width=87,relief='sunken',bd=5,wrap=tk.WORD,bg='white',fg='#800000')
        scrollable_text.place(x=10,y=10)
        mic_img=Image.open("music.png")
        mic_img=mic_img.resize((55,55))
        mic_img=ImageTk.PhotoImage(mic_img)
        Speak_label=tk.Label(root,text="WHAT WOULD YOU LIKE",fg="#FFD700",font='"Times New Roman" 12 ',borderwidth=0,bg='#2c4557')
        Speak_label.place(x=250,y=300)
        """Setting up objects"""
        SR=Annex.SpeakRecog(scrollable_text)    #Speak and Recognition class instance
        Listen_Button=tk.Button(root,image=mic_img,borderwidth=0,activebackground='white',bg='#2c4557',command=Launching_thread)
        Listen_Button.place(x=330,y=280)
        myMenu=tk.Menu(root)
        m1=tk.Menu(myMenu,tearoff=0) #tearoff=0 means the submenu can't be teared of from the window
        m1.add_command(label='Commands List',command=CommandsList)
        myMenu.add_cascade(label="Help",menu=m1)
        stng_win=Annex.SettingWindow()
        myMenu.add_cascade(label="Settings",command=partial(stng_win.settingWindow,root))
        myMenu.add_cascade(label="Clear Screen",command=clearScreen)
        root.config(menu=myMenu)
        root.mainloop()