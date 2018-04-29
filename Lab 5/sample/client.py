import socket


def start_client(address, port):
    # We're using TCP/IP as transport
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the given `address` and `port`
    client_socket.connect((address, port))
    print("=== Connected to %s:%s" % (address, port))
    while True:
        try:
            # Read input from the user (as string)
            data = raw_input(">>> ")
            client_socket.send(data.encode('utf-8'))
            # Recieve 1kB of data from the server
            data = client_socket.recv(1024)
            print("<<< %s" % (data,))
        except KeyboardInterrupt:
            break
    client_socket.close()


if __name__ == '__main__':
    start_client('127.0.0.1', 8000)