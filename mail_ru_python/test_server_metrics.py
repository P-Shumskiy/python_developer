import sys
from client_to_send_metrics import Client, ClientError


def run(host, port):
    pass
    client1 = Client(host, port)
    client2 = Client(host, port, timeout=5)

    try:
        client1.(b"malformed command test\n")
        client1._read()
        client2.connection.sendall(b"malformed command test\n")
        client2._read()
    except ClientSocketError as err:
        print(f"Ошибка общения с сервером: {err.__class__}: {err}")
        sys.exit(1)
    except ClientProtocolError:
        pass
    else:
        print("Неверная команда, отправленная серверу, должна возвращать ошибку протокола")
        sys.exit(1)

    try:

    client1.put("palm.cpu", 0.25, timestamp=1)
    client2.put("palm.cpu", 2.156, timestamp=2)
    client1.put("palm.cpu", 0.35, timestamp=3)
    client2.put("eardrum.memory", 30, timestamp=4)
    client1.put("eardrum.memory", 40, timestamp=5)
    client1.put("eardrum.memory", 40, timestamp=5)

    except Exception as err:
        print(f"Ошибка вызова client.put(...) {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "palm.cpu": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "eardrum.memory": [(4, 30.0), (5, 40.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') вернул неверный результат. Ожидается: {expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"eardrum.memory": [(4, 30.0), (5, 40.0)]}

    try:
        metrics = client2.get("eardrum.memory")
        if metrics != expected_metrics:
            print(f"client.get('eardrum.memory') вернул неверный результат. Ожидается: {expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('eardrum.memory') {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("palm.memory")
        if result != {}:
            print(f"Ошибка вызова метода get с ключом, который еще не был добавлен. Ожидается: пустой словарь. Получено: {result}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова метода get с ключом, который еще не был добавлен: {err.__class__} {err}")
        sys.exit(1)

    print("Похоже, что все верно! Попробуйте отправить решение на проверку.")

if __name__ == "__main__":
    run("127.0.0.1", 10_001)
