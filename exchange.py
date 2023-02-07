import zmq
from threading import Thread
import socket

def forward_to_server(to_server_sock, from_client_conn):
    while True:
        message = from_client_conn.recv(1024)
        if len(message):
            to_server_sock.send(message)

def forward_to_client(to_client_conn, from_server_sock):
    while True:
        message = from_server_sock.recv()
        to_client_conn.sendall(message)

def main():
    print("Starting Exchange")
    context = zmq.Context()

    from_server_sock = context.socket(zmq.PULL)
    from_server_sock.connect("tcp://localhost:5554")

    to_server_sock = context.socket(zmq.PUSH)
    to_server_sock.bind("tcp://127.0.0.1:5555")

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.bind(("127.0.0.1", 5556))
    client_sock.listen()
    client_conn, conn_addr = client_sock.accept()

    to_client_thread = Thread(target=forward_to_client, args=(client_conn, from_server_sock))
    to_server_thread = Thread(target=forward_to_server, args=(to_server_sock, client_conn))

    to_client_thread.start()
    to_server_thread.start()

    to_client_thread.join()
    to_server_thread.join()

    client_sock.close()

if __name__ == "__main__":
    main()
