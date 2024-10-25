import menus
import pyperclip
import tkinter
from tkinter import filedialog
import os
import vault as pio
from getpass import getpass


# Please pretend like this has actual documentation rn, I'll get to it eventually possibly
def get_path():
    # Importing will allow for path auto-complete only within scope
    functions = ['Manually type path', 'Get path from clipboard', 'Brose files', 'Back', 'Exit']
    valid_file = False
    path = ''
    while not valid_file:
        func = menus.list_menu(functions)

        match func:
            case "Manually type path":
                path = input("Enter path: ")
            case "Get path from clipboard":
                path = pyperclip.paste()
            case "Brose files":
                tkinter.Tk().withdraw()
                path = filedialog.askopenfilename()
            case "Back":
                # Most direct way, can be bad for memory if misused, but user would have to be stupid
                run()
                exit(0)
            case "Exit":
                exit(0)
            case _:
                print("Not a valid option")
        valid_file = os.path.isfile(path)
    return path


def create_vault():
    path = get_path()
    pw = getpass("Please enter the password you would like to use: ")
    while pw != getpass("Please confirm password: "):
        pw = getpass("Passwords did not match!\nPlease enter the password you would like to use: ")
    vault = pio.PBank(password=pw, loc=path)
    vault.run()


def access_vault():
    path = get_path()
    pw = getpass("Please enter password: ")
    vault = pio.PBank.from_path(path=path, password=pw)
    vault.run()


def run():
    # Choose function of program (Create, Access, )
    functions = ['Access Vault', 'Create New Vault', 'Exit']
    while True:
        func = menus.list_menu(functions)

        match func:
            case "Access Vault":
                access_vault()
            case "Create New Vault":
                create_vault()
            case "Exit":
                exit(0)
            case _:
                print("Not a valid option")


if __name__ == '__main__':
    run()
