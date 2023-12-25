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
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            elif data.decode('utf-8') == "file":
                receive_file(client_socket)
            else:
                print(f"Received message from {client_address}: {data.decode('utf-8')}")
                #broadcast_message(all_clients, client_socket, data)
        except:
            break
    all_clients.remove(client_socket)
    client_socket.close()

def broadcast_message(all_clients, client_socket, message):
    for other_client_socket in all_clients:
        if other_client_socket != client_socket:
            try:
                other_client_socket.send(message)
            except:
                other_client_socket.close()
                all_clients.remove(other_client_socket)

def receive_file(client_socket):
    file_size = int(client_socket.recv(1024).decode('utf-8'))
    file_name = client_socket.recv(1024).decode('utf-8')

    with open(file_name, 'wb') as file:
        while file_size > 0:
            data = client_socket.recv(1024)
            file.write(data)
            file_size -= len(data)
def start_server():
    num_ports = int(input("Enter the number of ports to listen on: "))
    ports = [int(input(f"Enter port number {i+1}: ")) for i in range(num_ports)]
    timeout = float(input("Enter the connection timeout in seconds:"))

    server_sockets = []
    all_clients = []

    for port in ports:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(1)
        server_sockets.append(server_socket)
        print(f"Listening on port {port}")

    while True:
        try:
            read_sockets, _, _ = select.select(server_sockets + all_clients, [], [])
            for notified_socket in read_sockets:
                if notified_socket in server_sockets:
                    client_socket, client_address = notified_socket.accept()
                    all_clients.append(client_socket)
                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]}")
                    threading.Thread(target=client_thread, args=(client_socket, client_address, all_clients, timeout)).start()
        except ValueError as ve:
            print(f"ValueError in select: {ve}")

if __name__ == "__main__":
    start_server()