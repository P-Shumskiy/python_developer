import re
import socket
import time


class ClientError(BaseException):
    pass


class Client:
    def __init__(self, host: str, port: int, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

        self._sock = socket.socket()
        self._sock.connect((self._host, self._port))

    def close_conn(self):
        self._sock.close()

    @staticmethod
    def generate_output(metric_name, data_response):
        data_return = dict()

        for data in data_response:
            if metric_name == "*":
                status = bool(re.findall(
                    r"(palm|eardrum)\.(cpu|memory|usage|disk_usage|network_usage)",
                    data))
            else:
                status = bool(re.findall(f"{metric_name}", data))

            if status:
                splitted_data = data.split(' ')

                try:
                    assert len(splitted_data) == 3
                    current_metric = str(splitted_data[0])
                    timestamp = int(splitted_data[2])
                    metric_value = float(splitted_data[1])
                except(AssertionError, ValueError):
                    raise ClientError

                if data_return.get(current_metric) is None:
                    data_return[current_metric] = [(timestamp, metric_value)]
                else:
                    data_return[current_metric].append((timestamp, metric_value))

            else:
                raise ClientError

        return data_return

    def get(self, metric_name: str):
        self._sock.sendall(f"get {metric_name}\n".encode("utf-8"))

        data_response = self._sock.recv(1024) \
            .decode("utf-8") \
            .split("\n")

        if data_response[0] == "ok" and not data_response[-1] and not data_response[-2]:
            output = self.generate_output(metric_name, data_response[1:-2])
            return output
        else:
            raise ClientError

    def put(self, metric_name: str, value: float, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())

        self._sock.sendall(f"put {metric_name} {value} {timestamp}\n".encode("utf-8"))

        data_response = self._sock.recv(1024) \
            .decode("utf-8") \
            .split("\n")

        if data_response[0] == "error":
            raise ClientError


if __name__ == '__main__':
    my_conn = Client("127.0.0.1", 12_001)

    print(my_conn.get("*"))
    my_conn.put("metric", 14.4, 134213)
    my_conn.close_conn()
