import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('localhost',9999))

closed =False

while not closed:
    client.send(input('Message: ').encode('utf-8'))
    txt=client.recv(1024).decode('utf-8')
    if txt=='close':
        closed=True
    else:
        print(txt)

client.close()