import sys
import json

class Packet:
    sourceid = 0
    destid = 0
    seqnum = 0
    acknum = 0
    flags = []
    urgpointer = ""
    data = ""
    
    def __init__(self, sourceid, destid, seqnum, acknum, flags, data, urgpointer=""):
        self.sourceid = sourceid
        self.destid = destid
        self.seqnum = seqnum
        self.acknum = acknum
        self.flags = flags
        self.urgpointer = urgpointer
        self.data = data
        
    def serialize(self):
        data = {
            'sourceid': self.sourceid,
            'destid': self.destid,
            'seqnum': self.seqnum,
            'acknum': self.acknum,
            'flags': self.flags,
            'urgpointer': self.urgpointer,
            'data': self.data
        }
        return json.dumps(data)
    
    def __str__(self):
        return " ** TCP PACKET ** \n"+" Source Port: {} \n Destination Port: {} \n Sequence Number: {} \n Ack Number: {}\n flags {} \n URG pointer: {} \n Data: {}".format(self.sourceid, self.destid,self.seqnum,self.acknum,self.flags,self.urgpointer,self.data)
        