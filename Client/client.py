from client_strings import *
import socket
from threading import Thread

is_running = True

class Client:

    def __init__(self, server_ip='localhost', server_port=65432):
        self.SERVER_INFO = (server_ip,server_port)
        self.BUFFER = 1024

        print(INITIATE_MESSAGE)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.NAME = input(NAME_MESSAGE)

        if self.connect_to_server():
            self.maintain_connection()
        else:
            self.client_socket.close()

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.SERVER_INFO)
            print(CONNECTED_MESSAGE, self.SERVER_INFO)
            print(LEAVE_MESSAGE_INFO)
            return 1

        except Exception as err:
            print(CONNECTION_ERROR_MESSAGE, err)
            return 0

    def maintain_connection(self):
        try:
            t1 = Thread(target= self.send_message, args=())
            t2 = Thread(target=self.receive_message,args=())
            
            t2.start()
            t1.start()

        except Exception as e:
            print(e)

    def receive_message(self):
        global is_running

        while is_running:
            try:
                message = self.client_socket.recv(self.BUFFER)
                if message:
                    print(message.decode())
                #else:
                #    break

            except Exception as e:
                break

    def send_message(self):
        global is_running
        while is_running:
            try:
                message = input(MESSAGE_PREFIX)
                if message.lower() != EXIT_MESSAGE:
                    complete_msg = (self.NAME + ': ' + message).encode()
                    self.client_socket.sendall(complete_msg)
                else:
                    self.client_socket.sendall(EXIT_MESSAGE.encode())
                    self.client_socket.close()
                    is_running = False

            except Exception as e:
                break
    

def main():
    client = Client()
        
if __name__ == "__main__":
    main()