# Giang Ly
# CS464 Project 
# Client.py

import socket

def Main():
    
    """Takes user input from client after 
    connecting to specific IP and
    port. Returns the message in all CAPS.
    """
    
    ## Determine the host
    host = input("Name of server:")

    ## Determine the port number 
    port = eval(input("Port Number:"))

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = input(" -> ")

    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print('Received from server: ' + data)

        message = input(" -> ")

    mySocket.close()

if __name__ == '__main__':
    Main()
