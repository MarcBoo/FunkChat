#!/usr/bin/env python3
"""Server Application for our Multithreaded and Asynchronous Chat Application"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def client_new_connection():
    """Controls connections of new clients"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=client_control, args=(client,)).start()


def client_control(client):  # Takes client socket as argument.
    """Controls interaction with a single client."""


    # Username saved in name
    # if not already in it, will be appended to clients
    # delete after leaving does not work properly yet
    name = client.recv(BUFSIZ).decode("utf8")
    if name in clients.values():
        client.send(bytes("Your name is already taken!", "utf8"))
        client.close()
        del clients[client]
        broadcast(bytes("%s has left the chat." % name, "utf8"))
    else:
        welcome = 'Welcome %s! If you ever want to quit, type /quit to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        print(clients.values())

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("/quit", "utf8"):
            if bytes("/whisper", "utf8") in msg:
                client.send(bytes("type in your target", "utf8"))
                target = client.recv(BUFSIZ)
                client.send(bytes("type in your message", "utf8"))
                targetmsg = client.recv(BUFSIZ)
                prefix = clients[client]
                client.send(bytes(prefix + " (Whisper) to ", "utf8") + target +  bytes(": ","utf8") + targetmsg)
                whisper(target, targetmsg, prefix + ": ")
                continue
            elif bytes("/users", "utf8") in msg:
                client.send(bytes("This is not yet implemented", "utf8")) #showUsers()
                continue 
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for sending name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def whisper(target, targetmsg, prefix=""):  
    """Whispers a message to a certain client.
    Still needs display of message on sending side"""

    targetmsg = targetmsg.decode("utf-8")
    for sock, user in clients.items():
       
        user = bytes(user, "utf8")
        if user == target:
            sock.send(bytes(prefix + "(Whisper) " + targetmsg, "utf8")) #Name of sending user still missing

def showUsers():
    """Reads out connected Users to requester
    for user in clients.values():
        client.send(bytes(user,"utf8"))"""



clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=client_new_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
