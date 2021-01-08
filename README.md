# PySimSocket
## A simple networking library for python
---
This library uses the in-built `sockets` library

It also uses the most basic client-server model

To initialize a server:
```python
from pySimSocket import Server

myServer = Server(
    IP,
    PORT,
    FORMAT='utf-8',
    HEADER=8
    DISCONNECT='!disconnect'
)

def connect(addr, conn):
    print(f"({addr}) connected")

def disconnect(addr):
    print(f"({addr}) disconnected")

def message(addr, conn, msg):
    print("[MESSAGE]", addr, msg)

myServer.onConnect(connect, args=(), kwargs={})
myServer.onMessage(message, args=(), kwargs={})
myServer.onDicconnect(disconnect, args=(), kwargs={})

myServer.start(onThread=True)
```

To initialize a client:
```python
from pySimSocket import Client
myClient = Client(
    IP,
    PORT,
    FORMAT='utf-8',
    HEADER=8
    DISCONNECT='!disconnect'
)

myClient.connect(onThread=True)
```
