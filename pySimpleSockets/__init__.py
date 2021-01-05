import socket

class Server:
    def __init__(self,
            IP, PORT,
            HEADER,
            FORMAT='utf-8',
            DISCONNECT='!Disconnect'):
        def setup():
            self.SIP = IP
            self.PORT = PORT
            self.ADDR = (IP, PORT)
            self.HEADER = HEADER
            self.FORMAT = FORMAT
            self.DISCONNECT = DISCONNECT
        def makeCallbacks():
            self.connectCallbacks = []
            self.disconnectCallbacks = []
            self.messageCallbacks = []
        setup()
        makeCallbacks()
        self.running = False
    
    def _onConnectCallback(self, addr, conn):
        for callback in self.connectCallbacks:
            callback(addr, conn)
    def _onDisconnectCallback(self, addr):
        for callback in self.disconnectCallbacks:
            callback(addr)
    def _onMessageCallback(self, addr, conn):
        for callback in self.messageCallbacks:
            callback(addr, conn)
    
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
            lambda addr, conn: \
            callback(addr, conn, *args, **kwargs)
        )
    
    def sendTo(self, conn, message):
        msgLen = str(len(message))
        sendMsgLen = (msgLen + ' ' * (self.HEADER - len(msgLen))).encode(self.FORMAT)
        conn.send(sendMsgLen)
        conn.send(message.encode(self.FORMAT))
    
    def __handle_thread_start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.ADDR)
        self.running = True
        server.listen()
        while self.running:
            conn, addr = server.accept()
            self._onConnectCallback(addr, conn)
    
    def start(self, onThread = True):
        if onThread:
            import threading
            thread = threading.Thread(
                target = self.__handle_thread_start()
            )
            thread.start()
        else:
            self.__handle_thread_start()
