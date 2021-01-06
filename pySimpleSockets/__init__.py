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
    
    def onConnect(self, callback, args, kwargs):
        self.connectCallbacks.append(
            lambda addr, conn: \
            callback(addr, conn, *args, **kwargs)
        )
    def onDicconnect(self, callback, args, kwargs):
        self.disconnectCallbacks.append(
            lambda addr: \
            callback(addr, *args, **kwargs)
        )
    def onMessage(self, callback, args, kwargs):
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
            msg_size = int(\
                self.server.recv(self.HEADER)\
                .decode(self.FORMAT)
                )
            msg = self.server.recv(msg)
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
            print("Connection!")
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

if __name__ == '__main__':
    svr = Server(socket.gethostbyname(socket.gethostname()), 6050, 16)
    print(svr.ADDR)
    svr.start()
