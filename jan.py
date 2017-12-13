'''
Ganeshbabu Thavasimuthu
1001452475
'''

import socket
import sys
import json
import random 
from packet import Packet
import datetime
oldsysout = sys.stdout
    
class Jan:
    def __init__(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip,2002))
        self.client_socket.connect((ip, port))
    
    def log(self, msg):
        log_file = open("janconversation.log","a")
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
        sourceid = 2002
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
                self.log("MissionTCP: Jan, You are connected. Start the mission!!")
                break
                
            if not response:
                break
            self.log("\n")
        self.log("DONE")
    
    def receiveFile(self):
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')
            if response:
                tcppacket = json.loads(response)
                self.log(tcppacket)
                self.log("Received file from destination "+str(tcppacket['sourceid']))
                break

    def kickstart_mission(self):
        # Location packet with URG bit and URG pointer
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,0,1,1,0,0,0)
        urgpointer = "32.43 22.77 N,97.9 7.53 W"
        frame1 = Packet(2002, 2001, seqnum, acknum, flags, "Ann, Approve my request to execute the mission", urgpointer)
        self.client_socket.send(frame1.serialize().encode())

        # Wait for the confirmation from Ann
        airforce_authorization_code = ""
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')
            if response:
                tcppacket = json.loads(response)
                logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['data'])
                self.log(logpacket)
                self.log("Received packet from destination "+str(tcppacket['sourceid']))
                airforce_authorization_code = tcppacket['data']
                break

        # Send the mission execution command to airforce
        self.connect_to_airforce(airforce_authorization_code)

    def connect_to_airforce(self, authorization_code):
        # Location packet with URG bit and URG pointer and authorization code
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,0,1,1,0,0,0)
        urgpointer = "32.43 22.77 N,97.9 7.53 W"
        data = authorization_code
        frame1 = Packet(2002, 3001, seqnum, acknum, flags, data, urgpointer)
        self.client_socket.send(frame1.serialize().encode())

        # Wait for the confirmation from Airforce
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')
            if response:
                tcppacket = json.loads(response)
                logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['data'])
                self.log(logpacket)
                self.log("Received packet from destination "+str(tcppacket['sourceid']))
                break
        
        # Jan sends success message to Ann
        seqnum = random.randint(1000,2000)
        acknum = 0
        flags = (0,1,0,1,0,0,0)
        frame1 = Packet(2002, 2001, seqnum, acknum, flags, "Mission Success", "CONGRATULATIONS WE FRIED DRY GREEN LEAVES")
        self.client_socket.send(frame1.serialize().encode())

        # Wait for the final response from Ann 
        while True:
            response = self.client_socket.recv(10024).decode('utf-8')
            if response:
                tcppacket = json.loads(response)
                logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n URG Pointer:{} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['urgpointer'],tcppacket['data'])
                self.log(logpacket)
                self.log("Received packet from destination "+str(tcppacket['sourceid']))
                break
                    
jan = Jan(str(sys.argv[1]),int(sys.argv[2]))
jan.log("*** HOST : Jan *** ")
jan.establish_handshake()
jan.receiveFile()

# Log the packet (this probably be the packet from Ann who informs about Chan termination)
while True:
    response = jan.client_socket.recv(10024).decode('utf-8')
    if response:
        tcppacket = json.loads(response)
        logpacket = " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n Data: {}".format(tcppacket['sourceid'], tcppacket['destid'],tcppacket['seqnum'],tcppacket['acknum'],tcppacket['flags'],tcppacket['data'])
        jan.log(logpacket)
        jan.log("Received packet from destination "+str(tcppacket['sourceid']))
        jan.log("Time to request for approval..")
        break

# Send location to Ann
jan.kickstart_mission()
jan.client_socket.close()
        
