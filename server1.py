from socket import *
from threading import Thread

clients = {}  # Stores {client_socket: address}
PORT = 12345

def handle_client(client_socket, address):
    clients[client_socket] = address
    welcome_msg = f"Welcome {address[0]}! Type 'list' to see users or 'msg <ip> <message>' to message someone."
    client_socket.send(welcome_msg.encode())

    try:
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.lower() == "list":
                client_list = "\n".join([f"{addr[0]}" for sock, addr in clients.items()])
                client_socket.send(f"Connected clients:\n{client_list}".encode())

            elif msg.startswith("msg"):
                parts = msg.split(" ", 2)
                if len(parts) == 3:
                    target_ip, message = parts[1], parts[2]
                    sent = False
                    for sock, addr in clients.items():
                        if addr[0] == target_ip and sock != client_socket:
                            sock.send(f"From {address[0]}: {message}".encode())
                            sent = True
                            break
                    if not sent:
                        client_socket.send("Client not found.".encode())
                else:
                    client_socket.send("Invalid message format. Use: msg <ip> <message>".encode())

            elif msg.lower() == "close":
                break
            else:
                client_socket.send("Unknown command.".encode())
    except:
        pass
    finally:
        print(f"{address} disconnected")
        clients.pop(client_socket, None)
        client_socket.close()


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
