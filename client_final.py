import socket
from cryptography.fernet import Fernet

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        print("Connected to the server.")

        # Receive the encryption key from the server
        key = client_socket.recv(1024)
        cipher = Fernet(key)
        print("Received Encryption Key:", key.decode())

        while True:
            try:
                message = input("Client: ")
                if message.lower() == 'exit':
                    print("Exiting client...")
                    break

                encrypted_message = cipher.encrypt(message.encode())
                client_socket.sendall(encrypted_message)

                encrypted_response = client_socket.recv(1024)
                if not encrypted_response:
                    print("No response from server. Closing connection.")
                    break

                decrypted_response = cipher.decrypt(encrypted_response).decode()
                print(f"Server: {decrypted_response}")

            except Exception as e:
                print(f"Error during communication: {e}")
                break

    except Exception as e:
        print(f"Could not connect to the server: {e}")

    finally:
        client_socket.close()
        print("Connection closed.")

start_client()
