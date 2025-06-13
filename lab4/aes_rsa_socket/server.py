from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients
clients = []

# Lock for thread-safe printing
print_lock = threading.Lock()

# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle client connection
def handle_client(client_socket, client_address):
    with print_lock:
        print(f"Connected with {client_address}")

    # Send server's public key to client
    client_socket.send(server_key.publickey().export_key(format='PEM'))

    # Receive client's public key
    client_received_key = RSA.import_key(client_socket.recv(2048))

    # Generate AES key for message encryption
    aes_key = get_random_bytes(16)

    # Encrypt the AES key using the client's public key
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    # Add client to the list
    clients.append((client_socket, aes_key))

    while True:
        try:
            # Receive length of message
            raw_length = client_socket.recv(4)
            if not raw_length:
                break
            length = int.from_bytes(raw_length, byteorder='big')
            encrypted_message = b""
            while len(encrypted_message) < length:
                packet = client_socket.recv(length - len(encrypted_message))
                if not packet:
                    break
                encrypted_message += packet

            if not encrypted_message:
                break

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            with print_lock:
                print(f"Received from {client_address}: {decrypted_message}")

            # Send received message to all other clients
            for client, key in clients[:]:  # Use copy of list to avoid modification during iteration
                if client != client_socket:
                    encrypted = encrypt_message(key, decrypted_message)
                    client.send(len(encrypted).to_bytes(4, byteorder='big') + encrypted)

            if decrypted_message == "exit":
                break
        except Exception as e:
            with print_lock:
                print(f"Error handling client {client_address}: {e}")
            break

    # Clean up
    if (client_socket, aes_key) in clients:
        clients.remove((client_socket, aes_key))
    client_socket.close()
    with print_lock:
        print(f"Connection with {client_address} closed")

# Accept and handle client connections
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()