import socket
import sys
import threading

def listen_for_messages(sock):
    while True:
        message = sock.recv(1024)
        if message:
            print(f"\rReceived: {message.decode('utf-8')}\nYou: ", end="")

def send_messages(sock):
    while True:
        message = input("You: ")
        if message:
            sock.sendall(message.encode())

def receive_file(connection, filename):
    with open(filename, 'wb') as file:
        data = connection.recv(1024)
        while data:
            file.write(data)
            data = connection.recv(1024)

def main():
    HOST = '127.0.0.1'
    PORT = int(input("Port: "))
    MODE = int(input("Mode (message - 0, file - 1) : "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if MODE == 1:
            s.send(b'FILE_DOWNLOAD_REQUEST')
            receive_file(s, f'recvd_file{PORT}')
            s.close()
            print('file received!!')
            return 0

        # Серверээс мэдээлэл авах утас эхлүүлэх
        thread = threading.Thread(target=listen_for_messages, args=(s,))
        thread.start()

        # Мэдээлэл илгээх
        send_messages(s)

if __name__ == "__main__":
    main()
