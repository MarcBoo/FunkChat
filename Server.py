#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""


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
                whisper(target, targetmsg)
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def whisper(target, targetmsg):  
    """Whispers a message to a certain client."""

    print(target)
    print(targetmsg)
    targetmsg = targetmsg.decode("utf-8")
    for sock, user in clients.items():
       
        user = bytes(user, "utf8")
        print(str(user) + "\n" + str(sock))
        if user == target:
            print("funktioniert")
            sock.send(bytes(targetmsg, "utf8"))


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
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
