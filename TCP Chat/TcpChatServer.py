from queue import Queue
import socket
import threading
import tkinter
from tkinter import simpledialog

clients = []
userNames = []


def test():
    print("1")

def getServerInfo():
    servMsg = tkinter.Tk() # creates a tkinter widget
    servMsg.withdraw() # hides the window
    host = simpledialog.askstring("Ip Address", "Set your servers IP address", parent=servMsg)
    port = simpledialog.askinteger("Port", "Set your servers Port", parent=servMsg)
    startServer(host, port)

def startServer(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a server with an ipv4 address and with the TCP protocol
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows us to use this port while its still waiting for late packets to arrive
    server.bind((host, port)) # binds the host and port to our server
    server.listen() # listens for messages or clients wanting to connect 
    recevice(server) # receive messages 
    

def broadcastMessage(message):
    for client in clients: # foreach connected client send the message provided
        client.send(message)

def HandleClient(client):
    while True:
        try:
            messege = client.recv(1024) # try to recive a message from the client and breadcast the message to the clients
            broadcastMessage(messege)

        except: # if theres an error 
            index = clients.index(client) # get the first client in the list of clients
            clients.remove(client) # remove the client
            client.close # close its connection
            userName = userNames[index]
            broadcastMessage("{} left".format(userName).encode("utf-8")) # broadcast a message saying the client left
            userNames.remove(userName) # get rid of the clients user from the list
            


def recevice(server):
    while True:
        client, address = server.accept() # the client and address the client conected with is stored in variables, allow the client to connect
        print("connected with {}".format(str(address)))

        client.send("User:".encode("utf-8")) # ask the client for a username
        user = client.recv(1024).decode("utf-8")
        userNames.append(user) # add the username to the list
        clients.append(client) # add the client to the list
        client.send("/clientlist {}".format(userNames).encode("utf-8"))

        print("Username is {}".format(user))
        broadcastMessage(f"{user} has joined\n".encode("utf-8"))
        client.send("Connected\n".encode("utf-8"))
        thread = threading.Thread(target=HandleClient, args=(client,)) # start a thread with the code from the handle client function
        thread.start() # start the thread
        
getServerInfo()

    


       
        
        
        


        
