import threading
import socket


sock_family = socket.AF_INET
sock_type = socket.SOCK_STREAM

def getThisIP():
    return socket.gethostbyname(
        socket.gethostname()
    )

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
        self.messageCallbacks.append(
            lambda addr, conn, msg:\
            callback(addr, conn, msg, *args, **kwargs)
        )
        
    def sendTo(self, conn, msg):
        msgLen = str(len(msg))
        msgLenSized = msgLen + ' '*(self.HEADER - len(msgLen))
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
        self.running = False
        self.server = None
        self.conns = []
    
    def _activateServer(self):
        self.server = socket.socket(sock_family, sock_type)
        self.server.bind(self.ADDR)
    
    def _listenForMsg(self, addr, conn:socket.socket):
        clientConnected = True
        while self.running and clientConnected:
            msg = self.recvMsg(conn)
            self._messageCallback(addr, conn, msg)
            if msg == self.DISCONNECT:
                clientConnected = False
        conn.close()
        self._disconnectCallback(addr)
    def _serverStart(self):
        self.server.listen()
        while self.running:
            conn, addr = self.server.accept()
            self.conns.append(conn)
            listenerThread = threading.Thread(
                target=self._listenForMsg,
                args=(addr, conn)
            )
            listenerThread.start()
            self._connectCallback(addr, conn)
        self.server.close()
    
    def start(self, onThread = True):
        self._activateServer()
        self.running = True
        if onThread:
            serverThread = threading.Thread(
                target=self._serverStart
            )
            serverThread.start()
        else:
            self._serverStart()
    def stop(self):
        for conn in self.conns:
            conn.close()
        self.running = False

class Client(BaseSocketConnector):
    def __init__(self,
        IP, PORT,
        HEADER=16,
        FORMAT='utf-8',
        DISCONNECT='!disconnect'):
        super().__init__(IP, PORT, HEADER, FORMAT, DISCONNECT)
        self.connected = False
        self.server = None
    
    def _activateClient(self):
        self.server = socket.socket(sock_family, sock_type)
        self.server.connect(self.ADDR)
    
    def send(self, msg):
        if self.server != None:
            self.sendTo(self.server, msg)
    def listen(self):
        while self.connected:
            msg = self.recvMsg(self.server)
            self._messageCallback(self.ADDR, self.server, msg)
            if msg == self.DISCONNECT:
                self.sendTo(self.server, self.DISCONNECT)
                self.connected = False
        self.server.close()
        self._disconnectCallback(self.ADDR)
    def connect(self, onThread=True):
        self._activateClient()
        self._connectCallback(self.ADDR, self.server)
        self.connected = True
        if onThread:
            listenerThread = threading.Thread(
                target=self.listen
            )
            listenerThread.start()
        else:
            self.listen()
    def disconnect(self):
        self.send(self.DISCONNECT)
        self.connected = False
        self._disconnectCallback(self.ADDR)


if __name__ == "__main__":
    svr = Server(getThisIP(), 6050)
    svr.onConnect(lambda addr, conn:\
        print(f"[CONNECT]{addr}") )
    svr.onMessage(lambda addr, conn, msg:\
        print(f"[SERVER]{addr} {msg}") )
    svr.start()
    print(svr.ADDR)
    cli1 = Client(getThisIP(), 6050)
    cli2 = Client(getThisIP(), 6050)
    cli1.connect()
    cli2.connect()
    cli1.send("Client1")
    cli2.send("Client2")
    cli1.disconnect()
    cli2.send("Bye bye")
    cli2.disconnect()
    svr.stop()