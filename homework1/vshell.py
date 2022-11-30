import zipfile


class VShell:
    def __init__(self):
        self.current_path = "iso/"
        self.archive = zipfile.ZipFile('iso.zip', 'r')
        self.archive.extractall()

        self.commands = {
            "pwd": self.pwd,
            "ls": self.ls,
            "cd": self.cd,
            "cat": self.cat
        }

    @staticmethod
    def wrong_command(*args):
        raise SyntaxError("Command not found")

    @staticmethod
    def wrong_argument(args, *numbers):
        if len(args) not in numbers:
            raise ValueError("Invalid arguments")

    def add_to_path(self, addition):
        if addition == "/":
            return self.current_path

        if addition.startswith('..'):
            path = '/'.join(self.current_path.split('/')[:-addition.count('..') - 1])
            if path == "":
                raise FileNotFoundError("File not found")
            return path + "/"

        try:
            self.archive.getinfo(self.current_path + addition)
        except KeyError:
            raise FileNotFoundError("File not found")

        return self.current_path + addition

    def pwd(self, *args):
        self.wrong_argument(args, 0)
        print(self.current_path)

    def ls(self, *args):
        self.wrong_argument(args, 0, 1)
        path = self.add_to_path(args[0]) if args else self.current_path

        print("%-46s %19s %12s" % ("File Name", "Modified", "Size"))

        for file_info in self.archive.filelist:
            if not file_info.filename.startswith(path) \
                    or file_info.filename[:-1].count("/") > path.count("/") \
                    or path == file_info.filename:
                continue
            date = "%d-%02d-%02d %02d:%02d:%02d" % file_info.date_time[:6]
            print("%-46s %s %12d" % (file_info.filename, date, file_info.file_size))

    def cd(self, *args):
        self.wrong_argument(args, 1)
        self.current_path = self.add_to_path(args[0])

    def cat(self, *args):
        self.wrong_argument(args, 1)
        with self.archive.open(self.add_to_path(args[0])) as file:
            print(file.read().decode("utf-8"))

    def run(self):
        while True:
            command = input(self.current_path + ": ").split()
            try:
                self.commands.get(command[0], self.wrong_command)(*command[1:])
            except (FileNotFoundError, ValueError, SyntaxError) as e:
                print(e)


if __name__ == '__main__':
    vshell = VShell()
    vshell.run()
