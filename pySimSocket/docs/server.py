def importing():
    print('''To import the server, type:
from pySimSocket import Server''')

def implement():
    print('''Create a server object:
myServer = Server(IP, PORT,
                  HEADER=HEADER_MESSAGE,
                  FORMAT=MESSAGE_FORMAT,
                  DISCONNECT=DISCONNECT_MESSAGE)

Any message can contain 10^HEADER byte characters
The message will be encoded in FORAMT encoding type
A client will be disconnected if they send the DISCONNECT message''')

def activate():
    print('''To activate a server:
myServer.start()

To stop a server:
myServer.stop()''')