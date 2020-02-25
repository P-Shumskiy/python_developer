import asyncio
import re


DATA_STORAGE = dict()
ERROR_MESSAGE = "error\nwrong command\n\n"
OK_MESSAGE = "ok\n\n"


def is_valid_message(message, command):
    splitted_message = message.split(' ')[1::]
    status = True

    try:
        assert not bool(message.split("\n")[-1])
        metric_name = str(splitted_message[0])
        assert bool(re.findall(r"\*?|(palm|eardrum)\.(cpu|memory|usage|disk_usage|network_usage)", metric_name))

        if command == "put":
            float(splitted_message[1])
            int(splitted_message[2])
            assert len(splitted_message) == 3

        elif command == "get":
            assert len(splitted_message) == 1
            # assert splitted_message[0].rstrip() == "*"

    except(AssertionError, ValueError):
        status = False

    return status


def get(message):
    if is_valid_message(message, command="get"):
        key = message.split(' ')[1]
        answer_string = "ok\n"

        if key in DATA_STORAGE.keys():
            for value, timestamp in DATA_STORAGE[key]:
                answer_string += f"{key} {value} {timestamp}\n"

            return answer_string + "\n"

        elif key.rstrip() == "*":
            for key, item in DATA_STORAGE.items():
                for value, timestamp in item:
                    answer_string += f"{key} {value} {timestamp}\n"

            return answer_string + "\n"

        else:
            return OK_MESSAGE

    return ERROR_MESSAGE


def put(message):

    if is_valid_message(message, command="put"):
        splitted_message = message.split(' ')
        key = splitted_message[1]
        value, timestamp = float(splitted_message[2]), int(splitted_message[3])

        if key not in DATA_STORAGE.keys():
            DATA_STORAGE[key] = [(value, timestamp)]

        else:
            if (value, timestamp) not in DATA_STORAGE[key]:
                DATA_STORAGE[key].append((value, timestamp))

        return OK_MESSAGE

    return ERROR_MESSAGE


def generate_answer(message):
    command = message.split(' ')[0]

    if command == "get":
        answer = get(message)
        return answer

    elif command == "put":
        answer = put(message)
        return answer

    return ERROR_MESSAGE


async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode("utf-8")
    addr = writer.get_extra_info("peername")

    answer = generate_answer(message)
    print(f"received {message} from {addr}\n")

    writer.write(answer.encode("utf-8"))
    print(f"return answer {ascii(answer)}\n")
    # print(DATA_STORAGE)
    await handle_echo(reader, writer)


def run_server(host, port):  # TODO remove params before sending
    loop = asyncio.get_event_loop()
    coroutine = asyncio.start_server(handle_echo, host, port, loop=loop)
    server = loop.run_until_complete(coroutine)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server("127.0.0.1", 10_001)

