'''
Ganeshbabu Thavasimuthu
1001452475
'''

import socket
import sys
import json
import random 
from packet import Packet
oldsysout = sys.stdout
import datetime
import time
from threading import Timer
    
class Ann:
    Jan = 2002
    Chan = 2003
    H = 3001
    
    def __init__(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip,2001))
        self.client_socket.connect((ip, port))
    
    def log(self, msg):
        log_file = open("annconversation.log","a")
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

    '''def retransmit(self, lostpacket):
         # Frame 1
        self.log("Sending first packet to the server")
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,0,0,0,0,1,0)
        frame1 = Packet(sourceid, destid, seqnum, acknum, flags, "")
        self.log(frame1)
        self.log("20secs timer starts..")
        self.log("after 20secs..")
        self.log("Packet lost..")
        self.log("Retransmitting it..")
        self.log(frame1)
        self.client_socket.send(frame1.serialize().encode())'''
        
    def establish_handshake(self):
        sourceid = 2001
        destid = 1234
        
        # Frame 1
        self.log("Sending first packet to the server")
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,0,0,0,0,1,0)
        frame1 = Packet(sourceid, destid, seqnum, acknum, flags, "")
        self.log(frame1)
        self.log("20secs timer starts..")
        self.log("after 20secs..")
        self.log("Packet lost..")
        self.log("Retransmitting it..")
        self.log(frame1)
        self.client_socket.send(frame1.serialize().encode())
        self.log("\nResponse from server \n")
        while True:
            #self.log("waiting for response")
            response = self.client_socket.recv(1024).decode('utf-8')
            if not response:
                #print("Timer 10secs started...")
                #Timer(10, self.retransmit, (frame1, )).start()
                continue
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
                self.log("MissionTCP: Ann, You are connected. Start the mission!!")
                break;
                
            if not response:
                break
            self.log("\n")
        self.log("DONE")
        
    def sendFileTo(self, dest):
        filepath = ""
        if dest==self.Jan:
            filepath = "confidential/Ann/Ann-_Jan.txt";
        elif dest==self.Chan:
            filepath = "confidential/Ann/Ann-_Chan.txt";
        
        seqnum = 0
        acknum = 0
        flags = (0,0,0,1,0,0,0)           
        filecontent = ""
        with open(filepath, 'r') as file_to_send:
            for data in file_to_send:
                filecontent += data
                
        
        filepacket = Packet(2001, dest, seqnum, acknum, flags, filecontent)
        self.log(filepacket)
        self.client_socket.send(filepacket.serialize().encode('utf-8'))
        
    def listencontinuously(self):
        chanMsgs = []
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')  
            if not response:
                continue
            packet = json.loads(response)
            logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {}\n URG Pointer: {} \n Data: {}".format(packet['sourceid'], packet['destid'],packet['seqnum'],packet['acknum'],packet['flags'],packet['urgpointer'],packet['data'])
            self.log(logpacket)
            if packet['sourceid'] == 2003:
                self.log("packet received from Chan ")
                chanMsgs.append(packet)
                if (len(chanMsgs)==5):
                    # Download conversations
                    self.log("Downloading conversations with Chan (annconversations.log, chanconversations.log)")
                    
                    # Terminate Chan
                    seqnum = packet['acknum']
                    acknum = packet['seqnum'] + 1
                    flags = (0,1,1,0,1,0,0)
                    data = "Chan, something fishy. Terminating connections right now!"
                    terpacket = Packet(2001, 2003, seqnum, acknum, flags, data)
                    self.log("Sending packet with RST and TER bit to Chan")
                    self.client_socket.send(terpacket.serialize().encode())
                    
                    #Inform Jan
                    seqnum = packet['acknum']
                    acknum = packet['seqnum'] + 1
                    flags = (0,0,1,1,0,0,0)
                    data = "Jan, Terminating my Chan connections right now due to security concerns! Just wanted to keep you informed!"
                    terpacket = Packet(2001, 2002, seqnum, acknum, flags, data)
                    self.log("Sending packet with URG bit to Jan")
                    self.client_socket.send(terpacket.serialize().encode())

            # Process location packet from Jan
            elif packet['sourceid'] == 2002 and packet['flags'][2]==1:
                # Confirm the location coordinates and grant permission
                airforce_code = "PEPPER THE PEPPER"
                seqnum = packet['acknum']
                acknum = packet['seqnum'] + 1
                flags = (0,0,0,0,1,0,0)
                data = "Execute **"+airforce_code+"**"
                terpacket = Packet(2001, 2002, seqnum, acknum, flags, data)
                self.log("Approving Ann's request to execute the mission with airforce code")
                self.client_socket.send(terpacket.serialize().encode())

            # Process Success packet from Jan
            elif packet['sourceid'] == 2002 and packet['flags'][1]==1:
                # Confirm the location coordinates and grant permission
                seqnum = packet['acknum']
                acknum = packet['seqnum'] + 1
                flags = (0,1,1,0,1,0,0)
                urgpointer = "32.76 N, -97.07W"
                data = "Good job Jan. Meet me at the specified coordinates. Let's party!"
                terpacket = Packet(2001, 2002, seqnum, acknum, flags, data, urgpointer)
                self.log("Congratulations message sent with location coordinates to Jan")
                self.client_socket.send(terpacket.serialize().encode())
                break
                    
        
ann = Ann(str(sys.argv[1]),int(sys.argv[2]))
ann.log("*** HOST : Ann *** ")
ann.establish_handshake()
# Get the yes or no from Ann
ans = input("Transfer files to Jan? (Y/N)")
if (ans == 'Y' or ans=='y' or ans=='yes'):
    ann.sendFileTo(ann.Jan)

ans = input("Transfer files to Chan? (Y/N)")
if (ans == 'Y' or ans=='y' or ans=='yes'):
    ann.sendFileTo(ann.Chan)
    
# Listen continuously for the data
ann.listencontinuously()

ann.client_socket.close()