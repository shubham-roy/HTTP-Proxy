This project builds a HTTP proxy server for the course of Computer Networks that handles only HTTP GET requests. The server does not perform caching.


TEST PROCEDURE:

1) RUN the myProxyServer.py program from terminal.
2) (a) For testing from localhost change browser settings (Firefox). HOST: localhost ;  PORT: desired-port-number-which-is-used-in-myProxyServer.py
    (b) For testing from other device, set HOST: IPV4 of localhost(system in which python program is running) ; PORT: desired-port-number-which-is-used-in-myProxyServer.py. (NOTE: To get ipv4 address of localhost run ipconfig/ifconfig from terminal)
3) Only HTTP sites will open. Few HTTP sites are listed in "http://scratchpads.eu/explore/sites-list". These sites can be used for testing.


PROGRAM DESIGN:

The script is cross platform since the modules imported are cross-platform i.e available in both windows python and linux python. Python version 3 is used. Error-checking is done at every step using "try" and "except" block. Custom error messages ("SUCCESS" & "FAILURE") will be displayed in the terminal.
"Except KeyboardInterrupt" handles keyboard interrupts.

Script uses 3 functions:

Function 1: setUp() - sets up the socket connecting the client and the proxy server
Function 2: requestParse() - parses the byte string request (HTTP REQUEST MESSAGE format) received from client and extracts origin server and port
Function 3: getRequest() - establishes contact with origin server from the proxy server to fetch client request and sends the response back to the client via the proxy server

The script is explicitly commented for inline details.

For Running in Linux: python3 myProxyServer.py
For Running in Windows: python myProxyServer.py