import threading
import socket
import tkinter
import os
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import messagebox


HOST = "127.0.0.1"
PORT = 49152 


class Client: # establishes a class or object, an sort of blueprint so that we can create instances of this object later
    def __init__(self, host, port, username):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a client object
        self.sock.connect((host, port))
        
        self.userName = username

        self.ui_done = False
        
        self.running = True

        uiThread = threading.Thread(target=self.UILoop)
        reciveThread = threading.Thread(target=self.receive) # create a thread (paralel process) that has the code from our recive function
        uiThread.start() # start the thread
        reciveThread.start() # start the thread



        #by declaring variables with self.[the variable's name] it means we are making a variable inside this class that can be accesed when we make an object of this class like this, object1 = class(), variable = object1.var1 
        

    def UILoop(self):
        # object.pack() jusyt places the created ui object on the screen and takes arguments determining location and padding etc. 
        self.wind = tkinter.Tk()
        self.wind.config(bg="lightgray")
        
        self.chatLabel = tkinter.Label(self.wind, text="Chat:", bg="lightgray") # creates a label
        self.chatLabel.pack()

        self.textLog = tkinter.scrolledtext.ScrolledText(self.wind) # creates a scrolling label
        self.textLog.pack(padx=20, pady=5)
        self.textLog.config(state="disabled")

        #self.ClientList = tkinter.scrolledtext.ScrolledText(master=self.wind)
        #self.ClientList.pack()
        #self.ClientList.config(state="disabled")

        self.msgLabel = tkinter.Label(self.wind, text="Message:", bg="lightgray") # creates a label
        self.msgLabel.pack()

        self.txtInputArea = tkinter.Text(self.wind, height=3) # creates a text box for inputs
        self.txtInputArea.bind("<Return>", self.write)
        self.txtInputArea.pack() 

        self.chatLabel = tkinter.Label(self.wind, text=" ", bg="lightgray") # creates a label
        self.chatLabel.pack()

        #  self.sndButton = tkinter.Button(self.wind, text="Send", command=self.write) # creates a button for sending the messages 
        # self.sndButton.pack()

        self.ui_done = True # lets the program know the ui has finished setting up

        self.wind.protocol = ("WM_DELETE_PROTOCOL", self.stop)

        self.wind.mainloop() # calls the ui loop
    
    def receive(self):
        while self.running:
            try:
                messege = self.sock.recv(1024).decode("utf-8") # sets messege to be the input from the server decoded 
                if (messege == "User:"): # if the server asks for our user
                  self.sock.send(self.userName.encode('utf-8')) # send our username, encoded in utf-8
                
                #elif(messege.startswith("/clientlist")):
                 #   self.ClientList.config(state="normal")
                  #  self.ClientList.insert('end', messege)
                   # self.ClientList.yview('end')
                    #self.ClientList.config(state="disabled")

                else:
                    if self.ui_done: # if the ui is set up
                        self.textLog.config(state="normal") # allow us to change the data of the chat log
                        self.textLog.insert('end', messege) # insert our message 
                        self.textLog.yview('end')
                        self.textLog.config(state="disabled")

                    
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break

    def write(self, event=None):
        message = f"{self.userName}: {self.txtInputArea.get('1.0', 'end')}"
        self.sock.send(message.encode("utf-8"))
        self.txtInputArea.delete("1.0", "end")
        return 'break'

    def stop(self):
        self.running = False
        self.wind.destroy
        self.sock.close
        exit(0)

def startFunc():
        userMsg = tkinter.Tk() # creates a tkinter widget
        userMsg.withdraw() # hides the window

        userName = simpledialog.askstring("Username:", "Choose a username", parent=userMsg)
        PORT = simpledialog.askinteger("Port:", "Choose an open port (55555)", parent=userMsg)
        HOST = simpledialog.askstring("Host ip address", "Choose the host's public ip address (127.0.0.1)", parent=userMsg)
        client = Client(HOST, PORT, userName)



startFunc()

        
           

