import socket
import threading
import time

class Network:
    def __init__(self, game, port = 5555):
        self.game = game
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows for port to be used after one socket just closed. Multiple udp connections in one port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #allows to broadcast messages. SOL_SOCK is the socket layer, changing option independent of protocol
        self.sock.bind(("0.0.0.0", self.port))
        self.game_players = []
        self.players_last_online = {}
        self.running = True
        self.discovery_running = False

        self.player_coords = []

        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receive_thread.start()
        self.heartbeat_thread = threading.Thread(target=self.check_players_alive, daemon=True)
        self.heartbeat_thread.start()
        self.heartbeat_sender_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
        self.heartbeat_sender_thread.start()

    def receive_loop(self):
        print("[NETWORK] Listening for messages...")
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024) #recvfrom UDP method addr returns a tuple (ip, port)
                data = data.decode()

                if data == "DISCOVER":
                    print(f"[NETWORK] Sending HELLO to {addr[0]}:{self.port}")
                    self.sock.sendto(f"HELLO {addr[0]}".encode(), (addr[0], self.port))
                elif data.startswith("POSITION"):
                    parts = data.split(":")
                    subparts = parts[1].split(",")
                    player_num = int(subparts[0])
                    x = int(subparts[1])
                    y = int(subparts[2])
                    self.game.update_online_player(player_num, x, y)
                elif data.startswith("HEARTBEAT"):
                    self.players_last_online[addr] = time.time()
                elif data.startswith("HELLO"):
                    print(f"[NETWORK] Received HELLO from {addr}")
                    if addr not in self.game_players:
                        self.game_players.append(addr)
                        self.game.add_remote_player(addr)  # You'll need to implement this method

            except Exception as e:
                print(f"ERROR-IN-RECEIVE: {e}")

    def broadcast(self, timeout = 10):
        print("[NETWORK] Starting LAN discovery...")
        self.discovery_running = True

        broadcast_thread = threading.Thread(target=self.broadcast_loop,args=(timeout,),daemon=True)
        broadcast_thread.start()

    def broadcast_loop(self, timeout):
        end_time = time.time() + timeout
        while time.time() < end_time and self.discovery_running:
            self.sock.sendto("DISCOVER".encode(), ("255.255.255.255", self.port))
            time.sleep(1)
        print(f"[NETWORK] Found {len(self.game_players)} players")


    def send_position(self, player_num, x, y):
        msg = f"POSITION:{player_num},{x},{y}"
        msg = msg.encode("utf-8")
        for player in self.game_players:
            self.sock.sendto(msg, player)


    def send_heartbeat(self):
        while self.running:
            for player in self.game_players:
                self.sock.sendto("HEARTBEAT".encode(), player)
            time.sleep(1)

    def check_players_alive(self):
        while self.running:
            try:
                current_time = time.time()
                dead_players = []
                for player, last_seen in self.players_last_online.items():
                    if current_time - last_seen > 5:
                        dead_players.append(player)

                for player in dead_players:
                    if player in self.game_players:
                        self.game_players.remove(player)
                    del self.players_last_online[player]
                time.sleep(1)
            except Exception as e:
                print(f"ERROR-IN-PLAYERS-ALIVE: {e}")

    def close(self):
        self.running = False
        self.sock.close()