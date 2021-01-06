class BaseSocketConnector:
    def __init__(self,
        IP, PORT,
        HEADER=16,
        FORMAT='utf-8',
        DISCONNECT='!disconnect'):
        def setConst():
            self.IP = IP
            self.PORT = PORT
            self.ADDR = (IP, PORT)
            self.HEADER = HEADER
            self.FORMAT = FORMAT
            self.DISCONNECT = DISCONNECT
        def setCallbacks():
            self.connectCallbacks = []
            self.disconnectCallbacks = []
            self.messageCallbacks = []
        setConst()
        setCallbacks()
    
    def _connectCallback(self, addr, conn):
        for callback in self.connectCallbacks:
            callback( addr, conn )
    def _disconnectCallback(self, addr):
        for callback in self.disconnectCallbacks:
            callback( addr )
    def _messageCallback(self, addr, conn, msg):
        for callback in self.messageCallbacks:
            callback( addr, conn, msg )
    
    def onConnect(self, callback, args:tuple = (), kwargs:dict = {}):
        self.connectCallbacks.append(
            lambda addr, conn:\
            callback(addr, conn, *args, **kwargs)
        )
    def onDisconnect(self, callback, args:tuple = (), kwargs:dict = {}):
        self.disconnectCallbacks.append(
            lambda addr:\
            callback(addr, *args, **kwargs)
        )
    def onMessage(self, callback, args:tuple = (), kwargs:dict = {}):
        self.messagCallbacks.append(
            lambda addr, conn, msg:\
            callback(addr, conn, msg, *args, **kwargs)
        )
    
    
    def sendTo(self, conn, msg):
        msgLen = str(len(msg))
        msgLenSized = msgLen + ' '*(self.HEADER - len*msgLen)
        msgLenSend = msgLenSized.encode(self.FORMAT)
        msgSend = msg.encode(self.FORMAT)
        conn.send(msgLenSend)
        conn.send(msgSend)
