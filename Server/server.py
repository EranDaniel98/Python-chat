from server_string import *
import socket
from threading import Thread

is_running = True

class Server:

    def __init__(self,ip='localhost', port=65432):
        # non-privileged ports are > 1023
        self.server_info = (ip,port)
        self.connected_clients_socket = []
        self.BUFFER = 1024

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
        self.bind_and_listen()
        self.handle_clients()
        
    def bind_and_listen(self):
        print(INITIATE_MESSAGE)
        self.server_socket.bind(self.server_info)

        print(CONNECTION_WAITING_MESSAGE)
        self.server_socket.listen(2)

    def handle_clients(self):
        global is_running
        while is_running:
            client_socket = self.accept_connections()
            if client_socket != None:
                t1 = Thread(target=self.maintain_server,args=(client_socket,))
                t1.start()

    def accept_connections(self):
        global is_running
        try:
            client_socket, client_info = self.server_socket.accept()
            self.connected_clients_socket.append(client_socket)

            print(CONNECTED_MESSAGE, client_info)
            print(AMOUNT_OF_CLIENTS_MESSAGE, len(self.connected_clients_socket))
            return client_socket

        except Exception as e:
            return None

    def maintain_server(self, client_socket):
        # maintain connection
        global is_running
        while is_running:
            try:
                client_message = client_socket.recv(self.BUFFER)
                if client_message:
                    if client_message.decode().lower() != EXIT_MESSAGE:
                        print(client_message.decode())
                        self.send_messages_to_all(client_socket, client_message)
                    else:
                        self.close_client_socket(client_socket)

            except Exception as e:
                break

    def close_client_socket(self,client_socket):
        global is_running

        client_socket.close()
        self.connected_clients_socket.remove(client_socket)
        print(AMOUNT_OF_CLIENTS_MESSAGE, len(self.connected_clients_socket))

        if not self.connected_clients_socket:
            self.server_socket_handler()
            is_running = False

    def server_socket_handler(self):
        close_or_keep_server = input(CLOSING_SERVER_MESSAGE)
        if close_or_keep_server == 'yes':
            self.server_socket.close()
        else:
            print(CONNECTION_WAITING_MESSAGE)
            self.handle_clients()

    def send_messages_to_all(self, sender, message):
        for soc in self.connected_clients_socket:
            if soc != sender:
                soc.sendall(message)


def main():
    server = Server()

if __name__ == "__main__":
    main()