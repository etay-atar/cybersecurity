import socket
import threading

def handle_client(client_socket):
    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on port {port}")
    
    while True:
        client, addr = server.accept()
        # print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    ports = [9000, 9001, 9002]
    for port in ports:
        t = threading.Thread(target=start_server, args=(port,))
        t.daemon = True
        t.start()
    
    # Keep main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping servers...")
