import tkinter as tk
from tkinter import *
import os
from time import strftime, sleep
import threading
import vlc

BACK_COLOR = '#332d38'
FONT_COLOR = '#8253ad'
FONT_TYPE = 'Montserrat'

class Timer:
    def __init__(self):
    #Raiz do projeto
        self.root = tk.Tk()
        self.root.title('Simple Custom Timer')
        self.root.geometry('500x240')
        self.root.maxsize(500,240)
        self.root.minsize(500, 240)
        self.root.configure(background=BACK_COLOR)
        self.path_icon = os.path.abspath(__file__).removesuffix('main.py') + 'assets/icon.png'
        self.path_mp3 = os.path.abspath(__file__).removesuffix('main.py') + 'assets/alarm.mp3'
        self.image = tk.PhotoImage(file=self.path_icon);
        self.root.iconphoto(False, self.image)

        self.top_view = tk.Canvas(self.root, width=600, height=60, bg=BACK_COLOR, bd=0, highlightthickness=0, relief='raised')
        self.top_view.pack(pady=10)
        
        self.start_button = tk.Button(self.top_view, text='START', bd=0, relief='raised', bg=BACK_COLOR, fg=FONT_COLOR, activeforeground="black", activebackground=BACK_COLOR, font=FONT_TYPE, pady=10, command=self.startThread)
        self.start_button.pack(in_=self.top_view, side=LEFT, padx=10)

        self.entry_button = tk.Entry(self.top_view, bd=0, relief='raised', background=BACK_COLOR, font="Montserrat 24", width=8, justify=CENTER)
        self.entry_button.pack(in_=self.top_view, side=LEFT, padx=10)

        self.stop_button = tk.Button(self.top_view, text='RESET', bd=0, relief='raised', bg=BACK_COLOR, fg=FONT_COLOR, activeforeground="black", activebackground=BACK_COLOR, font=FONT_TYPE, pady=10, command=self.stop)
        self.stop_button.pack(in_=self.top_view, side=LEFT, padx=10)

        self.user_salutation = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 16))
        self.user_salutation.pack()

        self.user_date = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 16))
        self.user_date.pack(pady=2)

        self.time_label = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 64), text="00:00:00")
        self.time_label.pack(pady=2)

        self.stop_loop = False

        self.getSalution()
        self.getDate()
        self.root.mainloop()

    def getSalution(self):
        userName = os.getlogin()
        self.user_salutation.config(text='Hello ' + userName)

    def getDate(self):
        currentDate = strftime(' %a, %d %b %Y')
        self.user_date.config(text=currentDate)

    def startThread(self):
        t = threading.Thread(target=self.start)
        t.start()

    def start(self):
        self.stop_loop = False
        hours,minutes,seconds=0,0,0
        string_split = self.entry_button.get().split(":")
        if len(string_split) == 3:
            hours = int(string_split[0])
            minutes = int(string_split[1])
            seconds = int(string_split[2])

        elif len(string_split) == 2:
            minutes = int(string_split[0])
            seconds = int(string_split[1])

        elif len(string_split) == 1:
            seconds = int(string_split[0])

        full_seconds = (hours*3600) + (minutes * 60) + seconds

        while full_seconds > 0 and not self.stop_loop:
            full_seconds -= 1
            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.update()
            sleep(1)

        if not self.stop_loop:
            player = vlc.MediaPlayer(self.path_mp3)
            player.play()
            sleep(5000)
            player.stop()

    def stop(self):
        self.stop_loop = True
        self.time_label.config(text='00:00:00')

if __name__ == '__main__':
    t = Timer()
    exit(0)
