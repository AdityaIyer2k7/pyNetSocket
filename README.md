# PySimpleSockets
## A simple networking library for python
---
This library uses the in-built `sockets` library

It also uses the most basic client-server model

To initialize a server:
```python
from pySimpleSockets import Server

myServer = Server(
    IP,
    PORT,
    FORMAT='utf-8',
    DISCONNECT='!Disconnect'
)
myServer.start()

def callback(conn, addr, *args):
    print(f"({addr}) connected")

def disconnect(conn, addr, *args):
    print(f"({addr}) disconnected")

myServer.onConnect(callback, args=(), kwargs={})
myServer.onDicconnect(disconnect, args=(), kwargs={})
```