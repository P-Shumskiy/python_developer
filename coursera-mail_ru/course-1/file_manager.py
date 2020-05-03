import tempfile
import os.path


class File:
    def __init__(self, path_to_file):
        self.path = os.path.abspath(path_to_file)
        self.current_pos = 0

        if not os.path.exists(path_to_file):
            open(self.path, 'w+').close()

    def __add__(self, other):
        temp_file = tempfile.NamedTemporaryFile().name
        temporary_path = os.path.join(tempfile.gettempdir(), temp_file)
        result_file = File(temporary_path)

        with open(temporary_path, 'w+') as f:
            f.write(self.read() + other.read())
            return result_file

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, content_to_write):
        with open(self.path, 'w+') as f:
            return f.write(content_to_write)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_pos)

            line = f.readline()
            if not line:
                self.current_pos = 0
                raise StopIteration("EOF")

            self.current_pos = f.tell()
            return line

    def __str__(self):
        return self.path


if __name__ == '__main__':
    print("No syntax errors")

    file1 = File('file1.txt')
    file2 = File('file2.txt')
    file1.write("'Line1'")
    file2.write('Line2')

    new_file = file1 + file2
    print(new_file)

    for line_ in new_file:
        print(line_)
        break

    print(new_file)
