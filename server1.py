from socket import *
from threading import Thread

clients = {}  # stores {client_socket: address}
PORT = 12345

def handle_client(client_socket, address):
    username = client_socket.recv(1024).decode().strip()
    
    # if i don't get it to work remove these lines, current problem if the same username gets inputed it will enter an infinite loop
    if any(existing_username == username for sock, (addr, existing_username) in clients.items()):
        client_socket.send("Username already taken, good bye".encode())
        client_socket.close()
        return
    # this is fine
    
    clients[client_socket] = (address, username)
    welcome_msg = f"Welcome {username}! Type 'list' to see users or 'msg <username> <message>' to message someone."
    client_socket.send(welcome_msg.encode())

    try:
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.lower() == "list":
                client_list = "\n".join([f"{username} ({addr[0]})" for sock, (addr, username) in clients.items()])
                client_socket.send(f"Connected clients:\n{client_list}".encode())

            elif msg.startswith("msg"):
                parts = msg.split(" ", 2)
                if len(parts) == 3:
                    target_username = parts[1]
                    message = parts[2]
                    sent = False
                    for sock, (addr, username) in clients.items():
                        if username == target_username and sock != client_socket:
                            sock.send(f"From {clients[client_socket][1]}: {message}".encode())
                            sent = True
                            break
                    if not sent:
                        client_socket.send("User not found.".encode())
                else:
                    client_socket.send("Invalid message format. Use: msg <username> <message>".encode())

            elif msg.lower() == "close":
                break
            else:
                client_socket.send("Unknown command.".encode())
    except:
        pass
    finally:
        print(f"{clients[client_socket][1]} disconnected")
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
