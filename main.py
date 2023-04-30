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
        self.image = tk.PhotoImage(file='/home/maysu/Documentos/github/Simple-Timer/assets/icon.png')
        self.root.iconphoto(False, self.image)

        self.upView = tk.Canvas(self.root, width=600, height=60, bg=BACK_COLOR, bd=0, highlightthickness=0, relief='raised')
        self.upView.pack(pady=10)
        
        self.startButton = tk.Button(self.upView, text='START', bd=0, relief='raised', bg=BACK_COLOR, fg=FONT_COLOR, activeforeground="black", activebackground=BACK_COLOR, font=FONT_TYPE, pady=10, command=self.startThread, )
        self.startButton.pack(in_=self.upView, side=LEFT, padx=10)

        self.entryButton = tk.Entry(self.upView, bd=0, relief='raised', background=BACK_COLOR, font="Montserrat 24", width=8, justify=CENTER)
        self.entryButton.pack(in_=self.upView, side=LEFT, padx=10)

        self.stopButton = tk.Button(self.upView, text='RESET', bd=0, relief='raised', bg=BACK_COLOR, fg=FONT_COLOR, activeforeground="black", activebackground=BACK_COLOR, font=FONT_TYPE, pady=10, command=self.stop)
        self.stopButton.pack(in_=self.upView, side=LEFT, padx=10)

        self.userSalutation = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 16))
        self.userSalutation.pack()

        self.userDate = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 16))
        self.userDate.pack(pady=2)

        self.timeLabel = Label(self.root, bg=BACK_COLOR ,fg=FONT_COLOR, font=(FONT_TYPE, 64), text="00:00:00")
        self.timeLabel.pack(pady=2)

        self.stop_loop = False

        self.getSalution()
        self.getDate()
        self.root.mainloop()

    def getSalution(self):
        userName = os.getlogin()
        self.userSalutation.config(text='Hello ' + userName)

    def getDate(self):
        currentDate = strftime(' %a, %d %b %Y')
        self.userDate.config(text=currentDate)

    def startThread(self):
        t = threading.Thread(target=self.start)
        t.start()



    def start(self):
        self.stop_loop = False
        hours,minutes,seconds=0,0,0
        string_split = self.entryButton.get().split(":")
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
            self.timeLabel.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.update()
            sleep(1)

        if not self.stop_loop:
            player = vlc.MediaPlayer('/home/maysu/Documentos/github/Simple-Timer/assets/excelent.mp3')
            player.play()
            sleep(5000)
            player.stop()

    def stop(self):
        self.stop_loop = True
        self.timeLabel.config(text='00:00:00')


if __name__ == '__main__':
    Timer()
