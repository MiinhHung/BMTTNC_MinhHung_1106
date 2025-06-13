from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
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
    global clients  # Sử dụng biến toàn cục 'clients'
    print(f"Connected with {client_address}")

    # Gửi khóa công khai của server cho client
    client_socket.send(server_key.public_key().export_key(format='PEM'))

    # Nhận khóa công khai của client
    client_received_key = RSA.import_key(client_socket.recv(2048))

    # Tạo khóa AES để mã hóa tin nhắn
    aes_key = get_random_bytes(16)

    # Mã hóa khóa AES bằng khóa công khai của client
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    # Thêm client vào danh sách
    clients.append((client_socket, aes_key))

    while True:
        try:
            # Nhận tin nhắn đã mã hóa từ client
            encrypted_message = client_socket.recv(1024)
            # Giải mã tin nhắn
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            # Gửi tin nhắn đã nhận cho tất cả các client khác
            for client, key in clients:
                if client != client_socket:
                    encrypted = encrypt_message(key, decrypted_message)
                    client.send(encrypted)

            # Nếu tin nhắn là "exit", thoát khỏi vòng lặp
            if decrypted_message == "exit":
                break
        except:
            # Xử lý ngắt kết nối client
            break

    # Xóa client khỏi danh sách và đóng socket
    clients.remove((client_socket, aes_key))
    client_socket.close()
    print(f"Connection with {client_address} closed")

# Chấp nhận và xử lý các kết nối client
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
