# Inserting modules  needed for the application
import socket, sys, os, _thread

# Introduction
print('\n****************************************************************************************************************************************************************************\n')
print('\nHTTP Proxy Server \nMade By Shubham Roy - IEC2018002 \nThe Server works only with HTTP GET Requests\n')
print('\n****************************************************************************************************************************************************************************\n')

# Taking user input for port number
try:
    proxy_port = int(input('\n*********************************************************************Enter Port Number**************************************************************************************\n'))
except KeyboardInterrupt:
    print('\n*****************************************************************User Requested Interrupt***********************************************************************************\n')
    print('\nEnding....\n')
    sys.exit()


#****Constants****

QUEUE_SIZE = 5             # how many pending connections queue will hold
BUFFER_SIZE = 8192         # max number of bytes we receive at once

#*****************

#********************************************************************************************************
# Following Function sets up the socket connecting the client and the proxy server
def setUp():
    
    try:
        proxy_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Socket creation using IPV4 addressing and TCP protocol. This socket is used for establishing TCP handshaking.
        proxy_server.bind(('',proxy_port)) # Socket binding to localhost and user-entered port 
        proxy_server.listen(QUEUE_SIZE) # Socket is correctly set-up and is listening for client

        print('\n*********************************************************Socket Initialized And Binded Successfully*************************************************************************')
        print('\nProxy Server Started At Port: ', str(proxy_port), ' And IP: ', socket.gethostbyname(socket.gethostname()), '\n')
    except Exception as error:
        print('\n*********Server Failed To Start*********\n')
        #print('\n*********Error: ', str(error), '*********\n')
        sys.exit(2)

    # Getting connections from clients
    i = 0
    while 1:
        try:
            i = i + 1
            conn, addr = proxy_server.accept() # conn is the socket used for actual transfer of messages b/w client and proxy-server
            print('\n', str(i), ') Proxy Server Got Connection From: ', addr[0], '\n')
            request = conn.recv(BUFFER_SIZE)
            _thread.start_new_thread(requestParse,(conn,addr,request)) # Multi-threading
        except KeyboardInterrupt:
            proxy_server.close()
            print('\n*****************************************************************User Requested Interrupt***********************************************************************************\n')
            print('\nEnding....\n')
            sys.exit(1)
    proxy_server.close()

#********************************************************************************************************

#********************************************************************************************************
# Following function parses the byte string request (HTTP REQUEST MESSAGE format) received from client and extracts origin server and port
# Few types of URLs are:
# 1) http://www.example.com/
# 2) www.example.com
# 3) http://www.example.com:1234/path/
# .....

def requestParse(conn, addr, request):
    try:
        first_line = request.split(b'\n')[0]
        print('\nClient requested: ', str(first_line), '\n')
        url = first_line.split(b' ')[1]

        http_pos = url.find(b'://')
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):] 
        
        port_pos = temp.find(b':') 
        webserver_pos = temp.find(b'/')
        if (webserver_pos == -1):
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]
        getRequest(webserver, port, conn, addr, request)
    except Exception as error:
        #print('1.....', str(error))
        pass

#********************************************************************************************************

#********************************************************************************************************
# Following function establishes contact with origin server from the proxy server to fetch client request and sends the response back to the client via the proxy server
 
def getRequest(webserver, port2, conn, addr, request):

    try:
        origin_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        origin_server.connect((webserver,port2))
        origin_server.send(request)

        while True:

            response = origin_server.recv(BUFFER_SIZE)
            if (len(response) > 0):
                conn.send(response)
                print('\nSending Client The Response: ', str(request.split(b'\n')[0]), '\n')
                print('\n**************************************************************************SUCCESS*******************************************************************************************\n')
            else:
                print('\n**************************************************************************FAILURE*******************************************************************************************\n')
                print('\nOnly HTTP GET Requests Are Served!!!\n')
                break
        origin_server.close()
        conn.close()
    except socket.error as message:
        print('\n**************************************************************************FAILURE*******************************************************************************************\n')
        print('\nOnly HTTP GET Requests Are Served!!!\n')
        origin_server.close()
        conn.close()
        sys.exit(1)

#********************************************************************************************************

setUp()
