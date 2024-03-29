#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.ttk import *
from tkinter import *


def receive():
    """Handles receiving of messages."""
    while True:
        msg = client_socket.recv(BUFSIZ)
        if isinstance(msg, bytearray):
            msg = msg.decode("utf8")
            usr_list.insert(tkinter.END, msg)
        else:
            msg.decode("utf8")
            msg_list.insert(tkinter.END, msg)
        


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "/quit":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit") #Bug , depending on idle wont show to others
    send()

top = tkinter.Tk()
top.title("Chattool Funk")
top.resizable(width = False, height = False)
top.configure(bg = "#17202A")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set, bg = "#17202A", fg = "#EAECEE",)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width=60)
entry_field.bind("<Return>", send)
entry_field.pack()
photo = PhotoImage(file = "Send-Icon-PNG.png")
send_button = tkinter.Button(top, image = photo, command=send, borderwidth = 0, bg = "#17202A")
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


#----Now comes the sockets part----
HOST = "localhost" # input('Enter host: ')
PORT = 33000 # input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
