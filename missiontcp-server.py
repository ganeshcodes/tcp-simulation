'''
Ganeshbabu Thavasimuthu
1001452475
'''

import socket
from threading import Thread
import json
import random
import sys
import datetime
from packet import Packet
oldsysout = sys.stdout

class MissionTCPServer:
    Ann = 2001
    Jan = 2002
    Chan = 2003
    airforce = 3001
    serverport = 1234
    annSocket = ""
    janSocket = ""
    chanSocket = ""
    airSocket = ""
    textfile = ""

    def __init__(self, ip, port):
        self.serverport = port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen(5)
        self.log("*** MISSON TCP SERVER ***")
        self.log(('Listening on {}:{}').format(ip,port))
        self.__listen(server_socket)
    
    def log(self, msg):
        log_file = open("missiontcp.log","a")
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M")
        sys.stdout = log_file
        print(timestamp + ": "+ str(msg))
        sys.stdout = oldsysout
        print(msg)

    def __listen(self, server_socket):
        while True:
            #Establish the connection
            self.log('Ready to serve...\n')
            connectionSocket, addr = server_socket.accept()
            if addr[1]==self.Ann:
                self.annSocket = connectionSocket
            elif addr[1]==self.Jan:
                self.janSocket = connectionSocket
            elif addr[1]==self.Chan:
                self.chanSocket = connectionSocket
            elif addr[1]==self.airforce:
                self.airSocket = connectionSocket
            #Create new thread for every request and response pair
            Thread(target=self.__handleRequest, args=(connectionSocket,addr)).start()
        server_socket.close()

    def __handleRequest(self, connectionSocket, addr):
        #self.log(connectionSocket)
        try:
            if addr[1]==self.Ann:
                self.log("Initiating 3 way handshake for Ann")
                while True:
                    data = connectionSocket.recv(10024).decode('utf-8')
                    #self.log(data)
                    if not data:
                        continue
                    packet = json.loads(data)
                    logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(packet['sourceid'], packet['destid'],packet['seqnum'],packet['acknum'],packet['flags'],packet['data'])
                    
                    self.log(logpacket)
                    if (packet['destid'] == self.serverport):
                        # Frame1 from client
                        if (packet['acknum'] == 0 and packet['flags'][-2] == 1):
                            seqnum = random.randint(100,200)
                            acknum = packet['seqnum'] + 1
                            flags = (0,0,0,1,0,1,0)
                            # Send Frame2 to the client
                            frame2 = Packet(self.serverport, packet['sourceid'], seqnum, acknum, flags, "")
                            connectionSocket.send(frame2.serialize().encode())
                            self.log("sent frame2 to the client")

                            # Wait for Frame3 from client with ACK set to 1 and SYN set to 0
                            self.log("wating for frame 3 from Ann...")
                            data = connectionSocket.recv(1024).decode('utf-8')
                            self.log("recieved")
                            #self.log(data)
                            frame3 = json.loads(data)
                            logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(frame3['sourceid'], frame3['destid'],frame3['seqnum'],frame3['acknum'],frame3['flags'],frame3['data'])
                            self.log(logpacket)

                            if frame3['flags'][3] == 1 and frame3['flags'][-2] == 0:
                                self.log("Connection successfully established to Ann")
                                #connectionSocket.send("MissionTCP: Ann, You are connected, start the mission!!")
                        

                    # Recieve file from Ann
                    elif packet['destid'] == self.Jan:
                        #self.log(self.janSocket)
#                        self.log(packet['data'])
                        self.log("Ann >> Jan packet forwarding")
                        self.janSocket.send(data.encode())
                        
                    # Recieve file from Chan
                    elif packet['destid'] == self.Chan:
                        #self.log(packet['data'])
                        self.log("Ann >> Chan packet forwarding")
                        self.chanSocket.send(data.encode())

            elif addr[1]==self.Jan:
                self.log("Initiating 3 way handshake for Jan")
                while True:
                    data = connectionSocket.recv(1024).decode('utf-8')
                    if not data:
                        continue
                    packet = json.loads(data)
                    logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(packet['sourceid'], packet['destid'],packet['seqnum'],packet['acknum'],packet['flags'],packet['data'])
                    
                    self.log(logpacket)
                    self.log("dest id = "+str(packet['destid']))
                    
                    if (packet['destid'] == self.serverport):
                        # Frame1 from client
                        if (packet['acknum'] == 0 and packet['flags'][-2] == 1):
                            seqnum = random.randint(100,200)
                            acknum = packet['seqnum'] + 1
                            flags = (0,0,0,1,0,1,0)
                            # Send Frame2 to the client
                            frame2 = Packet(self.serverport, packet['sourceid'], seqnum, acknum, flags, "")
                            connectionSocket.send(frame2.serialize().encode())
                            self.log("sent frame2 to the client")

                            # Wait for Frame3 from client with ACK set to 1 and SYN set to 0
                            self.log("wating for frame 3 from Ann...")
                            data = connectionSocket.recv(1024).decode('utf-8')
                            self.log("recieved")
                            self.log(data)
                            frame3 = json.loads(data)
                            if frame3['flags'][3] == 1 and frame3['flags'][-2] == 0:
                                self.log("Connection successfully established to Jan")
                                #connectionSocket.send("MissionTCP: Ann, You are connected, start the mission!!")
                        
                    elif packet['destid'] == self.airforce:
                        self.log("Jan >> Airforce packet forwarding")
                        self.airSocket.send(data.encode())

                    elif packet['destid'] == self.Ann:
                        self.log("Jan >> Ann packet forwarding")
                        self.annSocket.send(data.encode())

            elif addr[1]==self.Chan:
                print("address = "+str(addr[1]))
                self.log("Initiating 3 way handshake for Chan")
                while True:
                    data = connectionSocket.recv(1024).decode('utf-8')
                    if not data:
                        continue
                    packet = json.loads(data)
                    logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(packet['sourceid'], packet['destid'],packet['seqnum'],packet['acknum'],packet['flags'],packet['data'])
                    
                    self.log(logpacket)
                    
                    if (packet['destid'] == self.serverport):
                        # Frame1 from client
                        if (packet['acknum'] == 0 and packet['flags'][-2] == 1):
                            seqnum = random.randint(100,200)
                            acknum = packet['seqnum'] + 1
                            flags = (0,0,0,1,0,1,0)
                            # Send Frame2 to the client
                            frame2 = Packet(self.serverport, packet['sourceid'], seqnum, acknum, flags, "")
                            connectionSocket.send(frame2.serialize().encode())
                            self.log("sent frame2 to the client")

                            # Wait for Frame3 from client with ACK set to 1 and SYN set to 0
                            self.log("wating for frame 3 from Chan...")
                            data = connectionSocket.recv(1024).decode('utf-8')
                            self.log("recieved")
                            self.log(data)
                            frame3 = json.loads(data)
                            if frame3['flags'][3] == 1 and frame3['flags'][-2] == 0:
                                self.log("Connection successfully established to Ann")
                                #connectionSocket.send("MissionTCP: Ann, You are connected, start the mission!!")
                                
                    elif packet['destid'] == self.Ann:
                        #self.log(self.janSocket)
#                        self.log(packet['data'])
                        self.log("Chan >> Ann packet forwarding")
                        self.annSocket.send(data.encode())
            
            elif addr[1]==self.airforce:
                self.log("Initiating 3 way handshake for Airforce")
                while True:
                    data = connectionSocket.recv(1024).decode('utf-8')
                    if not data:
                        continue
                    packet = json.loads(data)
                    logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(packet['sourceid'], packet['destid'],packet['seqnum'],packet['acknum'],packet['flags'],packet['data'])
                    
                    self.log(logpacket)
                    
                    if (packet['destid'] == self.serverport):
                        # Frame1 from client
                        if (packet['acknum'] == 0 and packet['flags'][-2] == 1):
                            seqnum = random.randint(100,200)
                            acknum = packet['seqnum'] + 1
                            flags = (0,0,0,1,0,1,0)
                            # Send Frame2 to the client
                            frame2 = Packet(self.serverport, packet['sourceid'], seqnum, acknum, flags, "")
                            connectionSocket.send(frame2.serialize().encode())
                            self.log("sent frame2 to the client")

                            # Wait for Frame3 from client with ACK set to 1 and SYN set to 0
                            self.log("wating for frame 3 from Airforce...")
                            data = connectionSocket.recv(1024).decode('utf-8')
                            self.log("recieved")
                            self.log(data)
                            frame3 = json.loads(data)
                            if frame3['flags'][3] == 1 and frame3['flags'][-2] == 0:
                                self.log("Connection successfully established to Airforce")
                                #connectionSocket.send("MissionTCP: Ann, You are connected, start the mission!!")
                                
                    elif packet['destid'] == self.Jan:
                        self.log("Airforce >> Jan packet forwarding")
                        self.janSocket.send(data.encode())

            else:
                self.log("Somebody is trying to snoop into the MissionTCP")
                self.log("\n Broadcasting ALERT to Ann, Jan and Chan!")
                    
            #connectionSocket.close()
            
        except IOError as e:
            #Send response message for file not found
            '''if 'No such file' in str(e):
                connectionSocket.send(b'HTTP/1.1 404 NOT FOUND\n')
                connectionSocket.send(b'Content-Type: text/html; encoding=utf8 \nConnection: Close\n')
                connectionSocket.send(b'\n')
                connectionSocket.send(b'Oops! The file you requested is not found in server (404)')
                #Close client socket
                connectionSocket.close()
                return False'''
                

MissionTCPServer('127.0.0.1',1234)