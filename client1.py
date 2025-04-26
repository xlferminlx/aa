from socket import *
from threading import Thread
import sys

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print("\n" + msg)
        except:
            print("Disconnected from server.")
            break

def main():
    server_ip = input("Enter server IP: ")
    PORT = 12345

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, PORT))
    username = input("Enter your username: ")
    client_socket.send(username.encode())


    Thread(target=receive, args=(client_socket,), daemon=True).start()

    try:
        while True:
            msg = input()
            if msg.lower() == "close":
                client_socket.send(msg.encode())
                break
            client_socket.send(msg.encode())
    except:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
