# pyNetSocket
## A simple networking library for python
---
This library uses the in-built `sockets` library

It also uses the most basic client-server model

To initialize a server:
```python
from pyNetSocket import Server

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
myServer.onDisconnect(disconnect, args=(), kwargs={})

myServer.start(onThread=True)
```

To initialize a client:
```python
from pyNetSocket import Client
myClient = Client(
    IP,
    PORT,
    FORMAT='utf-8',
    HEADER=8
    DISCONNECT='!disconnect'
)

myClient.connect(onThread=True)
```

Wiki link [here](https://github.com/DrSparky-2007/PyNetSocket/wiki/)
or try this https://github.com/DrSparky-2007/PyNetSocket/wiki/

You can also view in-built documentation:
```python
import pyNetSocket.docs
```
