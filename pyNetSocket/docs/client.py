def importing():
    print('To import the client, type:',
          'from pyNetSocket import Client',
          sep='\n')

def implement():
    print('Create a server object:',
          'myClient = Client(IP, PORT,',
          '                  HEADER=HEADER_MESSAGE,',
          '                  FORMAT=MESSAGE_FORMAT,',
          '                  DISCONNECT=DISCONNECT_MESSAGE)','',
          'Any message can contain 10^HEADER byte characters',
          'The message will be encoded in FORAMT encoding type',
          'The client will be disconnected if they send the DISCONNECT message',
          sep='\n')

def sending():
    print('To send a message to the server:',
          'myClient.send(MESSAGE)','',
          'Make sure that the MESSAGE is',
          'less than 10^HEADER bytes long',
          sep='\n')

def activate():
    print('To connect a client:',
          'myClient.connect()',
          '',
          'To stop a server:',
          'myClient.disconnect()',
          sep='\n')

try:
    while True:
        topics = [
            'Importing',
            'Implementing',
            'Activating',
            'Sending',
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
            if topic == "sending" or topic == "messaging":
                sending()
            if topic == "exit":
                print("Exiting server documentation")
                break
except:
    exit()