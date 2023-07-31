import threading
import tkinter
from tkinter import simpledialog
#import TcpChatServer # allows us to run the commands and run the file from these py files 
#import TcpChatClient

def stop():
    exit(0)

def initialiseUI():
    wndw = tkinter.Tk()
    wndw.config(bg="lightgray")
    wndw.resizable(False, False)
    wndw.geometry("300x300")

    TitleLabel = tkinter.Label(wndw, text="TimTam's TCP Chat Launcher", bg="lightgray")
    TitleLabel.pack(side="top")

    InfoLabel = tkinter.Label(wndw, text="This is the launcher for my TCP chat program", bg="lightgray")
    InfoLabel.pack(side="top")

    StartServerButton = tkinter.Button(wndw, text="Start Server")
    StartServerButton.pack(side="left")

    StartClientButton = tkinter.Button(wndw, text="Join a server as a client")
    StartClientButton.pack(side="right")

    wndw.protocol = ("WM_DELETE_PROTOCOL", stop)
    wndw.mainloop() # calls the ui loop

def startServer():
    pass

def startClient():
    pass


initialiseUI()
