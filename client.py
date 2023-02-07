import socket
from threading import Thread

def tx(exchange_socket):
    message = input("Message: ")
    exchange_socket.sendall(message.encode("utf-8"))

def rx(exchange_socket):
    message = exchange_socket.recv(1024).decode("utf-8")
    print(f"Message Received: {message}")

def main():
    exchange_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exchange_socket.connect(("localhost", 5556))

    rx_thread = Thread(target=rx, args=(exchange_socket,))
    tx_thread = Thread(target=tx, args=(exchange_socket,))

    rx_thread.start()
    tx_thread.start()

    rx_thread.join()
    tx_thread.join()

    exchange_socket.close()

if __name__ == "__main__":
    main()
