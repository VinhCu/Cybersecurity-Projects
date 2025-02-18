import socket
from cryptography.fernet import Fernet

def start_server():
    # Generate a new encryption key
    key = Fernet.generate_key()
    cipher = Fernet(key)
    print("Generated Encryption Key:", key.decode())

    # Set up the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    conn, addr = server_socket.accept()
    print(f"Connected to client: {addr}")

    # Send the key to the client
    conn.sendall(key)

    while True:
        try:
            encrypted_message = conn.recv(1024)
            if not encrypted_message:
                print("No message received. Closing connection.")
                break

            decrypted_message = cipher.decrypt(encrypted_message).decode()
            print(f"Client: {decrypted_message}")

            response = input("Server: ")
            encrypted_response = cipher.encrypt(response.encode())
            conn.sendall(encrypted_response)

        except Exception as e:
            print(f"Error during communication: {e}")
            break

    conn.close()
    server_socket.close()

start_server()
