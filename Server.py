# Giang Ly
# CS 464 Project
# Server.py

import socket
from threading import Thread
import re


class ClientThread(Thread):
    def __init__(self, conn, addr):
        """
        Initialization for client thread parameters
        (E.g: host, port, socket)
        """
        self.conn = conn
        self.addr = addr
        Thread.__init__ (self)

    def run(self):
        """
        Send/receive data using the socket you created
        Sending message to connected client
        """
        while True:
            #Receiving from client
            data = self.conn.recv(1024)
            
            if not data:
                break
                
            #Parse Data to see if it is an HTTP request or request from
            #Client.py
            if (re.match('GET', data.decode()) != None):
                result = re.search('GET /(.*) HTTP', data.decode())
                req = result.group(1)
        
                if (req == ''):
                    req = 'index.html'
            
                if req.endswith(".html"):
                    mimetype='text/html'    
                elif req.endswith(".jpg"):
                    mimetype='image/jpg'         
                elif req.endswith(".gif"):
                    mimetype='image/gif'            
                elif req.endswith(".js"):
                    mimetype='application/javascript'
                elif req.endswith(".css"):
                    mimetype='text/css'
                else:
                    mimetype = 'text/html'

                try:
                    f = open(req,'rb')
                    fin = f.read() # read file content                       
                    f.close()   
                    response_headers = self._gen_headers( 200, mimetype)          
                except Exception as e: #in case file was not found, generate 404 page
                    print ("Warning, file not found. Serving response code 404\n", e)
                    response_headers = self._gen_headers( 404, mimetype)
                    fin = b"<html><HEAD><TITLE>Not Found</TITLE></HEAD><body><p>Error 404: File not found</p></body></html>"  

                server_response = response_headers.encode() # return headers for GET and HEAD
                server_response += fin  # return additional conten for GET only
            else:
                server_response = data.decode().upper()
                print("sending: " + server_response)
                server_response = server_response.encode()
        
            conn.sendall(server_response)

        self.conn.close()
        print ('Closed connection:', self.addr[0])
        
    
    def _gen_headers(self, code, mime_type):
        """ Generates HTTP response Headers. Ommits the first line! """
        # determine response code
        h = ''
        if (code == 200):
           h = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
           h = 'HTTP/1.1 404 Not Found\n'
    
        # insert header for content type
        h += 'Content-type: ' + mime_type +'\n\n'
        return h

## Determine the host
host = input("Name of server:")

## Determine the port number
port = eval(input("Port Number:"))

## Create a new socket and attach the host/address to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created")
 
s.bind((host, port))
print('Socket binding complete')

## Loop for listening requests
while True:
    ## Listen for connections. Maximum queued connections should be >1
    s.listen(10)
    print('Socket is now listening...')
    
    ## Accept the connection
    conn,addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    ## Create a new client thread and start the thread
    ClientThread(conn,addr).start()

