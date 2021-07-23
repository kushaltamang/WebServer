#Name: Mohit Tamang   Student ID: 1001552822
from socket import *
import threading

#input = path of the requested file
#function = send appropriate HTTP response based on the file asked by the client
#output = HTTP response with status line, header lines, and appropriate data
def send_HTTPresponse(filepath,clientSocket):
    try:#opening and reading the requested file       
        f = open(filepath[1:],'rb') 
        outputdata = f.read()
            
    except FileNotFoundError: #if file is not found, send 404 Not Found response
        response_msg = ("HTTP/1.0 404 Not Found\r\n\r\n") #status line for 404 Not found
        clientSocket.send(response_msg.encode()) #send the status to the client
        
    #Send the contents of the requested file to the client
    if(filepath == "/starrynight.jpg".encode()): #if the requested file is an image
        response_msg = ("HTTP/1.0 200 OK\r\n" #200 status code
                        +"Content-Type: image/jpg\r\n\r\n") #header line for image
        clientSocket.send(response_msg.encode()) #send response message
        clientSocket.send(outputdata) #send content of the image file read
        f.close()
        
    else:
        if(filepath == "/index.html".encode()): 
            response_msg = ("HTTP/1.0 200 OK\r\n" # 200 status code
                           +"Content-Type: text/html\r\n\r\n") #header line for a text file
            clientSocket.send(response_msg.encode()) #send response message
            clientSocket.send(outputdata) #send the base HTML file
            f.close()
                
        elif(filepath == "/index1.html".encode()):
            response_msg = ("HTTP/1.0 301 OK\r\n" # 301 status code
                           +"Location: http://localhost:8080/index.html\r\n\r\n")#permanent location of the website
            clientSocket.send(response_msg.encode()) #send response message
            clientSocket.send(outputdata) #send base HTML file
            f.close()
            
    clientSocket.close() #close the client connection
    #print("Client socket closed ")
    return


#input = server TCP connected socket
#function = listen to client's requests, establish connection with the client, and create a thread to handle the request
#output = threads for response fucntion to handle the client request 
def listen(serverSocket):
        serverSocket.listen(1)#start listening to the requests
        print("Listening for incoming client requests")
        while True:
            clientSocket, address = serverSocket.accept() #establish connection with the client
            #print("Got connection from:", address)
            clientSocket.settimeout(60) #set connection time to 60s
            threading.Thread(target = response, args = (clientSocket,address)).start() #create a thread to send HTTP response
 
#input = client Socket from where we recieve the requests
#function = get the name of requested fileand serve file to the client/browser using the function send_HTTPresponse 
#output =  HTTP response
def response(clientSocket,address):
    while True:
        try:
            message = clientSocket.recv(1024)#request message sent by the browser
            filepath = (message.split()[1]) #get the base html filename from the message(encoded in bytes)
            #print(filepath)
            if message:
                send_HTTPresponse(filepath,clientSocket) #send the appropriate HTTP response
            else:
                print("ERROR CLIENT DISCONNECTED")
        except:
            clientSocket.close() #close the client connection
            return False
try:    
    serverPort = 8080 #socket num of the server
    serverName = 'localhost' #name of the server
    serverSocket = socket(AF_INET, SOCK_STREAM) #create a TCP socket connection
    serverSocket.bind((serverName,serverPort)) #create the server
    listen(serverSocket)
    
except KeyboardInterrupt: 
    print("Closing the server due to keyboard interrupt( Ctrl+C )")
    serverSocket.close() 



    