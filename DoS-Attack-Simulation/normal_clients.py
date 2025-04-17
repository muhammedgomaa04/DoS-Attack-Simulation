import socket
import threading
import time
import random

HOST = '127.0.0.1'
PORT = 8080

def fast_client(cid):
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        s.sendall(f"[Fast-{cid}] Hi!".encode())
        s.close()
    except:
        pass

def slow_client(cid):
    try:
        time.sleep(random.uniform(0.5, 2))
        s = socket.socket()
        s.connect((HOST, PORT))
        s.sendall(f"[Slow-{cid}] I'm slow...".encode())
        time.sleep(random.uniform(1, 2))
        s.close()
    except:
        pass

def chatty_client(cid):
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        for i in range(random.randint(2, 5)):
            s.sendall(f"[Chatty-{cid}] Msg {i+1}".encode())
            time.sleep(random.uniform(0.3, 0.6))
        s.close()
    except:
        pass

def continuous_clients():
    cid = 1
    while True:
        behavior = random.choice([fast_client, slow_client, chatty_client])
        delay = random.uniform(0, 5)
        threading.Timer(delay, behavior, args=(cid,)).start()
        cid += 1
        time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    threading.Thread(target=continuous_clients, daemon=True).start()
    while True:
        time.sleep(1)
