### This code is a naive example of a pub/sub implementation
### TASK: improve the model
import socket
import sys
import select
import queue
import collections

# Any data received by this queue will be sent
send_queue = queue.Queue()

# Any data sent to ssock shows up on rsock
rsock, ssock = socket.socketpair()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

subscribers = dict()
channels = collections.defaultdict(list)

# Para que se puedan suscribir múltiples clientes, es necesario que sea el
# propio broker quien asigne un puerto al suscriptor para escuchar desde ahí,
# pues el broker debe enviar el mensaje a todos los suscriptores en sockets
# diferentes.

subscriber_port = 10001 # Puerto a partir del cual se irán agregando nuevos suscriptores

while True:
    print('\nwaiting to receive message')
    print(channels)

    rlist, _, _ = select.select([sock, rsock], [], [])
    for ready_socket in rlist:
        print(ready_socket)
        if ready_socket is sock:
            data, address = sock.recvfrom(1024)
            # Do stuff with data, fill this up with your code

            print('received {} bytes from {}'.format(len(data), address))
            print(data)

            if data:
                cmd,arg,msg = data.split(b":")
                if b"sub" in cmd:
                    if b"id" in arg:
                        # Cambio:
                        # -> Ahora el puerto no lo decide el suscriptor, sino el broker
                        # -> Es necesario enviar el puerto al suscriptor
                        print(subscriber_port)
                        subscribers[address]  = (address[0],subscriber_port)
                        sock.sendto(b'%i' % subscriber_port, address)
                        subscriber_port += 1
                    elif b"topic" in arg:
                        topic = str(msg)
                        print(topic)
                        channels[topic].append(subscribers[address])
                elif b"pub" in cmd:
                    topic = str(topic)
                    if topic in channels:
                        for subcriber_adress in channels[topic]:
                            sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sent = sock2.sendto(msg, subcriber_adress)
                            sock2.close()

        else:
            # Ready_socket is rsock
            rsock.recv(1)  # Dump the ready mark
            # Send the data.
            rsock.sendall(send_queue.get())
