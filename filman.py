import os

print("""    ____________    __  ______    _   __
   / ____/  _/ /   /  |/  /   |  / | / /
  / /_   / // /   / /|_/ / /| | /  |/ / 
 / __/ _/ // /___/ /  / / ___ |/ /|  /  
/_/   /___/_____/_/  /_/_/  |_/_/ |_/  """)

operations_possibilities = range(1,6)

def addNewFile():
    new_file_name = input("Name of the file to create (with format): ")
    if(os.path.isfile(new_file_name)):
        print("File already exists!")
        return
    with open(new_file_name, 'w') as nf:
        pass
    print(f"File {new_file_name} created successfully.")

def delteFile():
    to_delete_file_name = input("File to delete: ")
    file_not_exists = not(os.path.isfile(to_delete_file_name))
    if(file_not_exists):
        print("Can't delete file, no such name in directory!")
        return
    os.remove(to_delete_file_name)
    print(f"File {to_delete_file_name} deleted successfully.")

def editFile():
    to_edit_file_name = input("File to edit: ")
    file_not_exists = not(os.path.isfile(to_edit_file_name))
    if(file_not_exists):
        print("Can't edit file, no such name in directory!")
        return
    with open(to_edit_file_name, 'w') as nf:
        to_edit_file_data = input("Write down new file data (press enter to save): ")
        nf.write(to_edit_file_data)
        pass
    print(f"File {to_edit_file_name} overwritten successfully.")

def changeCWD():
    to_change_cwd_name = input("New directory name: ")
    dir_not_exists = not(os.path.isdir(to_change_cwd_name))
    if(dir_not_exists):
        print("This directory does not exist!")
        return
    os.chdir(to_change_cwd_name)
    print(f"Changed current working directory to {to_change_cwd_name}.")


def main():
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
                addNewFile()
            case 2:
                delteFile()
            case 3:
                editFile()
            case 4:
                changeCWD()
            case 5:
                print("Shutting down the program.")
                return
if __name__ == "__main__":
    main()