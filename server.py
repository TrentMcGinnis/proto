import zmq
from threading import Thread

def f_input(sock):
    while True:
        message = input("Message: ")
        sock.send(message.encode("utf-8"))
        print("Message Sent")

def rx(rx_sock):
    while True:
        message = rx_sock.recv().decode("utf-8")
        print(f"Received Message: {message}")

def main():
    context = zmq.Context()

    to_exchange_sock = context.socket(zmq.PUSH)
    to_exchange_sock.bind("tcp://127.0.0.1:5554")

    from_exchange_sock = context.socket(zmq.PULL)
    from_exchange_sock.connect("tcp://localhost:5555")

    to_server_thread = Thread(target=f_input, args=(to_exchange_sock,))
    from_exchange_thread = Thread(target=rx, args=(from_exchange_sock,))
    
    to_server_thread.start()
    from_exchange_thread.start()

    to_server_thread.join()
    from_exchange_thread.join()

if __name__ == "__main__":
    main()
