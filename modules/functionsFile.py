from os.path import exists

class FileFunctions:

    def __init__(self):
        pass

    def exists(self, file):
        return exists(file)

    def read(self, file, mode='r'):
        if self.exists(file=file):
            with open(file, mode) as reader:
                return reader.read()

    def readLines(self, file, mode='r'):
        if self.exists(file=file):
            with open(file, mode) as reader:
                return reader.readlines()
