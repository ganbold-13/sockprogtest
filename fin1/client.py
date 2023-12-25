import socket
import threading
import os

def listen_for_messages(sock):
    
    try:
        while True:
            data = sock.recv(1024)
            if data:
                if data.decode('utf-8') == "file":
                    receive_file(sock)
                else:
                    print(f"\rReceived: {data.decode('utf-8')}\nYou: ", end="")
    except ConnectionResetError:
        print(f"\ntimeout")

def send_messages(sock):
    while True:
        message = input("You: ")
        if message == 'exit':
            break
        if message:
            sock.sendall(message.encode())
        

def send_file(sock, file_path):
    sock.sendall("file".encode())
    file_size = os.path.getsize(file_path)
    sock.sendall(str(file_size).encode())

    # Send the file name separately
    file_name = os.path.basename(file_path)
    sock.sendall(file_name.encode())

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            sock.sendall(data)

def receive_file(sock):
    file_size = int(sock.recv(1024).decode('utf-8'))
    file_name = sock.recv(1024).decode('utf-8')

    with open(file_name, 'wb') as file:
        while file_size > 0:
            data = sock.recv(1024)
            file.write(data)
            file_size -= len(data)

def main():
    HOST = '127.0.0.1'
    PORT = int(input("Enter the server port to connect: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Start listening for messages in a separate thread
        thread = threading.Thread(target=listen_for_messages, args=(s,))
        thread.start()

        while True:
            try:
                choice = input("Choose an action: (1) Send Message, (2) Send File, (3) Exit\n")
                if choice == '1':
                    send_messages(s)
                elif choice == '2':
                    file_path = input("Enter the file path to send: ")
                    send_file(s, file_path)
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please choose again.")
            except ConnectionResetError:
                #print(f"timeout 2")
                return 0
if __name__ == "__main__":
    main()
