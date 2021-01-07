import threading
import socket

sock_family = socket.AF_INET
sock_type = socket.SOCK_STREAM

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
    def recvMsg(self, conn:socket.socket):
        msgLen = int(conn.recv(self.HEADER).decode(self.FORMAT))
        return conn.recv(msgLen).decode(self.FORMAT)



class Server(BaseSocketConnector):
    def __init__(self,
        IP, PORT,
        HEADER=16,
        FORMAT='utf-8',
        DISCONNECT='!disconnect'):
        super().__init__(IP,PORT,HEADER,FORMAT,DISCONNECT)
#        self.server = None
        self.running = False
    
    def activateServer(self):
        self.server = socket.socket(sock_family, sock_type)
        self.server.bind(self.ADDR)
    
    def _listenForMsg(self, addr, conn):
        clientConnected = True
        while self.running and clientConnected:
            msg = self.recvMsg(conn)
    def _serverStart(self):
        self.server.listen()
        while self.running:
            conn, addr = self.server.accept()
            listenerThread = threading.Thread(
                target=self._listenForMsg,
                args=(addr, conn)
            )
            self._connectCallback(addr, conn)
    
    def start(self, onThread = True):
        self.activateServer()
        self.running = True
        if onThread:
            serverThread = threading.Thread(
                target=self._serverStart
            )
            serverThread.start()
        else:
            self._serverStart()