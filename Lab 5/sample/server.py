import socket
from time import gmtime, strftime
import random
import string

ListOfCommands = [
    '/help - Get all available commands',
    '/hello Text - Output a text',
    '/time - Get current time',
    '/random_pass - Generates random 16 characters password',
    '/roll - Rolls the dice and gives random response'
]

def start_server(address, port, max_connections=5):
    # We're using TCP/IP as transport
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to the given address and port
    server_socket.bind((address, port))
    # Listen for incoming connection (with max connections)
    server_socket.listen(max_connections)
    print("=== Listening for connections at %s:%s" % (address, port))
    while True:
        # Accept an incomming connection
        # Note: this is blocking and synchronous processing of incoming connection
        incoming_socket, address = server_socket.accept()
        print("=== New connection from %s" % (address,))
        # Recv up to 1kB of data
        data = incoming_socket.recv(1024)
        print(">>> Received data %s" % (data,))

        if(data[0] == '/'):
            command = data[1:]
            if command == 'help':
                string_response = '\n'
                for i in range(len(ListOfCommands)):
                    string_response = string_response + ListOfCommands[i] + '\n'
                incoming_socket.send(string_response)
                incoming_socket.close()
            elif command == 'time':
                incoming_socket.send(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                incoming_socket.close()
            elif command == 'random_pass':
                random_pass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                incoming_socket.send('Your random generated pass of 16 characters : ' + random_pass)
                incoming_socket.close()
            elif command == 'roll':
                dice = random.randint(1, 6)
                incoming_socket.send('Dice has shown : ' + str(dice))
                incoming_socket.close()
            else:
                list_of_commands = command.split()
                if(list_of_commands[0] == 'hello'):
                    incoming_socket.send(command[6:])
                else:
                    incoming_socket.send('Bad Request')
                    incoming_socket.close()
        else:
            incoming_socket.send('Error functions starts with /')
            incoming_socket.close()


if __name__ == '__main__':
    start_server('127.0.0.1', 8000)