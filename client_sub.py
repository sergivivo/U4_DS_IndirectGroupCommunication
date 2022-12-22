import socket
import sys
import select
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Para que se puedan suscribir múltiples clientes, es necesario que sea el
# propio broker quien asigne un puerto al suscriptor para escuchar desde ahí,
# pues el broker debe enviar el mensaje a todos los suscriptores en sockets
# diferentes.

broker_address = ('localhost', 10000)
port = 10001
messageA = b'sub:id:%i'%port
messageB = b'sub:topic:game'

try:
    # Send data
    print('sending {!r}'.format(messageA))
    sent = sock.sendto(messageA, broker_address)

    # Get assigned port
    data, address = sock.recvfrom(1024)
    port = int(data)

    # Subscribe to a topic
    print('sending {!r}'.format(messageB))
    sent = sock.sendto(messageB, broker_address)
finally:
    print('closing socket')
    sock.close()

# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', port)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
while True:
    print('\nwaiting to receive message')
    rlist, _, _ = select.select([sock], [], [])
    data, address = sock.recvfrom(1024)
    # Do stuff with data, fill this up with your code
    print('received {} bytes from {}'.format(len(data), address))
    print(data)


