import tempfile
import os.path


class File:
    def __init__(self, path_to_file):
        self.path = os.path.abspath(path_to_file)
        if os.path.exists(path_to_file):
            self.f = open(self.path, 'r+')
        else:
            self.f = open(self.path, 'w+')

    def __add__(self, other):
        other_file_path = os.path.abspath(other.path)
        temporary_path = os.path.join(tempfile.gettempdir(), "temp_file")
        with open(temporary_path, 'w+') as temp_f:
            with open(other_file_path, 'r') as other_f:
                temp_f.write(self.f.read())
                temp_f.write('\n')
                temp_f.write(other_f.read())
                temp_f.write('\n')
        return File(temporary_path)

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __str__(self):
        pass

    def read(self):  # TODO rebuild: recalling function doesn't give output..
        return self.f.read()+'\n'

    def write(self, content_to_write):  # TODO add number of symbols of writing content
        return self.f.write('\n' + content_to_write)


# file = File('file1.txt')
# print(file.read())
# file.write('line10000000')
# print(file.read())