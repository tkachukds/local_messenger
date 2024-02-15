import socket

def encrypt(message, key):
    encrypted_message = b""
    for char in message:
        encrypted_char = (char + key) % 256
        encrypted_message += bytes([encrypted_char])
    return encrypted_message

# Получаем IP-адрес текущего хоста
host_ip = socket.gethostbyname(socket.gethostname())

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем адрес и порт для прослушивания
host = '0.0.0.0'  # Все доступные интерфейсы
port = 27080

# Привязываем сокет к адресу и порту
server_socket.bind((host, port))

# Начинаем прослушивание (максимальное количество подключений - 1)
server_socket.listen(1)

print("Сервер запущен и прослушивает порт {0}".format(port))
print("IP-адрес сервера: {0}".format(host_ip))

while True:
    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()

    print("Установлено соединение с {0}".format(client_address))

    # Запрашиваем код шифровки у клиента
    encryption_key = int(input("Введите трехзначный код шифровки: "))

    while True:
        # Читаем данные из сокета
        data = client_socket.recv(1024)

        if not data:
            print("Соединение с {0} разорвано".format(client_address))
            break

        # Расшифровываем полученное сообщение
        decrypted_data = encrypt(data, -encryption_key)

        print("Получено сообщение от {0}: {1}".format(client_address, decrypted_data.decode('utf-8')))

        # Отправляем ответ клиенту (зашифрованный)
        response = "Зашифрованное сообщение получено"
        encrypted_response = encrypt(response.encode('utf-8'), encryption_key)
        client_socket.send(encrypted_response)

    # Закрываем соединение с клиентом
    client_socket.close()
