import socket

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen()

client,add=server.accept()

closed=False

while not closed:
    txt=client.recv(1024).decode('utf-8')
    if txt =='close':
        closed=True
    else:
        print(txt)
    client.send(input('Message: ').encode('utf-8'))

client.close()
server.close()
