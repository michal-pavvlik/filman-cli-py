#!/usr/bin/env python3
from __future__ import annotations
import os
import argparse
from abc import ABC, abstractmethod
from collections import deque

ascii_art = """    ____________    __  ______    _   __\n   / ____/  _/ /   /  |/  /   |  / | / /\n  / /_   / // /   / /|_/ / /| | /  |/ /\n / __/ _/ // /___/ /  / / ___ |/ /|  /\n/_/   /___/_____/_/  /_/_/  |_/_/ |_/  """


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
    
    def undo(self) -> None:
        self._receiver.deleteFile(self._filename)

class deleteFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self._deleted_data = None

    def execute(self) -> None:
        self._deleted_data = self._receiver.getFileContent(self._filename)
        self._receiver.deleteFile(self._filename)

    def undo(self) -> None:
        self._receiver.addFile(self._filename)
        self._receiver.editFile(self._filename, self._deleted_data)

class editFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str, file_data: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self._file_data = file_data
        self._old_file_data = None

    def execute(self) -> None:
        self._old_file_data = self._receiver.getFileContent(self._filename)
        self._receiver.editFile(self._filename, self._file_data)
    
    def undo(self) -> None:
        self._receiver.editFile(self._filename, self._old_file_data)

class moveFileCommand(Command):
    
    def __init__(self, receiver: Receiver, source_file: str, dest_file: str) -> None:
        self._receiver = receiver
        self._source_file = source_file
        self._dest_file = dest_file
    
    def execute(self) -> None:
        self._receiver.moveFile(self._source_file, self._dest_file)
    
    def undo(self) -> None:
        self._receiver.moveFile(self._dest_file, self._source_file)

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

    def moveFile(self, source_file: str, dest_file: str) -> None:
        file_not_exists = not(os.path.isfile(source_file))
        if(file_not_exists):
            print("Wrong source file!")
            return
        os.rename(source_file, dest_file)
        

    def getFileContent(self, filename):
        with open(filename, "r") as f:
            return f.read()

class Invoker:

    def __init__(self) -> None:
        self._commands_history = deque([])

    def doCommand(self, command: Command) -> None:
        command.execute()
        if(len(self._commands_history) >= 10):
            self._commands_history.popleft()
        self._commands_history.append(command)

    def undoCommand(self) -> None:
        if(len(self._commands_history) == 0):
            print("There are no commands to undo!")
            return
        previous_command = self._commands_history.pop()
        previous_command.undo()

def main():
    invoker = Invoker()
    receiver = Receiver()

    parser = argparse.ArgumentParser(prog="filman", description=f"{ascii_art}\nLightweight file manager, made with Python, created specifically for Linux terminal envirnonment.", formatter_class=argparse.RawDescriptionHelpFormatter)
    
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-a', '--add', help="Add new file", metavar="FILE")
    group.add_argument('-d', '--delete', help="Delete existing file", metavar="FILE")
    group.add_argument('-e', '--edit', nargs=2, help="Edit contents of a file, write in \"\"", metavar=("FILE", "STR_CONTENT"))
    group.add_argument('-m', '--move', nargs=2, help="Move a file between directories", metavar=("FILE_DIR1", "FILE_DIR2"))
    group.add_argument('-u', '--undo', action='store_true', help="Undo previous action")
    args = parser.parse_args()

    if(args.add):
        arg1 = args.add
        invoker.doCommand(AddFileCommand(receiver, arg1))
    elif(args.delete):
        arg1 = args.delete
        invoker.doCommand(deleteFileCommand(receiver, arg1))
    elif(args.edit):
        arg1 = args.edit[0]
        arg2 = args.edit[1]
        invoker.doCommand(editFileCommand(receiver, arg1, arg2))
    elif(args.move):
        arg1 = args.move[0]
        arg2 = args.move[1]
        invoker.doCommand(moveFileCommand(receiver, arg1, arg2))
    elif(args.undo):
        invoker.undoCommand()

if __name__ == "__main__":
    main()