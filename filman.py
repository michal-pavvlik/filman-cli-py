from __future__ import annotations
import os
from abc import ABC, abstractmethod
from collections import deque

print("""    ____________    __  ______    _   __
   / ____/  _/ /   /  |/  /   |  / | / /
  / /_   / // /   / /|_/ / /| | /  |/ / 
 / __/ _/ // /___/ /  / / ___ |/ /|  /  
/_/   /___/_____/_/  /_/_/  |_/_/ |_/  """)


# Implementation of command design pattern
class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

class AddFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str) -> None:
        self._receiver = receiver
        self._filename = filename

    def execute(self) -> None:
        self._receiver.addFile(self._filename)

class deleteFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self._deleted_data = None

    def execute(self) -> None:
        self._deleted_data = self._receiver.getFileContent(self._filename)
        self._receiver.deleteFile(self._filename)

class editFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str, file_data: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self._file_data = file_data
        self._old_file_data = None

    def execute(self) -> None:
        self._old_file_data = self._receiver.getFileContent(self._filename)
        self._receiver.editFile(self._filename, self._file_data)

class changeCwdCommand(Command):

    def __init__(self, receiver: Receiver, dirname: str) -> None:
        self._receiver = receiver
        self._dirname = dirname
        self._old_cwd = None

    def execute(self) -> None:
        self._old_cwd = os.getcwd()
        self._receiver.changeCwd(self._dirname)


class Receiver:

    def addFile(self, filename: str) -> None:
        if(os.path.isfile(filename)):
            print("File already exists!")
            return
        with open(filename, 'w') as nf:
            pass
        print(f"File {filename} created successfully.")

    def deleteFile(self, filename: str) -> None:
        file_not_exists = not(os.path.isfile(filename))
        if(file_not_exists):
            print("Can't delete file, no such name in directory!")
            return
        os.remove(filename)
        print(f"File {filename} deleted successfully.")
    
    def editFile(self, filename: str, file_data: str) -> None:
        file_not_exists = not(os.path.isfile(filename))
        if(file_not_exists):
            print("Can't edit file, no such name in directory!")
            return
        with open(filename, 'w') as nf:

            nf.write(file_data)
            pass
        print(f"File {filename} overwritten successfully.")

    def changeCwd(self, dirname: str) -> None:
        dir_not_exists = not(os.path.isdir(dirname))
        if(dir_not_exists):
            print("This directory does not exist!")
            return
        os.chdir(dirname)
        print(f"Changed current working directory to {dirname}.")

    def getFileContent(self, filename):
        with open(filename, "r") as f:
            return f.read()

class Invoker:

    def __init__(self) -> None:
        self.commands_history = deque([])

    def doCommand(self, command: Command) -> None:
        command.execute()
        if(len(self.commands_history) >= 10):
            self.commands_history.popleft()
        self.commands_history.append(command)
        print(self.commands_history)


def main():
    operations_possibilities = range(1,6)
    invoker = Invoker()
    receiver = Receiver()
    while(True):
        print("What operation would you like to do:\n1. Add file\n2. Delete file\n3. Edit file\n4. Change directory\n5. Exit")
        while(True):
            try:
                operation_id = int(input("Write down a value from 1 to 5: "))
                if operation_id not in operations_possibilities:
                    print("Input out of range")
                else:
                    break
            except ValueError:
                print("Input is not a number")
        match int(operation_id):
            case 1:
                filename = input("write down file name: ")
                invoker.doCommand(AddFileCommand(receiver, filename))
            case 2:
                filename = input("write down file name: ")
                invoker.doCommand(deleteFileCommand(receiver, filename))
            case 3:
                filename = input("write down file name: ")
                file_data = input("Write down new file data (press enter to save): ")
                invoker.doCommand(editFileCommand(receiver, filename, file_data))
            case 4:
                filename = input("write down desired directory name: ")
                invoker.doCommand(changeCwdCommand(receiver, filename))
            case 5:
                print("Shutting down the program.")
                return

if __name__ == "__main__":
    main()