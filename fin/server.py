import socket
import select
import threading

def close_connection_after_timeout(client_socket, timeout):
    def close_connection():
        print(f"Closing connection with {client_socket.getpeername()}")
        client_socket.close()

    timer = threading.Timer(timeout, close_connection)
    timer.start()

def client_thread(client_socket, client_address, all_clients, timeout):
    close_connection_after_timeout(client_socket, timeout)
    
    message = client_socket.recv(1024)
    if message == b"FILE_DOWNLOAD_REQUEST":
        send_file(client_socket, 'serverfile.txt')
        client_socket.close()
        print('file sent!!')
        return 0
    while True:
        try:in listen(1) function. what is the 1 argument


            message = client_socket.recv(1024)
            if not message:
                break
            
            print(f"Received message from {client_address}: {message.decode('utf-8')}")
            for other_client_socket in all_clients:
                if other_client_socket != client_socket:
                    try:
                        other_client_socket.send(message)
                    except:
                        other_client_socket.close()
                        all_clients.remove(other_client_socket)
        except:
            break
    client_socket.close()

def send_file(connection, filename):
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            connection.send(data)
            data = file.read(1024)

def start_server():
    num_ports = int(input("Enter the number of ports to listen on: "))
    ports = [int(input(f"Enter port number {i+1}: ")) for i in range(num_ports)]
    timeout = float(input("Enter the connection timeout in seconds: "))

    server_sockets = []
    all_clients = []

    for port in ports:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen()
        server_sockets.append(server_socket)
        print(f"Listening on port {port}")

    while True:
        read_sockets, _, _ = select.select(server_sockets + all_clients, [], [])
        for notified_socket in read_sockets:
            if notified_socket in server_sockets:
                client_socket, client_address = notified_socket.accept()
                all_clients.append(client_socket)
                print(f"Accepted new connection from {client_address[0]}:{client_address[1]}")
                threading.Thread(target=client_thread, args=(client_socket, client_address, all_clients, timeout)).start()

if __name__ == "__main__":
    start_server()
