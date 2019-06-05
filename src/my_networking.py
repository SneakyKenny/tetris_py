from __future__ import print_function
import socket
import select
import errno
import json

import tetris

HEADER_LENGTH = 10

IP = "25.9.28.33"
#IP = "25.105.26.125"
PORT = 1234

class GameServer:
    def __init__(self, IP = None, PORT = None, is_init_on_create = True, is_run_on_create = True):
        self.server_socket = None
        self.sockets_list = []
        self.clients = {}
        self.IP = IP
        self.PORT = PORT
        if is_init_on_create:
            self.init_game_server()
        if is_run_on_create:
            self.game_server_loop()

    def init_game_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.IP, self.PORT))
            self.server_socket.listen()
            self.sockets_list = [self.server_socket]
            print(f'Listening for connections on {self.IP}:{self.PORT}...')
            return True
        except:
            print('invalid ip or port, server failed to create')
            return False

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:
            return False

    def game_server_loop(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    user = self.receive_message(client_socket)

                    if user is False:
                        continue

                    self.sockets_list.append(client_socket)

                    self.clients[client_socket] = user

                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

                else:
                    message = self.receive_message(notified_socket)

                    if message is False:
                        print('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))

                        self.sockets_list.remove(notified_socket)

                        del self.clients[notified_socket]

                        #if len(self.clients) == 0:
                        #    self.server_socket.close()
                        #    sys.exit()

                        continue

                    user = self.clients[notified_socket]

                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]



#---------------------------------------------------------------------------



class GameClient:
    def __init__(self, username = '', tetris = None):
        # TODO: add a reference to a player's tetris game:
        #       so that we continuously read for lines to send
        #       if there is any, send the information over the network and reset it
        self.username = username
        self.client_socket = None
        self.tetris = tetris
        self.is_connected = False
        self.init_game_client()
        if self.is_connected:
            print('client created and connected')
            self.send_on_connect_message()

    def init_game_client(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((IP, PORT))
            self.client_socket.setblocking(False) # we might want to change that later ? #FIXME ?
            self.is_connected = True
        except:
            self.is_connected = False

    def send_on_connect_message(self):
        enc_username = self.username.encode('utf-8')
        username_header = f"{len(enc_username):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + enc_username)

    def encode_message(self, message):
        enc_message = message.encode('utf-8')
        message_header = f"{len(enc_message):<{HEADER_LENGTH}}".encode('utf-8')
        return message_header + enc_message

    def create_client_message(self):
        obj = {'lines_sent': self.tetris.lines_sent, 'chunks': self.tetris.chunks}
        json_obj = json.dumps(obj)
        return json_obj

    def is_all_zeros(self):
        for e in self.tetris.chunks:
            if e != 0:
                return False
        return True

    def game_client_loop_check(self):
        if self.tetris is not None:
            if self.tetris.lines_sent != 0 and not self.is_all_zeros():
                enc_message = self.encode_message(self.create_client_message())
                self.client_socket.send(enc_message)
                print(f'sent {self.tetris.lines_sent} lines')
                self.tetris.clear_sent_lines()
            else:
                # no lines to send, just skip to check for incoming lines
                #print('no lines to send')
                pass

            try:
                username_header = self.client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server')
                    return False

                username_length = int(username_header.decode('utf-8').strip())

                username = self.client_socket.recv(username_length).decode('utf-8')

                message_header = self.client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.client_socket.recv(message_length).decode('utf-8')

                #print(f'{username} > {message}')

                json_obj = json.loads(message)

                chunks = json_obj.get("chunks")
                print('recieved chunks:', chunks)
                lines_recieved = json_obj.get("lines_sent")

                #print(f'recieved {json_obj.get("lines_sent")} lines')

                self.tetris.pending_chunks += chunks
                self.tetris.pending_lines += lines_recieved

                #print(self.tetris.pending_chunks)

                return True

            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    return False
                return True

        #else:
        #    message = input(f'{self.username} > ')

        #    if message:
        #        enc_message = self.encode_message(message)
        #        self.client_socket.send(enc_message)

        #    print('lol')
