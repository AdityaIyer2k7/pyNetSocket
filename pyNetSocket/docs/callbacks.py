def onconnect():
    print('To add connection callbacks to a connector:',
          'myConnector.onConnect(CALLBACK, args=args, kwargs=kwargs)',
          'The function will be given the address and connection object, then the args and kwargs',
          sep='\n')

def ondisconnect():
    print('To add disconnection callbacks to a connector:',
          'myConnector.onDisconnect(CALLBACK, args=args, kwargs=kwargs)',
          'The function will be given the address, then the args and kwargs',
          'It will not get the connection object since the connection is closed',
          sep='\n')

def onmessage()
    print('To add message-receive calbacks to a connector:',
          'myConnector.onMessage(CALLBACK, args=args, kwargs=kwargs)',
          'The function will be given the address, connection object, message, and then the args and kwargs',
          sep='\n')
 
try:
    topics = [
        'Connect',
        'Disconnect',
        'Message',
        'Exit'
    ]
    while True:
        print("Topics:".
              *topics,
              sep='\n\t')
        topic = input("> ").lower()
        if topic.capitalize() in topics:
            if topic == 'connect':
                onconnect()
            if topic == 'disconnect':
                ondisconnect()
            if topic == 'message':
                onmessage()
            if topic == 'exit':
                break
except:
    exit()
