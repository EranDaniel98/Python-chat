import socket, tqdm, os
import commands
from client_strings import *
from threading import Thread

is_running = True

class Client:

    def __init__(self, server_ip='localhost', server_port=65432):
        self.SERVER_INFO = (server_ip,server_port)
        self.BUFFER = 4096
        self.commands = commands.client_commands

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
            self.client_socket.sendall(self.NAME.encode())
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
                message = self.client_socket.recv(self.BUFFER).decode()
                if message == SENDING_FILE_MESSAGE:
                    if input('A file has received, do you want to save it ? y/n ').lower() == 'y':
                        self.recv_file()
                else:
                    print(message)

            except Exception as e:
                break

    def send_message(self):
        global is_running
        while is_running:
            try:
                message = input()
                if not message.startswith('/'): # Normal msg
                    complete_msg = (self.NAME +': '+ message).encode()
                    self.client_socket.sendall(complete_msg)
                else:
                    self.Handle_commands(message)

                
            except Exception as e:
                break
    
    def Handle_commands(self, message):
        if message.lower() == SHOW_COMMANDS_MESSAGE: #help - print all commands
            for key in self.commands.keys():
                print(f'[{key}], PARAMETERS: {self.commands[key][0]}, INFO: {self.commands[key][1]}')

        elif SEND_FILE_MESSAGE in message.lower(): # Send File to all
            if message.lower() == SEND_FILE_MESSAGE:
                print('Some parameters are missing!! try again')
                return
            else:
                filename = message.replace(SEND_FILE_MESSAGE,'') # leaves only the path
                self.send_file(filename)

        #elif message.lower() == SEND_TO_MESSAGE:

        elif message.lower() == EXIT_MESSAGE: # Disconnect from the server
            print('disconnecting from the server...')
            self.client_socket.sendall(EXIT_MESSAGE.encode())
            self.client_socket.close()
            is_running = False
        
        else:
            print('Unkown command or command parameters! try using [/help] to see all the avaliable commands')

    #C:/Users/Eran Daniel/Desktop/Test.txt
    def send_file(self, file_path):
        fileSize = 0
        filename = os.path.basename(file_path) # the file name and extencion 

        try:
            fileSize = os.path.getsize(file_path)
            self.client_socket.send(f'Incoming file: {filename}, size: {fileSize} bytes'.encode())
            self.client_socket.sendall(f'{filename}, {fileSize}'.encode())

            progress = tqdm.tqdm(range(fileSize), f'Sending {filename}\n', unit='B', unit_scale=True, unit_divisor=1024)
            with open(file_path,"rb") as f:
                while True:
                    bytes_read = f.read(self.BUFFER)
                    if not bytes_read:
                        break
                    self.client_socket.sendall(bytes_read)
                    progress.update(len(bytes_read))

            self.client_socket.sendall('File Has been sent')

        except Exception as e:
            print(e)
    
    def recv_file(self):
        message = self.client_socket.recv(self.BUFFER).decode()
        filename, filesize = message.split(', ')
        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize),f'Receiving {filename}',unit='B',unit_scale=True,unit_divisor=1024)
        with open(filename,"wb") as f:
            while True:
                bytes_read = self.client_socket.recv(self.BUFFER)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))


def main():
    client = Client()
        
if __name__ == "__main__":
    main()