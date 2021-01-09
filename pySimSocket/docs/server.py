def importing():
    print('To import the server, type:',
          'from pyNetSocket import Server',
          sep='\n')

def implement():
    print('Create a server object:',
          'myServer = Server(IP, PORT,',
          '                  HEADER=HEADER_MESSAGE,',
          '                  FORMAT=MESSAGE_FORMAT,',
          '                  DISCONNECT=DISCONNECT_MESSAGE)','',
          'Any message can contain 10^HEADER byte characters',
          'The message will be encoded in FORAMT encoding type',
          'A client will be disconnected if they send the DISCONNECT message',
          sep='\n')

def activate():
    print('To activate a server:',
          'myServer.start()',
          '',
          'To stop a server:',
          'myServer.stop()',
          sep='\n')

try:
    while True:
        topics = [
            'Importing',
            'Implementing',
            'Activating',
            'Exit'
        ]
        print('Topics:',
              *topics,
              sep='\n\t'
              )
        topic = input("-> ").lower()
        if topic.capitalize() in topics:
            if topic == "importing":
                importing()
            if topic == "implementing":
                implement()
            if topic == "activating":
                activate()
            if topic == "exit":
                print("Exiting server documentation")
                break
except:
    exit()