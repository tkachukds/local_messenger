import socket

def encrypt(message, key):
    encrypted_message = b""
    for char in message:
        encrypted_char = (char + key) % 256
        encrypted_message += bytes([encrypted_char])
    return encrypted_message

def client():
    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Запрашиваем у пользователя адрес сервера
    server_ip = input("Введите IP адрес сервера: ")
    server_port = 27080  # Порт сервера
    
    # Подключаемся к серверу
    server_address = (server_ip, server_port)
    
    try:
        client_socket.connect(server_address)
        print(f"Успешное подключение к серверу {server_ip}:{server_port}")
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Проверьте правильность IP адреса и порта.")
        return
    
    # Запрашиваем код шифровки у пользователя
    encryption_key = int(input("Введите трехзначный код шифровки: "))

    while True:
        # Вводим сообщение от пользователя
        message = input("Введите сообщение: ")
        
        # Шифруем сообщение перед отправкой
        encrypted_message = encrypt(message.encode('utf-8'), encryption_key)
        client_socket.send(encrypted_message)

        print(f"Отправлено зашифрованное сообщение: {encrypted_message}")
        
        # Получаем ответ от сервера (зашифрованный)
        encrypted_response = client_socket.recv(1024)

        # Расшифровываем полученный ответ
        decrypted_response = encrypt(encrypted_response, -encryption_key)
        print("Ответ от сервера:", decrypted_response.decode('utf-8'))

    # Закрываем соединение
    client_socket.close()

if __name__ == "__main__":
    client()
