
# key = command, value = (parameters, info)
client_commands = {}
#client_commands['/connect'] = (('Server IP, Server Port'), 'Connect the client to the specified Server')
client_commands['/disconnect'] = ('No parameters needed', 'Disconnect the client from the server and close it')
client_commands['/sendfile'] = ('Full file path', 'sends the file to the other connected clients')
client_commands['/sendto'] = ('The name to whom you want to send message', 'send message to a specific user')
client_commands['/help'] = ('No parameters needed', 'Display all the available commands')
