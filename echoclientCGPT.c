#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>


#define RCVBUFSIZE 32
#define SERV_PORT 12345

void DieWithError(char *errorMessage){
    perror(errorMessage);
    exit(1);
}

int main() {
    int sock;
    struct sockaddr_in servAddr;
    char *serverIP = "127.0.0.1";  // Change to the server's IP address if needed
    char *message = "Hello, server!";

    // Create a socket
    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    // Initialize the server address structure
    memset(&servAddr, 0, sizeof(servAddr));
    servAddr.sin_family = AF_INET;
    if (inet_pton(AF_INET, serverIP, &servAddr.sin_addr) <= 0)
        DieWithError("inet_pton() failed");
    servAddr.sin_port = htons(SERV_PORT);

    // Connect to the server
    if (connect(sock, (struct sockaddr *)&servAddr, sizeof(servAddr)) < 0)
        DieWithError("connect() failed");

    // Send a message to the server
    if (send(sock, message, strlen(message), 0) != strlen(message))
        DieWithError("send() sent a different number of bytes than expected");

    // Receive a response from the server
    char echoBuffer[RCVBUFSIZE];
    int recvMsgSize;

    if ((recvMsgSize = recv(sock, echoBuffer, RCVBUFSIZE - 1, 0)) <= 0)
        DieWithError("recv() failed or connection closed prematurely");

    echoBuffer[recvMsgSize] = '\0';
    printf("Received: %s\n", echoBuffer);

    close(sock);

    return 0;
}

