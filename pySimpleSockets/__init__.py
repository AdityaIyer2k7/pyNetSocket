class Server:
    def __init__(self,
            IP, PORT,
            FORMAT='utf-8',
            DISCONNECT='!Disconnect'):
        self.SIP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT)
        self.FORMAT = FORMAT
        self.DISCONNECT = DISCONNECT
        self.connectCallbacks = []
        self.disconnectCallbacks = []
        self.eventCallbacks = {}
    
    def onConnect(self, callback, args, kwargs):
        self.connectCallbacks.append(lambda addr, conn: \
            callback(addr, conn, *args, **kwargs)
        )
    
    def onDicconnect(self, callback, args, kwargs):
        self.disconnectCallbacks.append(lambda addr, conn: \
            callback(addr, conn, *args, **kwargs)
        )
