#!/usr/bin/env python3
from __future__ import annotations
import os
import argparse
from abc import ABC, abstractmethod
from collections import deque
import json

ascii_art = """    ____________    __  ______    _   __\n   / ____/  _/ /   /  |/  /   |  / | / /\n  / /_   / // /   / /|_/ / /| | /  |/ /\n / __/ _/ // /___/ /  / / ___ |/ /|  /\n/_/   /___/_____/_/  /_/_/  |_/_/ |_/\n"""


# Implementation of command design pattern
class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def commandToDict(self) -> None:
        pass

class AddFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str) -> None:
        self._receiver = receiver
        self._filename = filename
    
    def commandToDict(self) -> None:
        return {"command": "Add", "arg1": self._filename, "arg2": ""}

    def execute(self) -> None:
        self._receiver.addFile(self._filename)
    
    def undo(self) -> None:
        self._receiver.deleteFile(self._filename)

class deleteFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self.deleted_data = None

    def commandToDict(self) -> None:
        return {"command": "Delete", "arg1": self._filename, "arg2": self.deleted_data}

    def execute(self) -> None:
        self.deleted_data = self._receiver.getFileContent(self._filename)
        self._receiver.deleteFile(self._filename)

    def undo(self) -> None:
        self._receiver.addFile(self._filename)
        self._receiver.editFile(self._filename, self.deleted_data)

class editFileCommand(Command):

    def __init__(self, receiver: Receiver, filename: str, file_data: str) -> None:
        self._receiver = receiver
        self._filename = filename
        self._file_data = file_data
        self._old_file_data = None

    def commandToDict(self):
        return {"command": "Edit", "arg1": self._filename, "arg2": self._old_file_data}

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
    
    def commandToDict(self) -> None:
        return {"command": "Move", "arg1": self._source_file, "arg2": self._dest_file}

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
        self._commands_history = CommandsHistory()

    def doCommand(self, command: Command) -> None:
        command.execute()
        self._commands_history.addCommand(command)

    def undoCommand(self) -> None:
        previous_command = self._commands_history.returnLastCommand()
        previous_command.undo()


# Commands History is a class responsible for whole flow of saving and retrieving file states
# In files_states_history every json object represents single command change in format
# command: ... arg1: ... arg2: ...      where arg1, arg2 represents everything needed for this command to revert
class CommandsHistory:
    def __init__(self) -> None:
        try:
            with open("commands_history.json", "r") as f:
                self._commands_history = json.load(f)
        except FileNotFoundError:
            with open("commands_history.json", "w") as f:
                json.dump([], f)
                self._commands_history = []

    def _saveChangesToJSON(self) -> None:
        with open("commands_history.json", "w") as f:
            json.dump(self._commands_history, f)

    def _removeFirst(self) -> None:
        self._commands_history = self._commands_history[1::]
        self._saveChangesToJSON()

    def _dictToCommand(self, dict) -> None:
        receiver = Receiver()
        self.command_name = dict["command"]
        match self.command_name:
            case "Add":
                return AddFileCommand(receiver, dict["arg1"])
            case "Delete":
                del_obj = deleteFileCommand(receiver, dict["arg1"])
                del_obj.deleted_data = dict["arg2"]
                return del_obj
            case "Edit":
                edit_obj = editFileCommand(receiver, dict["arg1"], "")
                edit_obj._old_file_data = dict["arg2"]
                return edit_obj
            case "Move":
                return moveFileCommand(receiver, dict["arg1"], dict["arg2"])
        print("Wrong dictionary given!!")

    def removeLast(self) -> None:
        self._commands_history = self._commands_history[:-1]
        self._saveChangesToJSON()

    def returnLastCommand(self):
        last_command_as_dict = self._commands_history[-1]
        self.removeLast()
        return self._dictToCommand(last_command_as_dict)

    def addCommand(self, command) -> None:
        if(len(self._commands_history) >= 10):
            self._removeFirst()
        self._commands_history.append(command.commandToDict())
        self._saveChangesToJSON()

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