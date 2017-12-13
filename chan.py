'''
Ganeshbabu Thavasimuthu
1001452475
'''

import socket
import sys
import json
import random 
from threading import Thread
from packet import Packet
import datetime
oldsysout = sys.stdout
    
class Chan:
    terminateflag = False
    
    def __init__(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip,2003))
        self.client_socket.connect((ip, port))
    
    def log(self, msg):
        log_file = open("chanconversation.log","a")
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M")
        sys.stdout = log_file
        print(timestamp + ": "+ str(msg))
        sys.stdout = oldsysout
        print(msg)
        
    def get(self, filename):
        request = 'GET /'+filename+' HTTP/1.1'
        request = request.encode()
        self.log("\nSending GET request to the server for the file "+filename+"\n")
        self.log(request)
        self.client_socket.send(request)
        self.log("\nResponse from server \n")
        while True:
            response = self.client_socket.recv(1024)
            if not response:
                break
            self.log(response.decode())
            self.log("\n")
        self.client_socket.close()
        
    def establish_handshake(self):
        sourceid = 2003
        destid = 1234
        
        # Frame 1
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,0,0,0,0,1,0)
        frame1 = Packet(sourceid, destid, seqnum, acknum, flags, "")
        self.client_socket.send(frame1.serialize().encode())
        self.log("\nResponse from server \n")
        while True:
            #self.log("waiting for response")
            response = self.client_socket.recv(1024).decode('utf-8')
            if not response:
                continue;
            tcppacket = json.loads(response)
            logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['data'])
            self.log(logpacket)
            #self.log("{}{}{}".format(tcppacket['sourceid'],tcppacket['flags'][4],tcppacket['flags'][-2]))
            
            # Frame 2
            if tcppacket['sourceid']==1234 and tcppacket['flags'][3]==1 and tcppacket['flags'][-2]==1:
                seqnum = tcppacket['acknum']
                acknum = tcppacket['seqnum'] + 1
                flags = (0,0,0,1,0,0,0)
                frame3 = Packet(sourceid, tcppacket['sourceid'], seqnum, acknum, flags, "")
                self.log("Sending frame3 to server")
                self.client_socket.send(frame3.serialize().encode())
                self.log("MissionTCP: Chan, You are connected. Start the mission!!")
                break
            if not response:
                break
            self.log("\n")
        self.log("DONE")
        
    def sendFileTo(self, dest):
        filepath = ""
        if dest==self.Jan:
            filepath = "confidential/Ann/Chan-_Jan.txt";
        elif dest==self.Chan:
            filepath = "confidential/Ann/Chan-_Ann.txt";
        
        seqnum = 0
        acknum = 0
        flags = (0,0,0,1,0,0,0)           
        filecontent = ""
        with open(filepath, 'r') as file_to_send:
            for data in file_to_send:
                filecontent += data
                
        
        filepacket = Packet(2003, dest, seqnum, acknum, flags, filecontent)
        self.log(filepacket)
        self.client_socket.send(filepacket.serialize().encode('utf-8'))
    
    def receiveFile(self):
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')
            if response:
                tcppacket = json.loads(response)
                self.log(tcppacket)
                self.log("Received file from destination "+str(tcppacket['sourceid']))
                break
                
    def handleRequest(self):
        while True:
            response = chan.client_socket.recv(10024).decode('utf-8')   
            #print("response came")
            if response:
                tcppacket = json.loads(response)
                logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['data'])
                self.log(logpacket)
                if tcppacket['sourceid']==2001 and tcppacket['flags'][4]==1:
                    chan.log("Chan>> Ok.. Terminating...")
                    self.terminateflag = True
                    break

chan = Chan(str(sys.argv[1]),int(sys.argv[2]))
chan.log("*** HOST : Chan *** ")
chan.establish_handshake()
chan.receiveFile()

# Listen for URG from Ann
# Create new thread for every request and response pair
Thread(target=chan.handleRequest).start()

# Send five messages to Ann
i=0
while not chan.terminateflag:
    if i>4:
        break
    command = input('Type the command to send to Ann: ')
    seqnum = random.randint(10,20)
    acknum = random.randint(50,70)
    flags = (0,0,0,1,0,0,0)
    cmdpacket = Packet(2003, 2001, seqnum, acknum, flags, command)
    chan.client_socket.send(cmdpacket.serialize().encode('utf-8'))
    i+=1

chan.client_socket.close()
'''# Get the yes or no from Ann
ans = input("Transfer files to Jan? (Y/N)")
if (ans == 'Y' or ans=='y' or ans=='yes'):
    chan.sendFileTo(chan.Jan)

ans = input("Transfer files to Ann? (Y/N)")
if (ans == 'Y' or ans=='y' or ans=='yes'):
    chan.sendFileTo(chan.ann)
'''