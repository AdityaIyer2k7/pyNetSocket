import socket

class BaseSocket:
    def __init__(self,
            IP, PORT,
            HEADER,
            FORMAT='utf-8',
            DISCONNECT='!Disconnect'):
        def setup():
            self.IP = IP
            self.PORT = PORT
            self.ADDR = (IP, PORT)
            self.HEADER = HEADER
            self.FORMAT = FORMAT
            self.DISCONNECT = DISCONNECT
        setup()

class Server(BaseSocket):
    def __init__(self,
            IP, PORT,
            HEADER,
            FORMAT='utf-8',
            DISCONNECT='!Disconnect'):
        super().__init__(IP, PORT, HEADER, FORMAT, DISCONNECT)
        def makeCallbacks():
            self.connectCallbacks = []
            self.disconnectCallbacks = []
            self.messageCallbacks = []
        makeCallbacks()
        self.running = False
    
    def _onConnectCallback(self, addr, conn):
        for callback in self.connectCallbacks:
            callback(addr, conn)
    def _onDisconnectCallback(self, addr):
        for callback in self.disconnectCallbacks:
            callback(addr)
    def _onMessageCallback(self, addr, conn, msg):
        for callback in self.messageCallbacks:
            callback(addr, conn, msg)
    
    def onConnect(self, callback, args:tuple = (), kwargs:dict = {}) -> None:
        self.connectCallbacks.append(
            lambda addr, conn: \
            callback(addr, conn, *args, **kwargs)
        )
    def onDicconnect(self, callback, args:tuple = (), kwargs:dict = {}) -> None:
        self.disconnectCallbacks.append(
            lambda addr: \
            callback(addr, *args, **kwargs)
        )
    def onMessage(self, callback, args:tuple = (), kwargs:dict = {}) -> None:
        self.messageCallbacks.append(
            lambda addr, conn, msg: \
            callback(addr, conn, msg, *args, **kwargs)
        )
    
    def sendTo(self, conn, message):
        msgLen = str(len(message))
        sendMsgLen = (msgLen + ' ' * (self.HEADER - len(msgLen))).encode(self.FORMAT)
        conn.send(sendMsgLen)
        conn.send(message.encode(self.FORMAT))
    
    def __client_thread(self, addr, conn):
        clientConnected = True
        while self.running and clientConnected:
            msgLen = int(conn.recv(self.HEADER).decode(self.FORMAT))
            msg = conn.recv(msgLen).decode(self.FORMAT)
            self._onMessageCallback(addr, conn, msg)
    def __handle_thread_start(self):
        import threading
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.running = True
        self.server.listen()
        while self.running:
            conn, addr = self.server.accept()
            self._onConnectCallback(addr, conn)
            print("[SERVER]\tConnection!")
            clientThread = threading.Thread(target=self.__client_thread, args=(addr, conn))
            clientThread.start()
    def start(self, onThread = True):
        if onThread:
            import threading
            thread = threading.Thread(
                target = self.__handle_thread_start
            )
            thread.start()
        else:
            self.__handle_thread_start()

class Client(BaseSocket):
    def __init__(self,
            IP, PORT,
            HEADER,
            FORMAT='utf-8',
            DISCONNECT='!Disconnect'):
        super().__init__(IP, PORT, HEADER, FORMAT, DISCONNECT)
        self.messageCallbacks = []
        self.client = None
        self.connected = False
    
    def _onMessageCallback(self, msg):
        for callback in self.messageCallbacks:
            callback(msg)
    def onMessage(self, callback, args:tuple = (), kwargs:dict = {}) -> None:
        self.messageCallbacks.append(
            lambda msg:\
            callback(msg, *args, **kwargs)
        )
    def send(self, message):
        if self.client != None:
            msgLen = str(len(message))
            sendMsgLen = (msgLen + ' ' * (self.HEADER - len(msgLen))).encode(self.FORMAT)
            self.client.send(sendMsgLen)
            self.client.send(message.encode(self.FORMAT))
        else:
            raise ValueError("Can't send a message without connecting to a server")
    
    def __client_listen(self):
        while self.connected:
            msgLen = int(self.client.recv(self.HEADER).decode(self.FORMAT))
            msg = self.client.recv(msgLen).decode(self.FORMAT)
            self._onMessageCallback(msg)
    def __handle_thread_connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
    def connect(self, onThread = True):
        self.connected = True
        if onThread:
            import threading
            thread = threading.Thread(
                target = self.__handle_thread_connect
            )
            thread.start()
        else:
            self.__handle_thread_connect()

if __name__ == '__main__':
    def startServerTest():
        svr = Server(socket.gethostbyname(socket.gethostname()), 6050, 16)
        svr.onConnect(lambda addr, conn, *_, **__: print("[CLIENT]\t" + str(addr)))
        svr.onConnect(lambda addr, conn: svr.sendTo(conn, "Hello from server!"))
        svr.onMessage(
            lambda addr, conn, msg: print("[MESSAGE]{" + str(addr) + "}\t" + msg)
        )
        svr.start()
        print("[SERVER]\t" + str(svr.ADDR))
    def startClientTest():
        client = Client(socket.gethostbyname(socket.gethostname()), 6050, 16)
        client.onMessage(lambda msg, *_, **__: print("[MESSAGE]{SERVER}\t" + msg))
        print(client.messageCallbacks)
        client.connect()
        while client.client == None:
            pass
        client.send("Hello")
    startServerTest()
    startClientTest()
