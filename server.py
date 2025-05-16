import socket
import threading
import sys

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.164"
        self.port = 5555

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            print(f"Binding failed: {e}")
            sys.exit()

        self.socket.listen(4)
        print("Server started, Waiting for connections...")
        self.incoming_requests()

    def handle_client(self, sock):
        sock.send(str.encode("Connected"))
        reply = ""
        while True:
            try:
                data = sock.recv(2048)
                reply = data.decode("utf-8")

                if not data:
                    print("client disconnected")
                    break
                else:
                    print("client received:", reply)
                    print("Sending:", reply)

                sock.sendall(str.encode(reply))
            except:
                break

        sock.close()



    def incoming_requests(self):
        while True:
            sock, addr = self.socket.accept()
            print("Connected to:", addr)
            # Correct thread arguments and remove join()
            client_thread = threading.Thread(target=self.handle_client, args=(sock,), daemon=True)
            client_thread.start()





